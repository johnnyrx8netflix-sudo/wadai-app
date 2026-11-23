from django.contrib import admin
from django.urls import path
from hr.views import (
    register_complete,
    register_staff,
    skill_sheet_detail,
    skill_sheet_list,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_staff, name="register_staff"),
    path("register/complete/", register_complete, name="register_complete"),
    path("skill-sheets/", skill_sheet_list, name="skill_sheet_list"),
    path("skill-sheets/<int:pk>/", skill_sheet_detail, name="skill_sheet_detail"),
]