# employee_app/models.py
from django.db import models
from authentication.models import User
from manager.models import *


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "employee"}
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, upload_to="employee_photos")

    def __str__(self):
        return f"Employee: {self.user.username} at {self.branch}"


class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee.user.username} available on {self.date} from {self.start_time} to {self.end_time}"


class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_shifts",
    )

    def __str__(self):
        return f"Shift for {self.employee.user.username} on {self.date} from {self.start_time} to {self.end_time}"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField(null=True, blank=True)
    adjusted_hours = models.FloatField(null=True, blank=True)
    approved_by_manager = models.ForeignKey(
        Manager, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Attendance for {self.employee.user.username} on {self.date}"
