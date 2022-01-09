from django.urls import include, path, reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from ..models import Hometask
from ..serializers import HometaskSerializer


class HometaskCreateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './users/fixtures/users.json']

    def setUp(self):
        self.course_id = 1
        self.lecture_id = 1
        self.url = reverse('hometask-list', kwargs={'course_pk': self.course_id, 'lecture_pk': self.lecture_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_create_hometask_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.url, data={'text': 'new hometask'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 5)

    def test_create_hometask_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.post(self.url, data={'text': 'new hometask'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HometaskListTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './users/fixtures/users.json']

    def setUp(self):
        self.course_id = 1
        self.lecture_id = 1
        self.url = reverse('hometask-list', kwargs={'course_pk': self.course_id, 'lecture_pk': self.lecture_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_list_hometask_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        hometasks = Hometask.objects.filter(lecture=self.lecture_id)
        serializer = HometaskSerializer(hometasks, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_hometask_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        hometasks = Hometask.objects.filter(lecture=self.lecture_id)
        serializer = HometaskSerializer(hometasks, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_hometask_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HometaskReceiveTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './users/fixtures/users.json']

    def setUp(self):
        self.hometask = Hometask.objects.get(id=1)
        self.lecture_id = self.hometask.lecture.id
        self.course_id = self.hometask.lecture.course.id
        self.url = reverse('hometask-detail',  kwargs={'course_pk': self.course_id, 'lecture_pk': self.lecture_id, 'pk': self.hometask.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_receive_hometask_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url, kwargs={'pk': self.hometask.id})
        serializer = HometaskSerializer(self.hometask)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_hometask_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url, kwargs={'pk': self.hometask.id})
        serializer = HometaskSerializer(self.hometask)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_hometask_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url, kwargs={'pk': self.hometask.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LectureUpdateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './users/fixtures/users.json']

    def setUp(self):
        self.hometask = Hometask.objects.get(id=1)
        self.lecture_id = self.hometask.lecture.id
        self.course_id = self.hometask.lecture.course.id
        self.url = reverse('hometask-detail',  kwargs={'course_pk': self.course_id, 'lecture_pk': self.lecture_id, 'pk': self.hometask.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')
        self.data = {'text': 'Text changed'}

    def test_update_hometask_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.url, kwargs={'pk': self.hometask.id}, data=self.data)
        hometask = Hometask.objects.get(id=1)
        hometask.name = self.data['text']
        serializer = HometaskSerializer(hometask)
        self.assertEqual(response.data['text'], serializer.data['text'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hometask_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.patch(self.url, kwargs={'pk': self.hometask.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_hometask_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.patch(self.url, kwargs={'pk': self.hometask.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class HometaskDeleteTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './users/fixtures/users.json']

    def setUp(self):
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_delete_hometask_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('hometask-detail', kwargs={'course_pk': 1, 'lecture_pk': 1, 'pk': 1})
        response = self.client.delete(url, kwargs={'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_hometask_with_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('hometask-detail', kwargs={'course_pk': 1, 'lecture_pk': 1, 'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hometask_with_anon_user(self):
        self.client.force_authenticate()
        url = reverse('hometask-detail', kwargs={'course_pk': 1, 'lecture_pk': 1, 'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
