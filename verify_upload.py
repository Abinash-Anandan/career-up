import requests
import os

url = "https://career-up-gamma.vercel.app/signup/"
image_path = r"C:\Users\ABINASH\.gemini\antigravity\brain\bf5e23d8-de5f-441c-bdbb-d3abacca1819\verify_upload_jpg_1775398815295.png"

# We need CSRF token first
session = requests.Session()
r = session.get(url)
csrf_token = session.cookies['csrftoken']

data = {
    'csrfmiddlewaretoken': csrf_token,
    'username': 'upload_test_user_777',
    'password': 'Password123!',
    'first_name': 'Upload',
    'last_name': 'Tester',
    'email': 'uploadtest777@example.com',
    'mobile': '0000000000',
    'age': '20',
    'address': 'Test Address',
    'Paid_Fees': '1000',
    'enrollment_date': '2026-04-05'
}

files = {
    'profile_picture': open(image_path, 'rb'),
}

response = session.post(url, data=data, files=files, headers={'Referer': url})

print(f"Status Code: {response.status_code}")
print(f"Final URL: {response.url}")
if "Registration failed" in response.text:
    print("Registration FAILED.")
    # Look for error message
    if 'error-msg' in response.text:
        print("Error content detected.")
else:
    print("Registration seems SUCCESSFUL (or at least no failure message).")
