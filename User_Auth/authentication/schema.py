import graphene
import status as status
from graphene_django import DjangoObjectType

from .models import Link
from .models import Vote
from users.schema import UserType



class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

########################################################
#                        """ QUERY """


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()



########################################################
#               MUTATIONS


class CreateLink(graphene.Mutation):
    """
        these are the fields which i want to return after creation
        """
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    status = graphene.String()
    posted_by = graphene.Field(UserType)

    """
        these are the fields which i want to pass as argument 
        """
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    def mutate(self, info , url, description):
        user = info.context.user or None

        link = Link(
            url=url,
            description = description,
            posted_by = user,
        )
        link.save()

        status= "Link created Successfully"
        return CreateLink(
            status=status,
            id = link.id,
            url = link.url,
            description = link.description,
            posted_by = link.posted_by,
        )




class UpdateLink(graphene.Mutation):
    status = graphene.String()

    class Arguments:
        id=graphene.Int()
        url = graphene.String()

    def mutate(self, info, id, url):
        instance = Link.objects.get(id= id)
        if instance:
            instance.url=url
            instance.save()
            status = "link Upadated Successfully"
            return UpdateLink(
                status=status
            )
        return None


class DeleteLink(graphene.Mutation):
    id= graphene.Int()
    status = graphene.String()

    class Arguments:
        id = graphene.Int()
        #description = graphene.String()

    def mutate(self,info, id):
        instance=Link.objects.get(id=id)
        if instance:
            instance.delete()
            status = "Instance Deleted Successfully"
            return DeleteLink(
                status=status
            )
        return None


class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)
    status = graphene.String()

    class Arguments:
        link_id = graphene.Int()

    def mutate(self,info, link_id):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('You must be logged in  to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception("Invalid Link")

        vote = Vote(
            user=user,
            link = link,
        )
        vote.save()

        status = "Votted Successfully"
        print(status)
        return CreateVote(
            status=status,
            user = user,
            link=link,
        )

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()



class Mutation(graphene.ObjectType):
    create_link= CreateLink.Field()
    delete_link = DeleteLink.Field()
    update_link = UpdateLink.Field()

    create_Vote =CreateVote.Field()

#schema = graphene.Schema(query=Query, mutation=Mutation)
