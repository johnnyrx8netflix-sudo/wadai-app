from datetime import date

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SHIFT_CHOICES, StaffSkillRegistrationForm
from .models import SkillSheet, Staff

staff_only = user_passes_test(lambda u: u.is_active and u.is_staff, login_url="/admin/login/")


def calculate_age(birth_date, on_date=None):
    if not birth_date:
        return None
    today = on_date or date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def register_staff(request):
    if request.method == "POST":
        form = StaffSkillRegistrationForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.status = "standby"

            nationality = (staff.nationality or "").strip().lower()
            if nationality in ("japan", "jp", "日本"):
                staff.visa_type = ""

            birth_date = form.cleaned_data.get("birth_date")
            if birth_date:
                staff.age = calculate_age(birth_date)
                birth_field = Staff._meta.get_field("birth_date")
                if birth_field.get_internal_type() in ("CharField", "TextField"):
                    staff.birth_date = birth_date.strftime("%Y%m%d")
                else:
                    staff.birth_date = birth_date

            staff.save()

            shift_dict = dict(SHIFT_CHOICES)
            selected_shifts = [shift_dict[k] for k in form.cleaned_data.get("preferred_shift", []) if k in shift_dict]

            SkillSheet.objects.create(
                staff=staff,
                drivers_license=form.cleaned_data.get("drivers_license", ""),
                commute_method=form.cleaned_data.get("commute_method", ""),
                commute_other=form.cleaned_data.get("commute_other", ""),
                overtime=form.cleaned_data.get("overtime", ""),
                holiday_work=form.cleaned_data.get("holiday_work", ""),
                early_shift=form.cleaned_data.get("early_shift", ""),
                preferred_shift=" / ".join(selected_shifts),
                wh1_company=form.cleaned_data.get("wh1_company", ""),
                wh1_job=form.cleaned_data.get("wh1_job", ""),
                wh1_period=form.cleaned_data.get("wh1_period", ""),
                wh1_agency=form.cleaned_data.get("wh1_agency", ""),
                wh1_wage=form.cleaned_data.get("wh1_wage", ""),
                wh1_reason=form.cleaned_data.get("wh1_reason", ""),
                wh1_reason_other=form.cleaned_data.get("wh1_reason_other", ""),
                wh2_company=form.cleaned_data.get("wh2_company", ""),
                wh2_job=form.cleaned_data.get("wh2_job", ""),
                wh2_period=form.cleaned_data.get("wh2_period", ""),
                wh2_agency=form.cleaned_data.get("wh2_agency", ""),
                wh2_wage=form.cleaned_data.get("wh2_wage", ""),
                wh2_reason=form.cleaned_data.get("wh2_reason", ""),
                wh2_reason_other=form.cleaned_data.get("wh2_reason_other", ""),
                wh3_company=form.cleaned_data.get("wh3_company", ""),
                wh3_job=form.cleaned_data.get("wh3_job", ""),
                wh3_period=form.cleaned_data.get("wh3_period", ""),
                wh3_agency=form.cleaned_data.get("wh3_agency", ""),
                wh3_wage=form.cleaned_data.get("wh3_wage", ""),
                wh3_reason=form.cleaned_data.get("wh3_reason", ""),
                wh3_reason_other=form.cleaned_data.get("wh3_reason_other", ""),
                jp_speaking=form.cleaned_data.get("jp_speaking", ""),
                jp_reading=form.cleaned_data.get("jp_reading", ""),
                jp_writing=form.cleaned_data.get("jp_writing", ""),
                uniform_jacket=form.cleaned_data.get("uniform_jacket", ""),
                uniform_pants=form.cleaned_data.get("uniform_pants", ""),
                safety_shoes=form.cleaned_data.get("safety_shoes", ""),
            )
            return redirect("register_complete")
    else:
        form = StaffSkillRegistrationForm()

    return render(request, "hr/register.html", {"form": form})


def register_complete(request):
    return render(request, "hr/register_complete.html")


@staff_only
def skill_sheet_list(request):
    q = request.GET.get("q", "").strip()
    nationality = request.GET.get("nationality", "").strip()
    status = request.GET.get("status", "").strip()

    sheets = SkillSheet.objects.select_related("staff").order_by("-updated_at", "-staff__created_at")

    if q:
        sheets = sheets.filter(
            Q(staff__full_name__icontains=q)
            | Q(staff__phone__icontains=q)
            | Q(staff__address__icontains=q)
            | Q(wh1_company__icontains=q)
            | Q(wh1_job__icontains=q)
        )

    if nationality:
        sheets = sheets.filter(staff__nationality=nationality)

    if status:
        sheets = sheets.filter(staff__status=status)

    context = {
        "sheets": sheets,
        "q": q,
        "selected_nationality": nationality,
        "selected_status": status,
        "nationality_choices": Staff.NATIONALITY_CHOICES,
        "status_choices": Staff.STATUS_CHOICES,
    }
    return render(request, "hr/skill_sheet_list.html", context)


@staff_only
def skill_sheet_detail(request, pk):
    sheet = get_object_or_404(SkillSheet.objects.select_related("staff"), pk=pk)
    return render(request, "hr/skill_sheet_detail.html", {"sheet": sheet})