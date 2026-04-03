from django.contrib import admin
from Authentication.models import User_Details
from Students.models import Student_Details
from Course.models import Course_Details    

admin.site.register(User_Details)
admin.site.register(Student_Details)
admin.site.register(Course_Details)



admin.site.site_header = "Career Up Administration"
admin.site.site_title = "Career Up Admin"
admin.site.index_title = "Welcome to Career Up Dashboard"