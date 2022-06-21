
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Dogs


class DogTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_Dog = Dogs.objects.create(
            name="rake",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_Dog.save()

    
    # class 32
    def test_authentication_required(self):
        self.client.logout()
        url = reverse("Dog_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DogTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_Dog = Dogs.objects.create(
            name="rake",
            owner=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_Dog.save()

    def test_Dogs_model(self):
        Dog = Dogs.objects.get(id=1)
        actual_owner = str(Dog.owner)
        actual_name = str(Dog.name)
        actual_description = str(Dog.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_Dog_list(self):
        url = reverse("Dog_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Dog = response.data
        self.assertEqual(len(Dog), 1)
        self.assertEqual(Dog[0]["name"], "rake")

    def test_get_Dog_by_id(self):
        url = reverse("Dog_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Dog = response.data
        self.assertEqual(Dog["name"], "rake")

    def test_create_Dog(self):
        url = reverse("Dog_list")
        data = {"owner": 1, "name": "spoon", "description": "good for cereal and soup"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Dogs = Dogs.objects.all()
        self.assertEqual(len(Dogs), 2)
        self.assertEqual(Dogs.objects.get(id=2).name, "spoon")

    def test_update_Dog(self):
        url = reverse("Dog_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "rake",
            "description": "pole with a crossbar toothed like a comb.",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        Dog = Dogs.objects.get(id=1)
        self.assertEqual(Dog.name, data["name"])
        self.assertEqual(Dog.owner.id, data["owner"])
        self.assertEqual(Dog.description, data["description"])

    def test_delete_Dog(self):
        url = reverse("Dog_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        Dogs = Dogs.objects.all()
        self.assertEqual(len(Dogs), 0)
