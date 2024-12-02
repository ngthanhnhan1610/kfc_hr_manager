# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def home(request):
    # Kiểm tra vai trò của người dùng
    if request.user.role == "manager":
        message = "Hello quản lý"
    elif request.user.role == "employee":
        message = "Hello nhân viên"
    else:
        message = "Hello người dùng"

    return render(request, "home.html", {"message": message})
