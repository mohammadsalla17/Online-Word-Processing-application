import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from Tonebook.models import User


# This will test the main page of the application to determine if it will render
class MainPageTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_view(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

# This will test the register page of the application to determine if it will register the set user
class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        self.user_acc = {
            "username": "sala",
            "password": "1234",
        }

    def test_view(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")

    def test_register(self):
        response = self.client.post(reverse("register"), self.user_acc)

        self.assertEqual(response.status_code, 200)
        self.assertEquals(User.objects.all().count(), 1)

        user = User.objects.filter(username=self.user_acc["username"])
        self.assertTrue(user.exists())

# This will test the login page of the application to determine if it will allow for the authentication of the set username and password
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        self.user_acc = {
            "username": "sala",
            "password": "1234",
        }

        self.client.post(reverse('register'), self.user_acc)

    def test_authenticate(self):
        self.assertTrue(authenticate(
            username=self.user_acc["username"],
            password=self.user_acc["password"]
        ))

    def test_view_login(self):
        response = self.client.get(reverse("login"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_attempt_login(self):
        response = self.client.post(reverse('login'), self.user_acc)
        self.assertRedirects(response, reverse("account"))

        user = User.objects.get(username=self.user_acc["username"])
        self.assertTrue(user.is_authenticated)

    def test_view_account(self):
        self.client.post(reverse('login'), self.user_acc)
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account.html")

# This will test the apis of the application to determine if it will render the files it is meant to as well as the creating, renaming and deleting of a file
class APIsTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

        self.user_acc = {
            "username": "sala",
            "password": "1234",
        }

        self.client.post(reverse('register'), self.user_acc)
        self.client.post(reverse('login'), self.user_acc)

    def test_create_file(self):

        response = self.client.post(reverse("create"), data=json.dumps({
            "name": "File Name",
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.user_acc["username"])

        file = user.files.filter(name="File Name")
        self.assertTrue(file.exists())
        file = file.get(name="File Name")
        self.assertEqual(file.name, "File Name")

    def test_rename_file(self):
        self.client.post(reverse("create"), data=json.dumps({
            "name": "File Name",
        }), content_type="application/json")

        user = User.objects.get(username=self.user_acc["username"])
        file = user.files.get(name="File Name")

        response = self.client.post(file.obj()["rename"], data=json.dumps({
            "name": "New File Name",
        }), content_type="application/json")

        file = user.files.get(id=file.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(file.name, "New File Name")

    def test_delete_file(self):
        self.client.post(reverse("create"), data=json.dumps({
            "name": "File Name",
        }), content_type="application/json")

        user = User.objects.get(username=self.user_acc["username"])
        file = user.files.get(name="File Name")

        response = self.client.post(file.obj()["delete"])

        file = user.files.filter(id=file.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not file.exists())

    def test_save_file(self):
        self.client.post(reverse("create"), data=json.dumps({
            "name": "File Name",
        }), content_type="application/json")

        user = User.objects.get(username=self.user_acc["username"])
        file = user.files.get(name="File Name")

        response = self.client.post(file.obj()["save"], data=json.dumps({
            "content": "Hello <b>World</b>!",
        }), content_type="application/json")

        file = user.files.get(id=file.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(file.content, "Hello <b>World</b>!")

    def test_edit_view(self):
        self.client.post(reverse("create"), data=json.dumps({
            "name": "File Name",
        }), content_type="application/json")

        user = User.objects.get(username=self.user_acc["username"])
        file = user.files.get(name="File Name")

        response = self.client.get(file.obj()["edit"])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit.html")
