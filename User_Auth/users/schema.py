from django.contrib.auth import get_user_model
import graphene

from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

########################################################
#                        """ QUERY """


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()




class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    status = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        status = "Link created Successfully"
        return CreateUser(
            status=status,
            user = user,
        )


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

#schema = graphene.Schema(query=Query, mutation=Mutation)
