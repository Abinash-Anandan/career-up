from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Students.models import Student_Details
from Course.models import Course_Details
from django.contrib.auth import logout

@login_required
def student_home(request):
    return render(request, 'student_home.html')


@login_required
def personal_info(request):
    student, created = Student_Details.objects.get_or_create(user=request.user)
    if created:
        # Give some default values if it was just created
        student.first_name = request.user.username.capitalize()
        student.email = request.user.email or f"{request.user.username}@careerup.com"
        student.course_fee = 0.00
        student.enrollment_date = "2026-04-03" # default date
        student.save()
    return render(request, 'personal_info.html', {'student': student})


@login_required
def course_list(request):
    courses = Course_Details.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')   # redirect to login page
from django.http import JsonResponse
from .models import EnrollmentRequest

@login_required
def submit_enrollment(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        path = request.POST.get('path')
        
        if full_name and email and phone:
            EnrollmentRequest.objects.create(
                full_name=full_name,
                email=email,
                phone_number=phone,
                selected_path=path
            )
            return JsonResponse({'status': 'success', 'message': 'Application received! Expert advisors will contact you soon.'})
        return JsonResponse({'status': 'error', 'message': 'Missing required fields.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
