import pytz
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from employee.models import Employee, Attendance
from datetime import datetime


from .utils import is_ajax, classify_face
import base64
from logs.models import Log
from django.core.files.base import ContentFile
from authentication.models import User
from django.http import JsonResponse


# Đây là view dành cho những trang liên quan đến checkin/checkout bằng faceid
def faceid_view(request):
    return render(request, "face-id-checkin.html")


@login_required
def faceid_confirm_view(request):
    employee = Employee.objects.get(user=request.user)
    today = datetime.today().date()

    attendances = Attendance.objects.filter(employee=employee, date=today)
    curr_attendance = []
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")

    for attendance in attendances:
        date = attendance.date

        # Convert check-in and check-out times to datetime objects
        if attendance.check_in:
            check_in = datetime.combine(date, attendance.check_in)
            check_in = check_in.astimezone(vietnam_tz).strftime("%H:%M:%S")
        else:
            check_in = None

        if attendance.check_out:
            check_out = datetime.combine(date, attendance.check_out)
            check_out = check_out.astimezone(vietnam_tz).strftime("%H:%M:%S")
        else:
            check_out = None

        # reformat the date to dd-mm-yyyy
        date = date.strftime("%d/%m/%Y")

        curr_attendance.append(
            {
                "today": date,
                "check_in_time": check_in,
                "check_out_time": check_out,
            }
        )

    return render(
        request,
        "face-id-confirm.html",
        context={"curr_attendance": curr_attendance},
    )


def faceid_failed(request):
    return render(request, "face-id-failed.html")


def faceid_return(request):
    logout(request)
    return redirect("face-id")


def find_user_view(request):
    if is_ajax(request):
        photo = request.POST.get("photo")
        _, str_img = photo.split(";base64")

        decoded_file = base64.b64decode(str_img)

        x = Log()
        x.photo.save("upload.png", ContentFile(decoded_file))
        x.save()

        print(":::Photo path:::", x.photo.path)

        res = classify_face(x.photo.path)
        if res:
            user_exists = User.objects.filter(username=res).exists()
            if user_exists:
                user = User.objects.get(username=res)
                employee = Employee.objects.get(user=user)
                x.profile = employee
                x.save()

                login(request, user)
                print(":::User logged in:::", user.username)

                today = datetime.today().date()
                now = datetime.now()

                latest_attendance = (
                    Attendance.objects.filter(employee=employee).order_by("-id").first()
                )
                if latest_attendance and latest_attendance.date == today:
                    if latest_attendance.check_in and not latest_attendance.check_out:
                        latest_attendance.check_out = now.time()
                        latest_attendance.save()
                    else:
                        Attendance.objects.create(
                            employee=employee, date=today, check_in=now.time()
                        )
                    print(":::Attendance updated:::")
                    return JsonResponse({"success": True})
                else:
                    Attendance.objects.create(
                        employee=employee, date=today, check_in=now.time()
                    )
                    print(":::Attendance created:::")
                    return JsonResponse({"success": True})

        return JsonResponse({"success": False})
