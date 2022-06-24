from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
import pytest
from course.models import Course


@pytest.mark.django_db
class TestRegistration:

    url = reverse('register')

    def test_account_creation(self, api_client, register_data):
        response = api_client.post(self.url, data=register_data, format='json')
        assert response.status_code == 201
        assert response.data['username'] == register_data['username']


@pytest.mark.django_db
class TestLogin:

    url = reverse('token_obtain_pair')

    def test_login_account(self, api_client, user_data, test_user):
        response = api_client.post(self.url, data=user_data, format="json")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRefresh:

    access_url = reverse('token_obtain_pair')
    refresh_url = reverse('token_refresh')

    def test_login_account(self, api_client, user_data, test_user):
        token = api_client.post(self.access_url, data=user_data, format="json")
        refresh_token = token.json().get("refresh")
        response = api_client.post(self.refresh_url, data={"refresh": refresh_token}, format="json")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCourseList:

    url = reverse('course-list')

    def test_course_list_authorized_user(self, authorized_user, course):
        response = authorized_user.get(self.url, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get("results")) == 1

    def test_course_list_unauthorized_user(self, api_client, course):
        response = api_client.get(self.url, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_course_creation_authorized_user(self, authorized_user, course_data, test_user):
        response = authorized_user.post(self.url, data=course_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json().get("name") == course_data["name"]
        assert User.objects.filter(as_teacher__name=course_data["name"]).exists()


@pytest.mark.django_db
class TestCourseDetail:

    def test_course_retrieve_authorized_user(self, authorized_user, course):
        url = reverse('course-detail', kwargs={'pk': course.id})
        response = authorized_user.get(url, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_course_update_authorized_user(self, authorized_user, test_user, course):
        url = reverse('course-detail', kwargs={'pk': course.id})
        update_data = {'name': 'UPDATED course'}
        response = authorized_user.patch(url, data=update_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get("name") == update_data["name"]
        assert User.objects.filter(as_teacher__name=update_data["name"]).exists()

    def test_course_delete_authorized_user(self, authorized_user, course_data, test_user, course):
        url = reverse('course-detail', kwargs={'pk': course.id})
        response = authorized_user.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Course.objects.filter(id=course.id).exists()
