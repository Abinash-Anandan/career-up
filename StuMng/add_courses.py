import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from Course.models import Course_Details

new_courses = [
    {"name": "Python Full Stack", "fee": 14999, "duration": 180},
    {"name": "Java Specialized", "fee": 12499, "duration": 210},
    {"name": "MERN Stack Hub", "fee": 11999, "duration": 150},
    {"name": "Deep Learning & AI", "fee": 15999, "duration": 240},
    {"name": "Data Analytics Elite", "fee": 9999, "duration": 120},
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
