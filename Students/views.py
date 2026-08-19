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

import json
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            if not user_message:
                return JsonResponse({'status': 'error', 'message': 'No message provided.'})

            client = OpenAI(
              base_url = "https://integrate.api.nvidia.com/v1",
              api_key = "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"
            )

            system_prompt = """You are CORTEX AI, the official career assistant for 'Career Up' (StuMng_Proj).
Your job is to answer student queries about our platform, courses, fees, and enrollment.
Always keep your answers concise, friendly, and professional. Use emojis where appropriate.

Here is the key information about Career Up:
- **Contact:** Students can speak to Abinash directly at +91 6379580730 for a professional career audit.
- **Mentorship:** We provide 1-to-1 weekly mentorship with experts from Google, AWS, and Netflix.
- **Enrollment:** Enrollment is open. Students can click 'Enroll' on any course card, and our managers will contact them within 2 hours.
- **Payment:** EMI options are available for all courses.

**Available Courses & Fees:**
- Java: ₹35,000 (160 days)
- Python: ₹30,000 (120 days)
- Django: ₹10,000 (90 days)
- Python Full Stack: ₹45,000 (180 days)
- Java Full Stack: ₹50,000 (210 days)
- MERN Full Stack: ₹48,000 (150 days)

**Platform Features (Hubs):**
- Alumni Hub: Join 15,000+ graduates in our exclusive career-referral ecosystem.
- Elite Dashboard: Real-time certification and outcome tracking.
- Peak Roadmap: AI-optimized curriculum path for 2024 tech requirements.
- Certificate Vault: Access and verify professional industrial certifications.
- Resource Library: Comprehensive repository of code, assets, and study materials.
- Exam Center: Schedule and take professional competency assessments.

Never make up information. If a question is outside this scope, let them know you are forwarding their inquiry to our expert advisors."""

            completion = client.chat.completions.create(
              model="meta/llama-3.1-8b-instruct",
              messages=[
                  {"role":"system", "content": system_prompt},
                  {"role":"user","content":user_message}
              ],
              temperature=1,
              top_p=1,
              max_tokens=4096,
              stream=False,
              timeout=15.0 # Add timeout to prevent hanging
            )

            response_content = ""
            reasoning = getattr(completion.choices[0].message, "reasoning_content", None)
            if reasoning:
                response_content += f"🤔 **Reasoning:**\n{reasoning}\n\n---\n\n"
            
            response_content += completion.choices[0].message.content or ""
            
            return JsonResponse({'status': 'success', 'message': response_content})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})