from django.db import models

class Course_Details(models.Model):
    course_name = models.CharField(max_length=100)
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)       
    course_duration = models.IntegerField(help_text="Duration in days") 
    
    def __str__(self):
        return self.course_name