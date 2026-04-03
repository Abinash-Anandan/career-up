#testing ---> Models views urls Login Templates Forms

from django.test import TestCase, Client
from django.urls import reverse 
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',   
            password='testpass123'
        )

    def test_login_success(self):
        response = self.client.post(reverse('LoginPage'),
                                    {
                                      'username':'testuser',   
                                      'password':'testpass123'   
                                    }
                                    )
        self.assertEqual(response.status_code, 302)  # 400 -->success 200--> error  302 --> redirect
                        
    def test_login_failure(self):
        response = self.client.post(reverse('LoginPage'),
                                    {
                                      'username':'testuser',   
                                      'password':'testetesttest'   
                                    }
                                    )
        self.assertContains(response, 'Incorrect Username or Password')  