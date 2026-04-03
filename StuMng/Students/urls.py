from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', student_home, name='student_home'),
    path('personal-info/', personal_info, name='personal_info'),
    path('courses/', course_list, name='course_list'),
    path('logout/', logout_view, name='logout'),
    path('submit-enrollment/', submit_enrollment, name='submit_enrollment'),
]
