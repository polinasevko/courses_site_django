from django.urls import include, path, reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from ..models import Comment
from ..serializers import CommentSerializer


class CommentCreateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './course/fixtures/comment.json', './users/fixtures/users.json']

    def setUp(self):
        self.course_id = 1
        self.lecture_id = 1
        self.hometask_id = 1
        self.homework_id = 1
        self.url = reverse('comment-list', kwargs={'course_pk': self.course_id,
                                                   'lecture_pk': self.lecture_id,
                                                   'hometask_pk': self.hometask_id,
                                                   'homework_pk': self.homework_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_create_comment_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.url, data={'text': 'new comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(self.url, data={'text': 'new comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.post(self.url, data={'text': 'new comment'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentListTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './course/fixtures/comment.json', './users/fixtures/users.json']

    def setUp(self):
        self.course_id = 1
        self.lecture_id = 1
        self.hometask_id = 1
        self.homework_id = 1
        self.url = reverse('comment-list', kwargs={'course_pk': self.course_id,
                                                   'lecture_pk': self.lecture_id,
                                                   'hometask_pk': self.hometask_id,
                                                   'homework_pk': self.homework_id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_list_comment_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url)
        comments = Comment.objects.filter(homework=self.homework_id)
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_comment_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        comments = Comment.objects.filter(homework=self.homework_id)
        serializer = CommentSerializer(comments, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_comment_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentReceiveTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './course/fixtures/comment.json', './users/fixtures/users.json']

    def setUp(self):
        self.comment = Comment.objects.get(id=1)
        self.course_id = 1
        self.lecture_id = 1
        self.hometask_id = 1
        self.homework_id = 1
        self.url = reverse('comment-detail', kwargs={'course_pk': self.course_id,
                                                     'lecture_pk': self.lecture_id,
                                                     'hometask_pk': self.hometask_id,
                                                     'homework_pk': self.homework_id,
                                                     'pk': self.comment.id})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_receive_comment_with_teacher(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.url, kwargs={'pk': self.comment.id})
        serializer = CommentSerializer(self.comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_comment_with_student(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url, kwargs={'pk': self.comment.id})
        serializer = CommentSerializer(self.comment)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_receive_comment_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.get(self.url, kwargs={'pk': self.comment.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LectureUpdateTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './course/fixtures/comment.json', './users/fixtures/users.json']

    def setUp(self):
        self.comment = Comment.objects.get(id=2)
        self.url = reverse('comment-detail', kwargs={'course_pk': 1,
                                                     'lecture_pk': 1,
                                                     'hometask_pk': 1,
                                                     'homework_pk': 1,
                                                     'pk': 2})
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')
        self.data = {'text': 'Text changed'}

    def test_update_comment_with_owner(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.url, kwargs={'pk': self.comment.id}, data=self.data)
        comment = Comment.objects.get(id=2)
        comment.name = self.data['text']
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data['text'], serializer.data['text'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment_with_not_owner(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.patch(self.url, kwargs={'pk': self.comment.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_comment_with_anon_user(self):
        self.client.force_authenticate()
        response = self.client.patch(self.url, kwargs={'pk': self.comment.id}, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentDeleteTest(URLPatternsTestCase, APITestCase):
    urlpatterns = [
        path('', include('course.urls')),
    ]
    fixtures = ['./course/fixtures/course.json', './course/fixtures/lecture.json',
                './course/fixtures/hometask.json', './course/fixtures/homework.json',
                './course/fixtures/comment.json', './users/fixtures/users.json']

    def setUp(self):
        self.teacher = User.objects.get(username='ps')
        self.student = User.objects.get(username='admin')

    def test_delete_comment_with_owner(self):
        self.client.force_authenticate(user=self.teacher)
        url = reverse('comment-detail', kwargs={'course_pk': 1,
                                                'lecture_pk': 1,
                                                'hometask_pk': 1,
                                                'homework_pk': 1,
                                                'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_with_not_owner(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('comment-detail', kwargs={'course_pk': 1,
                                                'lecture_pk': 1,
                                                'hometask_pk': 1,
                                                'homework_pk': 1,
                                                'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_with_anon_user(self):
        self.client.force_authenticate()
        url = reverse('comment-detail', kwargs={'course_pk': 1,
                                                'lecture_pk': 1,
                                                'hometask_pk': 1,
                                                'homework_pk': 1,
                                                'pk': 2})
        response = self.client.delete(url, kwargs={'pk': 2})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
