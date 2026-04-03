from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from Authentication.models import User_Details
from Students.models import Student_Details
from Course.models import Course_Details
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

def Login_page(request):
    if request.method == 'POST':
        Check_user=authenticate(request,
                                username=request.POST.get('username'),
                                password=request.POST.get('password'))
        
        if Check_user is not None:
            login(request, Check_user)
            return redirect('student_home')
        else:
            return render(request, 'login.html', {'message': 'Incorrect Username or Password'})
    return render(request, 'login.html')

def social_login_redirect(request, provider):
    """Simulates a social login redirection and login process."""
    # Use existing test user or create a guest user
    username = f"guest_{provider}"
    user, created = User_Details.objects.get_or_create(username=username)
    if created:
        user.set_unusable_password()
        user.first_name = "Guest"
        user.last_name = provider.capitalize()
        user.save()
        
    # Ensure a student record exists for this guest (check every time in case it was missing)
    if not Student_Details.objects.filter(user=user).exists():
        default_course = Course_Details.objects.first()
        if default_course:
            Student_Details.objects.create(
                user=user,
                first_name="Guest",
                last_name=provider.capitalize(),
                email=f"guest_{provider}@example.com",
                course_id=default_course.id,
                course_fee=default_course.course_fee,
                paid_amount=0,
                remaining_amount=default_course.course_fee,
                enrollment_date=timezone.now().date()
            )

    # Explicitly set the backend for manual login
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('student_home')



def signup_view(request):
    try:
        courses = Course_Details.objects.all()
    except Exception as e:
        return render(request, 'signup.html', {
            'error': f'Database connection failed: {str(e)}',
            'courses': []
        })

    if request.method == "POST":
        try:
            if User_Details.objects.filter(username=request.POST.get('username', '')).exists():
                return render(request, 'signup.html', {'error': 'Username already exists.', 'courses': courses})

            with transaction.atomic():
                user = User_Details.objects.create_user(
                    username=request.POST.get('username', ''),
                    password=request.POST.get('password', '')
                )
                user.Mobiele_Number = request.POST.get('mobile')
                user.Age = request.POST.get('age') or None
                user.Address = request.POST.get('address')
                user.State = request.POST.get('state')
                user.Country = request.POST.get('country')
                user.save()

                course_val = request.POST.get('course')
                if course_val:
                    selected_course = Course_Details.objects.get(id=course_val)
                else:
                    selected_course = Course_Details.objects.first()

                # Step 1: Create student WITHOUT files first (guaranteed to work)
                student = Student_Details.objects.create(
                    user=user,
                    first_name=request.POST.get('first_name', ''),
                    last_name=request.POST.get('last_name', ''),
                    email=request.POST.get('email', ''),
                    enrollment_date=request.POST.get('enrollment_date') or timezone.now().date(),
                    course_id=selected_course.id,
                    course_fee=selected_course.course_fee,
                    paid_amount=request.POST.get('Paid_Fees', 0) or 0,
                    remaining_amount=selected_course.course_fee - Decimal(str(request.POST.get('Paid_Fees', 0) or 0)),
                )

            # Step 2: Try to attach files OUTSIDE the atomic block
            # If this fails, user is already saved — no crash
            try:
                import os
                os.makedirs('/tmp/media', exist_ok=True)
                profile_pic = request.FILES.get('profile_picture')
                resume_file = request.FILES.get('resume')
                if profile_pic or resume_file:
                    if profile_pic:
                        student.profile_picture = profile_pic
                    if resume_file:
                        student.resume = resume_file
                    student.save()
            except Exception:
                pass  # File upload failed silently — user is still registered

            return redirect('/')


        except Exception as e:
            import traceback
            err_detail = traceback.format_exc()
            print("Signup error:", err_detail)
            return render(request, 'signup.html', {
                'error': f'Registration failed: {str(e)}',
                'courses': courses
            })

    return render(request, 'signup.html', {'courses': courses})
