from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'quizzes', views.QuizViewSet)
router.register(r'answers', views.AnswersViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = [
    path('', include(router.urls))
]