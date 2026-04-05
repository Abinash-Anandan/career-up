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
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from Authentication.models import User_Details
from Students.models import Student_Details
from Course.models import Course_Details
from decimal import Decimal, InvalidOperation
from django.db import transaction, IntegrityError
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
        courses = list(Course_Details.objects.all())
    except Exception:
        courses = []

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # 1. Validation basics
        if not username or not password:
            return render(request, 'signup.html', {'error': 'Username and password are required.', 'courses': courses})

        # 2. Check duplicates explicitly to give clear messages
        if User_Details.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.', 'courses': courses})
        
        if email and Student_Details.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email is already registered.', 'courses': courses})

        try:
            # 3. Safe paid amount conversion
            try:
                paid_str = request.POST.get('Paid_Fees', '0') or '0'
                paid = Decimal(paid_str)
            except (InvalidOperation, ValueError):
                paid = Decimal('0.00')

            course_val = request.POST.get('course')

            with transaction.atomic():
                # Create user account
                user = User_Details.objects.create_user(username=username, password=password)
                user.Mobiele_Number = request.POST.get('mobile', '')
                user.Age = request.POST.get('age') or None
                user.Address = request.POST.get('address', '')
                user.save()

                # Get selected course safely
                selected_course = None
                if course_val:
                    try:
                        selected_course = Course_Details.objects.get(id=course_val)
                    except Course_Details.DoesNotExist:
                        pass
                
                if not selected_course:
                    selected_course = Course_Details.objects.first()

                # Basic defaults if NO courses exist at all
                course_id = selected_course.id if selected_course else None
                course_fee = selected_course.course_fee if selected_course else Decimal('0.00')

                # Create student record WITHOUT files first
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

            # 4. File uploads (OUTSIDE transaction)
            profile_pic = request.FILES.get('profile_picture')
            resume_file = request.FILES.get('resume')

            if profile_pic:
                try:
                    student.profile_picture = profile_pic
                    student.save(update_fields=['profile_picture'])
                except Exception as e:
                    print(f"Non-fatal profile pic error: {e}")

            if resume_file:
                try:
                    student.resume = resume_file
                    student.save(update_fields=['resume'])
                except Exception as e:
                    print(f"Non-fatal resume error: {e}")

            # Auto-login and go home
            login(request, user)
            return redirect('student_home')

        except IntegrityError as e:
            return render(request, 'signup.html', {'error': f'Database conflict: {str(e)}', 'courses': courses})
        except Exception as e:
            import traceback
            print("SIGNUP ERROR:", traceback.format_exc())
            return render(request, 'signup.html', {'error': f'Registration failed: {str(e)}', 'courses': courses})

    return render(request, 'signup.html', {'courses': courses})
