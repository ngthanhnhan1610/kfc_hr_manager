# manager_app/models.py
from django.db import models
from authentication.models import User


class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.location}"


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'manager'})
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Manager: {self.user.username} at {self.branch}"
