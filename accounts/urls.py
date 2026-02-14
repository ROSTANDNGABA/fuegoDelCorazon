from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login_simple.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(template_name='accounts/signup_simple.html'), name='signup'),
    path('create-profile/', views.create_profile, name='create_profile'),
]
