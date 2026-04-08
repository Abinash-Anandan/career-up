import requests
import random
import os
import time

url = "https://career-up-gamma.vercel.app/signup/"

print("Waiting a bit for Vercel deploy...")
time.sleep(10)

try:
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    r = session.get(url)
    csrf_token = session.cookies['csrftoken']
    print(f"Got CSRF token: {csrf_token}")

    username = f"live_tester_{random.randint(1000, 9999)}"

    data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': 'Password123!',
        'first_name': 'Live',
        'last_name': 'Tester',
        'email': f'{username}@example.com',
        'mobile': '0000000000',
        'age': '20',
        'address': 'Test Live Address',
        'Paid_Fees': '1000',
        'enrollment_date': '2026-04-05'
    }

    files = {
        'profile_image': ('dummy.jpg', open('dummy.jpg', 'rb'), 'image/jpeg'),
        'resume': ('dummy.pdf', open('dummy.pdf', 'rb'), 'application/pdf')
    }

    print("Uploading to live server...")
    response = session.post(url, data=data, files=files, headers={'Referer': url})

    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    
    if "error-msg" in response.text:
        print("Registration FAILED. Error found in response.")
        for line in response.text.split('\n'):
            if 'error-msg' in line:
                print(line.strip())
    elif 'students/home/' in response.url:
        print("Registration SUCCESSFUL. Redirected to student dashboard.")
    else:
        print("Registration MIGHT have failed. Check response text.")
        if "500 Internal Server Error" in response.text:
             print("Hit a 500 error :(")
        
except Exception as e:
    print(f"Test failed: {e}")
