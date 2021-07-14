import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth.schema import UserQuery,MeQuery
from graphql_auth import mutations

from app.models import Post, Tag, User

class TagInput(graphene.InputObjectType):
    name=graphene.String()

class UserType(DjangoObjectType):
    class Meta:
        model=User

class postType(DjangoObjectType):
    class Meta:
        model=Post
        #fields=("user","title"," description")
        # filter_fields=['title']
class TagType(DjangoObjectType):
    class Meta:
        model=Tag


class Query(UserQuery,MeQuery,graphene.ObjectType):
    user_by_id = graphene.Field(UserType, id=graphene.ID())
    post_by_id = graphene.Field(postType, id=graphene.ID())
    all_post = graphene.List(postType)
    all_users = graphene.List(UserType)
    all_tag = graphene.List(TagType)
    by_title =  graphene.Field(postType, title=graphene.String())
    by_tags = graphene.Field(TagType,name=graphene.String())

    def resolve_post_by_id(root,info,id):
        return Post.objects.get(id=id)

    def resolve_user_by_id(root,info,id):
        return User.objects.get(id=id)

    def resolve_all_users(root,info):
        return User.objects.all()
    def resolve_all_post(root, info):
        return Post.objects.all()

    def resolve_all_tag(root,info):
        return Tag.objects.all()

    def resolve_by_title(root,info,title):
        return Post.objects.get(title=title)

    def resolve_by_tags(root,info,name):
        return Tag.objects.get(name=name)


class PostcreateMutation(graphene.Mutation):
    class Arguments:
       title=graphene.String(required=True)
       description=graphene.String()
       user_id = graphene.ID()
       tags = graphene.List(TagInput)

    success = graphene.Boolean()
    postdata=graphene.Field(postType)
    @classmethod
    def mutate(cls,root,info,title,description,user_id,tags):

        user = User.objects.get(id=user_id)
        postdata = Post(

            title = title,
            description = description,
            user_id = user_id,
        )
        postdata.save()
        for data in tags:
            tagdata=Tag(name=data.name)
            tagdata.save()
            postdata.tags.add(tagdata)
        postdata.save()
        return PostcreateMutation(success=True,postdata=postdata)

class TagMutation(graphene.Mutation):
    class Arguments:
        name=graphene.String()

    success=graphene.Boolean()

    @classmethod
    def mutate(cls,root,info,name):
        tagdata=Tag(name=name)
        tagdata.save()
        return  TagMutation(success=True)

class PostUpdateMutation(graphene.Mutation):
    class Arguments:
       user_id = graphene.ID()
       title=graphene.String()
       description = graphene.String()

    #post = graphene.Field(postType)
    success = graphene.Boolean()
    @classmethod
    def mutate(cls,root,info,user_id,title,description):


        postid = Post.objects.get(id=user_id)

        postid.title = title
        postid.description = description
        postid.save()
        return PostUpdateMutation(success=True)


class PostDeleteMutation(graphene.Mutation):
    class Arguments:
        user_id=graphene.ID()

    delete=graphene.Field(postType)
    success = graphene.Boolean()
    @classmethod
    def mutate(cls,root,info,user_id):
        delete=User.objects.get(id=user_id)
        delete.delete()
        return PostDeleteMutation(success=True)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

class Mutation(AuthMutation, graphene.ObjectType):
    create_post = PostcreateMutation.Field()
    create_tag = TagMutation.Field()
    update_post = PostUpdateMutation.Field()
    delete_post = PostDeleteMutation.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
