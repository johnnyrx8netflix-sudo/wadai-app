from django.contrib import admin
from .models import LeaveRequest, RecruitmentCase, SkillSheet, Staff


class SkillSheetInline(admin.StackedInline):
    model = SkillSheet
    can_delete = False


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "gender", "nationality", "visa_type", "phone", "status", "created_at")
    list_filter = ("nationality", "visa_type", "gender", "status")
    search_fields = ("full_name", "phone", "address")
    inlines = [SkillSheetInline]


@admin.register(SkillSheet)
class SkillSheetAdmin(admin.ModelAdmin):
    list_display = ("staff", "drivers_license", "commute_method", "overtime", "jp_speaking", "uniform_jacket", "safety_shoes")
    list_filter = ("drivers_license", "commute_method", "overtime", "jp_speaking")
    search_fields = ("staff__full_name", "wh1_company", "wh1_job")


@admin.register(RecruitmentCase)
class RecruitmentCaseAdmin(admin.ModelAdmin):
    list_display = ("client_name", "title", "work_location", "hourly_wage", "headcount", "status")
    list_filter = ("status",)
    search_fields = ("client_name", "title")


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("staff", "leave_date", "status", "created_at")
    list_filter = ("status",)