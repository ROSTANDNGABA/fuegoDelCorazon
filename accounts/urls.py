from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(template_name='accounts/signup_simple.html'), name='signup'),
    path('create-profile/', views.create_profile, name='create_profile'),
]
