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
    courses = Course_Details.objects.all()

    if request.method == "POST":
    
        if User_Details.objects.filter(username=request.POST['username']).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.', 'courses': courses})
        try:
            with transaction.atomic():              #commit or rollback

                # USER TABLE (saved only if everything passes)
                    user = User_Details.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password']
                        )

                    user.Mobiele_Number = request.POST.get('mobile')
                    user.Age = request.POST.get('age') or None
                    user.Address = request.POST.get('address')
                    user.State = request.POST.get('state')
                    user.Country = request.POST.get('country')
                    user.save()                                
                # STUDENT TABLE
                    selected_course = Course_Details.objects.get(id=request.POST['course'])
                    print(request.POST['course'], type(request.POST['course']))
                    print(selected_course.id,type(selected_course.id))
                    Student_Details.objects.create(
                        user=user,
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                        enrollment_date=request.POST['enrollment_date'],
                        course_id=selected_course.id,
                        course_fee=selected_course.course_fee,
                        paid_amount=request.POST['Paid_Fees'],
                        remaining_amount=selected_course.course_fee -Decimal(request.POST.get('Paid_Fees', '0')),
                        profile_picture=request.FILES.get('profile_picture'),
                        resume=request.FILES.get('resume')              
                    )

        # LOGIN ONLY AFTER SUCCESS
            return redirect('/')

        except Exception as e:
            print("Error occurred during signup.", e )
            
            return render(request, 'signup.html', {
                'error': 'Something went wrong. Please try again.',
                'courses': courses
            })


    return render(request, 'signup.html', {'courses': courses})
