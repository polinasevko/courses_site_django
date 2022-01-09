from django.urls import include, path, reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from ..models import Course


class TeachersReceiveTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './users/fixtures/users.json']

    def setUp(self):
        self.course = Course.objects.get(id=2)
        self.url = reverse('add-teacher', kwargs={'pk': self.course.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_receive_teachers_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url, kwargs={'pk': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_teachers_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url, kwargs={'pk': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_receive_teachers_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url, kwargs={'pk': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeachersUpdateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './users/fixtures/users.json']

    def setUp(self):
        self.course = Course.objects.get(id=2)
        self.url = reverse('add-teacher', kwargs={'pk': self.course.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')
        self.user = User.objects.get(username='additional')

    def test_update_teachers_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.url, kwargs={'pk': self.course.id}, data={'teachers': [self.user.id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_teachers_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.patch(self.url, kwargs={'pk': self.course.id}, data={'teachers': [self.user.id]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_teachers_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.patch(self.url, kwargs={'pk': self.course.id}, data={'teachers': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
