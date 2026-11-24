import json
import urllib.request
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
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


@require_GET
def postal_lookup(request):
    zip_code = "".join(ch for ch in request.GET.get("zipcode", "") if ch.isdigit())
    if len(zip_code) != 7:
        return JsonResponse({"ok": False, "address": "", "error": "invalid_zip"})

    # 1. zipcloud API
    try:
        url = f"https://zipcloud.ibsnet.co.jp/api/api/json?zipcode={zip_code}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results") or []
            if results:
                r = results[0]
                address = f"{r.get('address1', '')}{r.get('address2', '')}{r.get('address3', '')}"
                if address:
                    return JsonResponse({"ok": True, "address": address})
    except Exception:
        pass

    # 2. postcode-jp API（フォールバック）
    try:
        url2 = f"https://apis.postcode-jp.com/api/v5/postcodes/{zip_code}"
        req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=5) as resp2:
            data2 = json.loads(resp2.read().decode("utf-8"))
            item = data2[0] if isinstance(data2, list) and data2 else None
            if not item and isinstance(data2, dict):
                arr = data2.get("data") or []
                item = arr[0] if arr else None
            if item:
                address = f"{item.get('pref', '')}{item.get('city', '')}{item.get('town', '')}"
                if address:
                    return JsonResponse({"ok": True, "address": address})
    except Exception:
        pass

    return JsonResponse({"ok": False, "address": "", "error": "not_found"})