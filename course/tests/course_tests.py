from django.urls import include, path, reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from ..models import Course
from ..serializers import CourseSerializer


class CourseCreateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]

    def setUp(self):
        self.url = reverse('course-list')
        self.user = User.objects.create_user(username='username', password='qwerty123-')
        self.data = {
            'name': 'Course 1',
            'slug': 'course_1',
            'description': 'qwertyuiop',
            'teachers': [],
            'students': []
        }

    def test_create_course_with_auth_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 7)

    def test_create_course_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseListTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './users/fixtures/users.json']

    def setUp(self):
        self.url = reverse('course-list')
        self.teacher = User.objects.get(username='ps')
        self.user = User.objects.get(username='admin')

    def test_list_course_with_auth_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        courses = (self.user.as_teacher.all() | self.user.as_student.all()).distinct()
        serializer = CourseSerializer(courses, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_course_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseReceiveTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './users/fixtures/users.json']

    def setUp(self):
        self.course = Course.objects.get(id=1)
        self.url = reverse('course-detail', kwargs={'pk': self.course.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_receive_course_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url, kwargs={'pk': self.course.id})
        course = Course.objects.get(id=1)
        serializer = CourseSerializer(course)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_course_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url, kwargs={'pk': self.course.id})
        course = Course.objects.get(id=1)
        serializer = CourseSerializer(course)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_course_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url, kwargs={'pk': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseUpdateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './users/fixtures/users.json']

    def setUp(self):
        self.course = Course.objects.get(id=1)
        self.url = reverse('course-detail', kwargs={'pk': self.course.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_update_course_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.url, kwargs={'pk': self.course.id}, data={'name': 'Name changed'})
        course = Course.objects.get(id=1)
        course.name = 'Name changed'
        serializer = CourseSerializer(course)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.patch(self.url, kwargs={'pk': self.course.id}, data={'name': 'Name changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.patch(self.url, kwargs={'pk': self.course.id}, data={'name': 'Name changed'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseDeleteTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './users/fixtures/users.json']

    def setUp(self):
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_delete_course_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        course = Course.objects.get(id=1)
        url = reverse('course-detail', kwargs={'pk': course.id})
        response = self.client.delete(url, kwargs={'pk': course.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_with_student(self):
        self.client.force_authenticate(user=self.student)
        course = Course.objects.get(id=2)
        url = reverse('course-detail', kwargs={'pk': course.id})
        response = self.client.delete(url, kwargs={'pk': course.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course_with_anon_user(self):
        self.client.force_authenticate()
        course = Course.objects.get(id=2)
        url = reverse('course-detail', kwargs={'pk': course.id})
        response = self.client.delete(url, kwargs={'pk': course.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
