import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import UserRegistration, post, Tag


class UserRegistrationType(DjangoObjectType):
    class Meta:
        model=UserRegistration
        # fields=("username","email")

class postType(DjangoObjectType):
    class Meta:
        model=post
        # fields=("user","title"," description")

class TagType(DjangoObjectType):
    class Meta:
        model=Tag
class ABC(graphene.ObjectType):
    post_id=graphene.String()
    title=graphene.String()
    description=graphene.String()
    tags=graphene.String()

class Query(graphene.ObjectType):
    users = graphene.Field(UserRegistrationType, id=graphene.ID())
    all_users = graphene.List(UserRegistrationType)
    all_post = graphene.List(postType)
    all_tag = graphene.List(TagType)
    posts= graphene.List(postType,user=graphene.String(),title=graphene.String())

    def resolve_posts(root,info,user=None,title=None,**kwargs):
        if user:
            return post.objects.filter(user__username=user)

    def resolve_users(root, info,id):
        return UserRegistration.objects.get(id=id)

    def resolve_all_users(root, info):
        return UserRegistration.objects.all()

    def resolve_all_post(root, info):
        return post.objects.all()
        # for details in a:
        #     print(details.id)
        #     # print(details.tags)
        #     # print(details.title)
        #     # print(details.description)
        #     array2=[]
        #     for t in details.tags.all():
        #         array2.append(t)
        #     array = []
        #     finalData=ABC(
        #         post_id=details.id,
        #         title=details.title,
        #         description=details.description,
        #         tags=details.tags.all()
        #     )
        #     print(finalData)
        #     array.append(finalData)
        # a=array
        # return a


    def resolve_all_tag(root,info):
        return Tag.objects.all()

class UserRegistrationMutation(graphene.Mutation):
    class Arguments:
       username=graphene.String(required=True)
       email=graphene.String()

    user = graphene.Field(UserRegistrationType)
    success = graphene.Boolean()
    @classmethod
    def mutate(cls,root,info,username,email):
        user=UserRegistration(username=username,email=email)
        user.save()
        return UserRegistrationMutation(success=True)

class PostcreateMutation(graphene.Mutation):
    class Arguments:
       title=graphene.String(required=True)
       description=graphene.String()
       user_id = graphene.ID()

    success = graphene.Boolean()
    @classmethod
    def mutate(cls,root,info,title,description,user_id):

        user = UserRegistration.objects.get(id=user_id)
        postdata = post(
            user = user,
            title = title,
            description = description
        )
        postdata.save()

        return PostcreateMutation(success=True)


class UserUpdateMutation(graphene.Mutation):
    class Arguments:
       id = graphene.ID()
       username=graphene.String(required=True)
       email=graphene.String()

    user = graphene.Field(UserRegistrationType)
    success = graphene.Boolean()
    @classmethod
    def mutate(cls,root,info,username,email,id):

        # try:
        # except:
        #     raise Exception("User Dose Not Exist")
        user = UserRegistration.objects.get(id=id)

        user.username = username
        user.email = email
        user.save()
        return UserRegistrationMutation(success=True)

class UserDeleteMutation(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    delete=graphene.Field(UserRegistrationType)
    success = graphene.Boolean()
    @classmethod
    def mutate(cls,root,info,id):
        delete=UserRegistration.objects.get(id=id)
        delete.delete()
        return UserDeleteMutation(success=True)




class Mutation(graphene.ObjectType):
    create_user=UserRegistrationMutation.Field()
    update_user=UserUpdateMutation.Field()
    create_post = PostcreateMutation.Field()
    delete_user = UserDeleteMutation.Field()
schema=graphene.Schema(query=Query,mutation=Mutation)

 # 5 mins