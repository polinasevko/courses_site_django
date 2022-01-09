from django.urls import include, path, reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from ..models import Homework
from ..serializers import HomeworkSerializer


class HomeworkListTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './users/fixtures/users.json']

    def setUp(self):
        self.course_id = 1
        self.lecture_id = 1
        self.hometask_id = 1
        self.url = reverse('homework-list', kwargs={'course_pk': self.course_id,
                                                    'lecture_pk': self.lecture_id,
                                                    'hometask_pk': self.hometask_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_list_homework_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Homework.objects.filter(hometask=self.hometask_id).count())

    def test_list_homework_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),
                         Homework.objects.filter(hometask=self.hometask_id, student=self.student).count())

    def test_list_homework_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HomeworkReceiveTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './users/fixtures/users.json']

    def setUp(self):
        self.homework = Homework.objects.get(id=1)
        self.course_id = 1
        self.lecture_id = 1
        self.hometask_id = 1
        self.url = reverse('homework-list', kwargs={'course_pk': self.course_id,
                                                    'lecture_pk': self.lecture_id,
                                                    'hometask_pk': self.hometask_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_receive_homework_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url, kwargs={'pk': self.homework.id})
        homework = Homework.objects.get(id=1)
        serializer = HomeworkSerializer(homework)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_homework_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url, kwargs={'pk': self.homework.id})
        homework = Homework.objects.get(id=1)
        serializer = HomeworkSerializer(homework)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_homework_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url, kwargs={'pk': self.homework.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HomeworkSetMarkTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './users/fixtures/users.json']

    def setUp(self):
        self.homework = Homework.objects.get(id=1)
        self.course_id = 1
        self.lecture_id = 1
        self.hometask_id = 1
        self.url = reverse('homework-mark', kwargs={'course_pk': self.course_id,
                                                    'lecture_pk': self.lecture_id,
                                                    'hometask_pk': self.hometask_id,
                                                    'pk': self.homework.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')
        self.data = {'mark': '8'}

    def test_set_mark_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.put(self.url, kwargs={'pk': self.homework.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_homework_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.put(self.url, kwargs={'pk': self.homework.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_homework_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.patch(self.url, kwargs={'pk': self.homework.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HomeworkDeleteTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './users/fixtures/users.json']

    def setUp(self):
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_delete_homework_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('homework-detail', kwargs={'course_pk': 1, 'lecture_pk': 1, 'hometask_pk': 1, 'pk': 1})
        response = self.client.delete(url, kwargs={'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_homework_with_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('homework-detail', kwargs={'course_pk': 1, 'lecture_pk': 1, 'hometask_pk': 1, 'pk': 1})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_homework_with_anon_user(self):
        self.client.force_authenticate()
        url = reverse('homework-detail', kwargs={'course_pk': 1, 'lecture_pk': 1, 'hometask_pk': 1, 'pk': 1})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
