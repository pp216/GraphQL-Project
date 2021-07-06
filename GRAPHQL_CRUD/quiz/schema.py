import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from .models import Quizzes,Category,Question,Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        fields=("id","name")



class QuizzesType(DjangoObjectType):
    class Meta:
        model=Quizzes
        fields=("id","title","quiz","category")


class QuestionType(DjangoObjectType):
    class Meta:
        model=Question
        fields=("title","quiz")



class AnswerType(DjangoObjectType):
    class Meta:
        model=Answer
        fields=("question","answer_text")

class Query(graphene.ObjectType):

    all_quizzes=graphene.Field(QuizzesType,id=graphene.Int())
    all_questions=graphene.Field(QuestionType,id=graphene.Int())
    all_answers=graphene.List(AnswerType,id=graphene.Int())
    def resolve_all_quizzes(root,info,id):
        return Quizzes.objects.get(pk=id)

    def resolve_all_questions(root,info,id):
        return Question.objects.get(pk=id)
    def resolve_all_answers(root,info,id):
        return Answer.objects.filter(question=id)

#------------------------------------------------------------------
#Create Data
#-----------------------------------------------------------------
# class CategoryMutation(graphene.Mutation):
#     class Arguments:
#         name=graphene.String(required=True)
#
#     category = graphene.Field(CategoryType)
#
#     @classmethod
#     def mutate(cls,root,info,name):
#         category=Category(name=name)
#         category.save()
#         return CategoryMutation(category=category)
#
#
# class Mutation(graphene.ObjectType):
#     update_category=CategoryMutation.Field()

#______________________________________________________________________________
#______________________________________________________________________________

#________________________________________________________________________________
# Update Data


# class CategoryMutation(graphene.Mutation):
#     class Arguments:
#         id=graphene.ID()
#         name=graphene.String(required=True)
#     category = graphene.Field((CategoryType))
#
#     @classmethod
#     def mutate(cls,root,info,name,id):
#         category=Category.objects.get(id=id)
#         category.name=name
#         category.save()
#         return CategoryMutation(category=category)
#
#
#
# class Mutation (graphene.ObjectType):
#     update_category=CategoryMutation.Field()

#________________________________________________________________________________
#_________________________________________________________________________________


#__________________________________________________________________________________
#Delete  Data

class CategoryMutation(graphene.Mutation):
    class Arguments:
        id=graphene.ID()

    category = graphene.Field((CategoryType))

    @classmethod
    def mutate(cls,root,info,id):
        category=Category.objects.get(id=id)
        category.delete()
        return



class Mutation (graphene.ObjectType):
    update_category=CategoryMutation.Field()

#____________________________________________________________________________
schema=graphene.Schema(query=Query,mutation=Mutation)