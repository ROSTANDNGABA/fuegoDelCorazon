from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.questionnaire, name='questionnaire'),
    path('answers/', views.view_answers, name='view_answers'),
]
