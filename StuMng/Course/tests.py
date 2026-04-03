from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import Course_Details

User = get_user_model()


class CourseListViewTest(TestCase):

    def setUp(self):
        # Create a user (required for login_required)
        self.user = User.objects.create_user(
            username='student1',
            password='test123'
        )

        # Create sample courses
        self.course1 = Course_Details.objects.create(
            course_name="Python",
            course_fee=Decimal("10000.00"),
            course_duration=30
        )

        self.course2 = Course_Details.objects.create(
            course_name="Django",
            course_fee=Decimal("15000.00"),
            course_duration=45
        )

        # URL for course list
        self.url = reverse('course_list')

    def test_redirect_if_not_logged_in(self):
        """
        If user is NOT logged in,
        they should be redirected to login page
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_course_list_view_logged_in(self):
        """
        Logged-in user should access course list page
        """
        self.client.login(username='student1', password='test123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_correct_template_used(self):
        """
        Check correct template is rendered
        """
        self.client.login(username='student1', password='test123')
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'course_list.html')

    def test_courses_passed_in_context(self):
        """
        Check courses are passed to template context
        """
        self.client.login(username='student1', password='test123')
        response = self.client.get(self.url)

        self.assertIn('courses', response.context)
        self.assertEqual(len(response.context['courses']), 2)

    def test_course_content_display(self):
        """
        Check course data appears in response
        """
        self.client.login(username='student1', password='test123')
        response = self.client.get(self.url)

        self.assertContains(response, "Python")
        self.assertContains(response, "Django")
