import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from Course.models import Course_Details

new_courses = [
    {"name": "Python Full Stack", "fee": 45000, "duration": 180},
    {"name": "Java Full Stack", "fee": 50000, "duration": 210},
    {"name": "MERN Full Stack", "fee": 48000, "duration": 150},
]

for c in new_courses:
    # Use update_or_create to ensure everything matches
    course, created = Course_Details.objects.get_or_create(
        course_name=c["name"],
        defaults={"course_fee": c["fee"], "course_duration": c["duration"]}
    )
    if created:
        print(f"Created: {c['name']}")
    else:
        print(f"Exists: {c['name']}")
