# urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from authentication import (
    views,
)  # Định nghĩa thêm view `home` để xử lý điều hướng sau đăng nhập
from django.conf.urls.static import static

from manager.views import timekeeping, worksheet

from .views import (
    faceid_view,
    faceid_confirm_view,
    faceid_return,
    find_user_view,
    faceid_failed,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Trang đăng nhập
    path("", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    # Trang chào mừng sau khi đăng nhập
    path("home/", views.home, name="home"),
    ## Face ID urls ###
    path("face-id/", faceid_view, name="face-id"),  # Trang checkin/checkout bằng faceid
    path(
        "face-id-confirm/", faceid_confirm_view, name="face-id-confirm"
    ),  # Trang xác nhận checkin/checkout bằng faceid
    path(
        "face-id-failed/", faceid_failed, name="face-id-failed"
    ),  # Trang thông báo checkin/checkout bằng faceid thất bại
    path(
        "face-id-return/", faceid_return, name="face-id-return"
    ),  # Trang quay lại checkin/checkout bằng faceid
    path("classify/", find_user_view, name="classify"),
    path("timekeeping/", timekeeping, name="timekeeping"),
    path("worksheet/", worksheet, name="worksheet"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
