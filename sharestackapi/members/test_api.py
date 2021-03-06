import random
from datetime import datetime

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserAPITests(APITestCase):

    def setUp(self):
        # Set an user so we can use the API
        password = "I love my Xmen"
        u = User()
        u.username = "profesor-X"
        u.set_password(password)
        u.first_name = "Charles"
        u.last_name = "Xavier"
        u.is_superuser = True
        u.is_active = True
        u.is_staff = True
        u.save()

        # Login, we could use: 'force_authenticate' but we will login
        # as always, the 'classic' way, wiht DRF help
        self.client.login(username=u.username, password=password)

        self.data = {
            "username": "batman",
            "is_superuser": True,
            "password": u'pbkdf2_sha256$12000$r9vx2aWg13x218slB59DrbMWO8=...',
            "first_name": "Bruce",
            "last_name": "Wayne",
            "email": "thedarkknight@gmail.com",
            "is_staff": False,
            "is_active": True,
            "url": "http://jokeryouwillbebeaten.org",
            "gravatar": "thedarkknight@gmail.com",
        }

    def test_create(self):
        url = reverse('user-list')

        # Json default format in settings.py
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Can't check as a full equals because id, last_login... are autofields
        for k, v in self.data.items():
            self.assertEqual(response.data[k], self.data[k])

    def test_update(self):
        # Save first (We have already, but we will get the id)
        url = reverse('user-list')
        response = self.client.post(url, self.data)

        # Update later
        url = reverse('user-detail', args=[response.data["id"]])

        self.data["url"] = "http://batmanisnotbrucewayne.com"
        response = self.client.put(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for k, v in self.data.items():
            self.assertEqual(response.data[k], self.data[k])

    def test_detail(self):
        # Save first (We have already, but we will get the id)
        url = reverse('user-list')
        response = self.client.post(url, self.data)

        # Get the details
        url = reverse('user-detail', args=[response.data["id"]])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for k, v in self.data.items():
            self.assertEqual(response.data[k], self.data[k])

    def test_delete(self):
         # Save first (We have already, but we will get the id)
        url = reverse('user-list')
        response = self.client.post(url, self.data)

        # Get the details
        url = reverse('user-detail', args=[response.data["id"]])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list(self):
        url = reverse('user-list')

        # Sove N users
        number_users = random.randrange(20, 100)
        for i in range(number_users):
            self.data["username"] = "Batman-{0}".format(i)
            response = self.client.post(url, self.data)

        response = self.client.get(url)

        self.assertEqual(response.data["count"], number_users + 1)
