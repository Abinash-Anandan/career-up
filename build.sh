#!/bin/bash

echo "🚀 Building Career Up Platform..."

# Install dependencies
python3 -m pip install -r requirements.txt

# Run migrations to setup Neon tables
python3 manage.py migrate --noinput

# Seed Courses
python3 manage.py shell -c "import add_courses"

# Create Initial Admin User (abishek / 12345)
python3 manage.py shell -c "from Authentication.models import User_Details; from django.contrib.auth.hashers import make_password; User_Details.objects.get_or_create(username='abishek', defaults={'password': make_password('12345'), 'is_staff': True, 'is_superuser': True})"

echo "✅ Build & Database Setup Complete!"
