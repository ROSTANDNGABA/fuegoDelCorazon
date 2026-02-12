from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.view_profile, name='view_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('user/<int:user_id>/', views.view_other_profile, name='view_other_profile'),
]
