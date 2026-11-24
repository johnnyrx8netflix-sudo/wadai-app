from django.db import transaction
from django.shortcuts import render
from .forms import SkillSheetApplicationForm
from .models import Staff, SkillSheet


def skill_sheet_apply(request):
    submitted = False

    if request.method == "POST":
        form = SkillSheetApplicationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            with transaction.atomic():
                staff = Staff.objects.create(
                    full_name=d["full_name"],
                    age=d["age"],
                    phone=d["phone"],
                    postal_code=d["postal_code"],
                    address=d["address"],
                    gender=d["gender"],
                    marital_status=d["marital_status"],
                    birth_date=d["birth_date"],
                    nationality=d["nationality"],
                    visa_type=d["visa_type"],
                    status="standby",
                )
                SkillSheet.objects.create(
                    staff=staff,
                    drivers_license=d["drivers_license"],
                    commute_method=d["commute_method"],
                    commute_other=d["commute_other"],
                    overtime=d["overtime"],
                    holiday_work=d["holiday_work"],
                    early_shift=d["early_shift"],
                    preferred_shift=d["preferred_shift"],
                    wh1_company=d["wh1_company"],
                    wh1_job=d["wh1_job"],
                    wh1_period=d["wh1_period"],
                    wh1_agency=d["wh1_agency"],
                    wh1_wage=d["wh1_wage"],
                    wh1_reason=d["wh1_reason"],
                    wh1_reason_other=d["wh1_reason_other"],
                    wh2_company=d["wh2_company"],
                    wh2_job=d["wh2_job"],
                    wh2_period=d["wh2_period"],
                    wh2_agency=d["wh2_agency"],
                    wh2_wage=d["wh2_wage"],
                    wh2_reason=d["wh2_reason"],
                    wh2_reason_other=d["wh2_reason_other"],
                    wh3_company=d["wh3_company"],
                    wh3_job=d["wh3_job"],
                    wh3_period=d["wh3_period"],
                    wh3_agency=d["wh3_agency"],
                    wh3_wage=d["wh3_wage"],
                    wh3_reason=d["wh3_reason"],
                    wh3_reason_other=d["wh3_reason_other"],
                    jp_speaking=d["jp_speaking"],
                    jp_reading=d["jp_reading"],
                    jp_writing=d["jp_writing"],
                    uniform_jacket=d["uniform_jacket"],
                    uniform_pants=d["uniform_pants"],
                    safety_shoes=d["safety_shoes"],
                )
            submitted = True
            form = SkillSheetApplicationForm()
    else:
        form = SkillSheetApplicationForm()

    return render(request, "hr/skill_sheet_apply.html", {"form": form, "submitted": submitted})