import requests
import os
import random

url = "https://career-up-gamma.vercel.app/signup/"
# Use the real generated image from before
image_path = r"C:\Users\ABINASH\.gemini\antigravity\brain\bf5e23d8-de5f-441c-bdbb-d3abacca1819\verify_upload_jpg_1775398815295.png"
# Create a valid tiny PDF
pdf_path = "test_resume_real.pdf"
with open(pdf_path, "wb") as f:
    f.write(b"%PDF-1.1\n% \n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF")

rand_id = random.randint(1000, 9999)
username = f"full_test_user_{rand_id}"
email = f"full_test_{rand_id}@example.com"

print(f"Testing with User: {username}, Email: {email}")

session = requests.Session()
# 1. Get CSRF
try:
    r = session.get(url, timeout=15)
    csrf_token = session.cookies.get('csrftoken', '')
    print(f"CSRF Token: {csrf_token[:10]}...")
except Exception as e:
    print(f"Failed to reach site: {e}")
    exit(1)

data = {
    'csrfmiddlewaretoken': csrf_token,
    'username': username,
    'password': 'Password123!',
    'first_name': 'Full',
    'last_name': 'Tester',
    'email': email,
    'mobile': '1234567890',
    'age': '30',
    'address': 'Testing Lane',
    'Paid_Fees': '2000',
    'enrollment_date': '2026-04-05'
}

files = {
    'profile_image': ('profile.png', open(image_path, 'rb'), 'image/png'),
    'resume': ('resume.pdf', open(pdf_path, 'rb'), 'application/pdf'),
}

print("Poking the live server with a full upload...")
try:
    response = session.post(url, data=data, files=files, headers={'Referer': url}, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    
    if "Registration failed" in response.text:
        print(">>> SERVER RETURNED REGISTRATION FAILED MESSAGE")
        # Extract error message
        start = response.text.find('Registration failed')
        print(response.text[start:start+100])
    elif response.status_code == 504:
        print(">>> GATEWAY TIMEOUT (504) - Cloudinary response took too long!")
    elif response.status_code == 500:
        print(">>> INTERNAL SERVER ERROR (500)")
    else:
        print(">>> SUCCESS (Likely). Redirected URL:", response.url)
except requests.exceptions.Timeout:
    print(">>> REQUEST TIMED OUT (Local Timeout hit)")
except Exception as e:
    print(f">>> EXCEPTION: {e}")
