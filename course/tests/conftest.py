from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

from course.models import Course
from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def register_data():
    return {
        'username': 'username',
        'password': 'qwerty123-',
        'password2': 'qwerty123-',
        'email': 'username@gmail.com',
        'first_name': 'first',
        'last_name': 'last'
    }


@pytest.fixture
def user_data():
    return {
        'username': 'username',
        'password': 'qwerty123-'
    }


@pytest.fixture
def test_user(user_data):
    user = User.objects.create_user(**user_data)
    user.save()
    return user


@pytest.fixture
def authorized_user(api_client, test_user):
    client = api_client
    refresh = RefreshToken.for_user(test_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.fixture
def course_data(test_user):
    return {
        'name': 'Test course',
        'slug': 'course_1',
        'teachers': []
    }


@pytest.fixture
def course(test_user, course_data):
    course = baker.make(Course)
    course.teachers.add(test_user)
    return course
