import requests
import os
import random

url = "https://career-up-gamma.vercel.app/signup/"
image_path = r"C:\Users\ABINASH\OneDrive\Desktop\aaaaa\hrh (1 of 1).jpg"
pdf_path = r"C:\Users\ABINASH\OneDrive\Desktop\HTML\javascript_tutorial.pdf"

rand_id = random.randint(10000, 99999)
username = f"live_test_{rand_id}"
email = f"live_test_{rand_id}@example.com"

print(f"Testing real user upload: {username}")

session = requests.Session()
# CSRF first
session.get(url, timeout=20)
csrf_token = session.cookies.get('csrftoken', '')

data = {
    'csrfmiddlewaretoken': csrf_token,
    'username': username,
    'password': 'Password123!',
    'first_name': 'Live',
    'last_name': 'Test',
    'email': email,
    'mobile': '0000000000',
    'age': '22',
    'address': 'Desktop Path Test',
    'Paid_Fees': '2000',
    'enrollment_date': '2026-04-05',
    'course': '1'
}

files = {
    'profile_picture': open(image_path, 'rb'),
    'resume': open(pdf_path, 'rb'),
}

# Add Referer (Django CSRF checks it)
headers = {'Referer': url}

print("Poking the live site with real files from your disk...")
response = session.post(url, data=data, files=files, headers=headers, timeout=60)

print(f"Status Code: {response.status_code}")
print(f"Final URL: {response.url}")

if response.status_code == 413:
    print(">>> FAILED: Request Body Too Large (Vercel Limit hit). Try smaller files!")
elif "Registration failed" in response.text:
    print(">>> FAILED: Server-side registration error.")
elif response.url.endswith('/students/home/') or response.url.endswith('/'):
    print(">>> SUCCESS! User created and redirected.")
else:
    print(">>> RE-VERIFY: Signup result unknown. Response text length:", len(response.text))
