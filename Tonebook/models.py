from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class BUManager(BaseUserManager):
    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError("Users must enter a username")

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        return self.create_user(email, password, **other_fields)


class User(AbstractUser):
    # User attributes
    username = models.CharField(max_length=50, unique=True)
    files = models.ManyToManyField("File", blank=True)

    # Status
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = BUManager()

    def obj(self):
        return {
            'id': self.id,
            'username': self.username,
            'files': self.get_files()
        }

    def get_files(self):
        files = []

        for file in self.files.all().order_by("-modified"):
            files.append(file.obj())

        return files


class File(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now_add=True, blank=True)
    content = models.TextField(default="")

    def obj(self):
        return {
            "name": self.name,
            "created": str(self.created),
            "modified": str(self.modified),
            "edit": reverse("edit", kwargs={"file_id": self.id}),
            "save": reverse("save", kwargs={"file_id": self.id}),
            "delete": reverse("delete", kwargs={"file_id": self.id}),
            "rename": reverse("rename", kwargs={"file_id": self.id}),
        }

    def full_obj(self):
        return {
            "name": self.name,
            "created": str(self.created),
            "modified": str(self.modified),
            "content": self.content,
            "edit": reverse("edit", kwargs={"file_id": self.id}),
            "save": reverse("save", kwargs={"file_id": self.id}),
            "delete": reverse("delete", kwargs={"file_id": self.id}),
            "rename": reverse("rename", kwargs={"file_id": self.id}),
        }
