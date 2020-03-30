from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, QuizSerializer, QuestionSerializer, AnswersSerializer
from api.permissions import IsQuizOwnerOrReadOnly, CheckQuestionOwnerOrReadOnly, CheckAnswerOwnerOrReadOnly
from quizzes.models import Quizzes
from questions.models import Questions
from answers.models import Answers


class QuizViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user's quizzes to be viewed or edited.
    """
    queryset = Quizzes.objects.all().order_by('-id')
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated, IsQuizOwnerOrReadOnly]

    def get_queryset(self):
        return Quizzes.objects.filter(user=self.request.user).order_by('-id')


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows quiz's questions to be viewed or edited.
    """
    queryset = Questions.objects.all().order_by('-id')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, CheckQuestionOwnerOrReadOnly]

    def get_queryset(self):
        quiz = self.request.query_params.get('quiz', None)
        if quiz:
            return Questions.objects.filter(quiz__id=quiz, quiz__user=self.request.user).order_by('-id')
        return Questions.objects.all().order_by('-id')


class AnswersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows question's answer  to be viewed or edited.
    """
    queryset = Answers.objects.all().order_by('-id')
    serializer_class = AnswersSerializer
    permission_classes = [permissions.IsAuthenticated, CheckAnswerOwnerOrReadOnly]

    def get_queryset(self):
        question = self.request.query_params.get('question', None)
        if question:
            return Answers.objects.filter(question__id=question, question__quiz__user=self.request.user).order_by('-id')
        return Answers.objects.all().order_by('-id')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
