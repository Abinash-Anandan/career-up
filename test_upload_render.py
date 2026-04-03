import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
import random
import io

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

opener.open('https://career-up-xgxo.onrender.com/signup/')
csrf_token = next((c.value for c in cj if c.name == 'csrftoken'), '')
test_user = 'sealtester_' + str(random.randint(1000, 9999))

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = []

def add_field(name, value):
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n')

def add_file(name, filename, content):
    body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{filename}"\r\nContent-Type: image/jpeg\r\n\r\n{content}\r\n')

add_field('csrfmiddlewaretoken', csrf_token)
add_field('username', test_user)
add_field('password', 'password123')
add_field('first_name', 'Test')
add_field('last_name', 'User')
add_field('email', f'{test_user}@test.com')
add_field('course', '1')
add_field('Paid_Fees', '5000')
add_field('enrollment_date', '2026-04-03')
add_file('profile_picture', 'test.jpg', 'fake image data')

body.append(f'--{boundary}--\r\n')
data = ''.join(body).encode('utf-8')

req = urllib.request.Request('https://career-up-xgxo.onrender.com/signup/', data=data)
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
req.add_header('Referer', 'https://career-up-xgxo.onrender.com/signup/')

try:
    response = opener.open(req)
    html = response.read().decode('utf-8')
    if 'error-msg' in html:
        print('FORM RENDERED ERROR:')
        for line in html.split('\n'):
             if 'error-msg' in line or 'alert' in line or 'wrong' in line or 'Error details' in line:
                  print(line.strip())
    else:
        print('SUCCESS:', response.url)
except Exception as e:
    print('EXCEPTION DURING POST:', e)
    if hasattr(e, 'read'):
        try:
           print(e.read().decode('utf-8'))
        except:
           pass
