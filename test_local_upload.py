import requests
import random
import os

url = "http://127.0.0.1:8000/signup/"

try:
    session = requests.Session()
    r = session.get(url)
    csrf_token = session.cookies['csrftoken']
    print(f"Got CSRF token: {csrf_token}")

    username = f"test_{random.randint(1000, 9999)}"

    data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': 'Password123!',
        'first_name': 'Local',
        'last_name': 'Tester',
        'email': f'{username}@example.com',
        'mobile': '0000000000',
        'age': '20',
        'address': 'Test Local Address',
        'Paid_Fees': '1000',
        'enrollment_date': '2026-04-05'
    }

    # Upload files with specific content types to pass validation
    files = {
        'profile_image': ('dummy.jpg', open('dummy.jpg', 'rb'), 'image/jpeg'),
        'resume': ('dummy.pdf', open('dummy.pdf', 'rb'), 'application/pdf')
    }

    response = session.post(url, data=data, files=files, headers={'Referer': url})

    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    
    if "error-msg" in response.text:
        print("Registration FAILED. Error found in response.")
        for line in response.text.split('\n'):
            if 'error-msg' in line:
                print(line.strip())
    elif response.url == 'http://127.0.0.1:8000/students/home/': # student_home url
        print("Registration SUCCESSFUL. Redirected to student dashboard.")
    else:
        print("Registration MIGHT have failed. Check DB.")
        
except Exception as e:
    print(f"Test failed: {e}")
