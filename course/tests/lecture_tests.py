from rest_framework import status
from django.urls import include, path, reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, URLPatternsTestCase
from ..models import Lecture
from ..serializers import LectureSerializer


class LectureListTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json', './users/fixtures/users.json']

    def setUp(self):
        self.course_id = 1
        self.url = reverse('lecture-list', kwargs={'course_pk': self.course_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_list_lecture_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Lecture.objects.filter(course=self.course_id).count())

    def test_list_lecture_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Lecture.objects.filter(course=self.course_id).count())

    def test_list_lecture_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LectureReceiveTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json', './users/fixtures/users.json']

    def setUp(self):
        self.lecture = Lecture.objects.get(id=1)
        self.course_id = self.lecture.course.id
        self.url = reverse('lecture-detail', kwargs={'course_pk': self.course_id, 'pk': self.lecture.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_receive_lecture_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url, kwargs={'pk': self.lecture.id})
        lecture = Lecture.objects.get(id=1)
        serializer = LectureSerializer(lecture)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_lecture_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url, kwargs={'pk': self.lecture.id})
        lecture = Lecture.objects.get(id=1)
        serializer = LectureSerializer(lecture)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_lecture_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url, kwargs={'pk': self.lecture.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LectureUpdateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json', './users/fixtures/users.json']

    def setUp(self):
        self.lecture = Lecture.objects.get(id=1)
        self.course_id = self.lecture.course.id
        self.url = reverse('lecture-detail', kwargs={'course_pk': self.course_id, 'pk': self.lecture.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')
        self.data = {'name': 'Name changed'}

    def test_update_lecture_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.url, kwargs={'pk': self.lecture.id}, data=self.data)
        lecture = Lecture.objects.get(id=1)
        lecture.name = self.data['name']
        serializer = LectureSerializer(lecture)
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lecture_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.patch(self.url, kwargs={'pk': self.lecture.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lecture_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.patch(self.url, kwargs={'pk': self.lecture.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LectureDeleteTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json', './users/fixtures/users.json']

    def setUp(self):
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_delete_lecture_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('lecture-detail', kwargs={'course_pk': 1, 'pk': 1})
        response = self.client.delete(url, kwargs={'pk': 1})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lecture_with_student(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('lecture-detail', kwargs={'course_pk': 1, 'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lecture_with_anon_user(self):
        self.client.force_authenticate()
        url = reverse('lecture-detail', kwargs={'course_pk': 1, 'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
