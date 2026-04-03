import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from Course.models import Course_Details

# Find and delete the generic "full stack" course
target_name = "full stack"
courses_to_delete = Course_Details.objects.filter(course_name__iexact=target_name)

if courses_to_delete.exists():
    for c in courses_to_delete:
        print(f"Deleting: {c.course_name} (ID: {c.id})")
        c.delete()
else:
    print(f"No course found with name '{target_name}'")

# List remaining courses to confirm
print("\nRemaining Courses:")
for c in Course_Details.objects.all():
    print(f"- {c.course_name}")
