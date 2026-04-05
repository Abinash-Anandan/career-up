from django.db import models
from Course.models import Course_Details
from Authentication.models import User_Details

class Student_Details(models.Model):
    user =models.OneToOneField(User_Details, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    enrollment_date = models.DateField()

    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)

    course = models.ForeignKey(Course_Details, on_delete=models.SET_NULL, null=True)   
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EnrollmentRequest(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    selected_path = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.selected_path}"
