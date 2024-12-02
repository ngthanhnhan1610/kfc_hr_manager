# employee_app/admin.py
from django.contrib import admin
from .models import Employee, Availability, Shift, Attendance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "branch", "phone_number", "date_of_birth", "photo")
    list_filter = ("branch",)
    search_fields = ("user__username", "phone_number")


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "start_time", "end_time")
    list_filter = ("date",)
    search_fields = ("employee__user__username",)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ("employee", "branch", "date", "start_time", "end_time")
    list_filter = ("branch", "date")
    search_fields = ("employee__user__username",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "check_in", "check_out", "adjusted_hours")
    list_filter = ("date",)
    search_fields = ("employee__user__username",)
