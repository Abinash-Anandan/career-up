from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import logging
import traceback

from Authentication.models import User_Details
from Students.models import Student_Details
from Course.models import Course_Details

logger = logging.getLogger(__name__)

def Login_page(request):
    if request.method == 'POST':
        Check_user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        
        if Check_user is not None:
            login(request, Check_user)
            return redirect('student_home')
        else:
            return render(request, 'login.html', {'message': 'Incorrect Username or Password'})
    return render(request, 'login.html')

def social_login_redirect(request, provider):
    """Simulates a social login redirection and login process."""
    username = f"guest_{provider}"
    user, created = User_Details.objects.get_or_create(username=username)
    if created:
        user.set_unusable_password()
        user.first_name = "Guest"
        user.last_name = provider.capitalize()
        user.save()
        
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

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('student_home')

def signup_view(request):
    try:
        courses = list(Course_Details.objects.all())
    except Exception:
        courses = []

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'signup.html', {'error': 'Username and password are required.', 'courses': courses})

        if User_Details.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.', 'courses': courses})
        
        if email and Student_Details.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email is already registered.', 'courses': courses})

        try:
            try:
                paid_str = request.POST.get('Paid_Fees', '0') or '0'
                paid = Decimal(paid_str)
            except (InvalidOperation, ValueError):
                paid = Decimal('0.00')

            course_val = request.POST.get('course')

            profile_image = request.FILES.get('profile_image') or request.FILES.get('profile_picture')
            resume_file = request.FILES.get('resume')

            # --- VERCEL PAYLOAD OPTIMIZATION ---
            # Limit file size BEFORE processing to avoid 413 Payload Too Large OR function timeouts
            MAX_UPLOAD_SIZE = 3 * 1024 * 1024  # 3MB
            if profile_image and profile_image.size > MAX_UPLOAD_SIZE:
                 return render(request, 'signup.html', {'error': 'Profile image exceeds 3MB limit.', 'courses': courses})
            if resume_file and resume_file.size > MAX_UPLOAD_SIZE:
                 return render(request, 'signup.html', {'error': 'Resume exceeds 3MB limit.', 'courses': courses})

            with transaction.atomic():
                user = User_Details.objects.create_user(username=username, password=password)
                user.Mobiele_Number = request.POST.get('mobile', '')
                user.Age = request.POST.get('age') or None
                user.Address = request.POST.get('address', '')
                user.save()

                selected_course = None
                if course_val:
                    try:
                        selected_course = Course_Details.objects.get(id=course_val)
                    except Course_Details.DoesNotExist:
                        pass
                
                if not selected_course:
                    selected_course = Course_Details.objects.first()

                course_id = selected_course.id if selected_course else None
                course_fee = selected_course.course_fee if selected_course else Decimal('0.00')

                student = Student_Details.objects.create(
                    user=user,
                    first_name=request.POST.get('first_name', ''),
                    last_name=request.POST.get('last_name', ''),
                    email=email,
                    enrollment_date=request.POST.get('enrollment_date') or timezone.now().date(),
                    course_id=course_id,
                    course_fee=course_fee,
                    paid_amount=paid,
                    remaining_amount=course_fee - paid,
                )

            if profile_image or resume_file:
                # 1. First attempt to save profile image
                if profile_image:
                    try:
                        student.profile_image = profile_image
                        student.save(update_fields=['profile_image'])
                        logger.info(f"Profile image uploaded successfully for user {username}")
                    except Exception as e:
                        logger.error(f"PROFILE IMAGE UPLOAD FAILED for {username}: {str(e)}")
                
                # 2. Then attempt to save resume independently
                if resume_file:
                    try:
                        student.resume = resume_file
                        student.save(update_fields=['resume'])
                        logger.info(f"Resume uploaded successfully for user {username}")
                    except Exception as e:
                        logger.error(f"RESUME UPLOAD FAILED for {username}: {str(e)}")

            login(request, user)
            return redirect('student_home')

        except IntegrityError as e:
            return render(request, 'signup.html', {'error': f'Database conflict: {str(e)}', 'courses': courses})
        except Exception as e:
            logger.error(f"Registration crash: {str(e)}")
            logger.error(traceback.format_exc())
            return render(request, 'signup.html', {'error': f'Registration failed (v5.2): {str(e)}', 'courses': courses})

    return render(request, 'signup.html', {'courses': courses})

def Logout_Page(request):
    logout(request)
    return redirect('LoginPage')
