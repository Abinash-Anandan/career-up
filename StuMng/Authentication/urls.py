from django.urls import path
from Authentication import views

urlpatterns = [
    path('',views.Login_page,name='LoginPage'),
    path('signup/',views.signup_view,name='SignupPage'),
    path('social-login/<str:provider>/', views.social_login_redirect, name='SocialLogin'),
]
