import json
import urllib.request
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from .forms import SkillSheetApplicationForm
from .models import SkillSheet, Staff


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


def skill_sheet_list(request):
    q = (request.GET.get("q") or "").strip()
    selected_nationality = (request.GET.get("nationality") or "").strip()
    selected_status = (request.GET.get("status") or "").strip()

    sheets = SkillSheet.objects.select_related("staff").order_by("-staff__created_at", "-pk")

    if q:
        sheets = sheets.filter(
            Q(staff__full_name__icontains=q)
            | Q(staff__phone__icontains=q)
            | Q(staff__address__icontains=q)
            | Q(wh1_company__icontains=q)
            | Q(wh2_company__icontains=q)
            | Q(wh3_company__icontains=q)
        )

    if selected_nationality:
        sheets = sheets.filter(staff__nationality=selected_nationality)

    if selected_status:
        sheets = sheets.filter(staff__status=selected_status)

    nationality_choices = getattr(Staff, "NATIONALITY_CHOICES", ())
    status_choices = getattr(Staff, "STATUS_CHOICES", ())

    return render(
        request,
        "hr/skill_sheet_list.html",
        {
            "sheets": sheets,
            "q": q,
            "selected_nationality": selected_nationality,
            "selected_status": selected_status,
            "nationality_choices": nationality_choices,
            "status_choices": status_choices,
        },
    )


def skill_sheet_detail(request, pk):
    sheet = get_object_or_404(SkillSheet.objects.select_related("staff"), pk=pk)
    return render(
        request,
        "hr/skill_sheet_detail.html",
        {
            "sheet": sheet,
            "staff": sheet.staff,
        },
    )


@require_GET
def postal_lookup(request):
    zip_code = "".join(ch for ch in request.GET.get("zipcode", "") if ch.isdigit())
    if len(zip_code) != 7:
        return JsonResponse({"ok": False, "address": "", "error": "invalid_zip"})

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    # 1. zipcloud
    try:
        url = f"https://zipcloud.ibsnet.co.jp/api/api/json?zipcode={zip_code}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("results"):
                r = data["results"][0]
                address = f"{r.get('address1', '')}{r.get('address2', '')}{r.get('address3', '')}"
                if address:
                    return JsonResponse({"ok": True, "address": address})
    except Exception:
        pass

    # 2. postcode-jp
    try:
        url2 = f"https://apis.postcode-jp.com/api/v5/postcodes/{zip_code}"
        req2 = urllib.request.Request(url2, headers=headers)
        with urllib.request.urlopen(req2, timeout=6) as resp2:
            data2 = json.loads(resp2.read().decode("utf-8"))
            item = None
            if isinstance(data2, list) and len(data2) > 0:
                item = data2[0]
            elif isinstance(data2, dict) and data2.get("data"):
                item = data2["data"][0]
            if item:
                address = f"{item.get('pref', '')}{item.get('city', '')}{item.get('town', '')}"
                if address:
                    return JsonResponse({"ok": True, "address": address})
    except Exception:
        pass

    # 3. HeartRails Geo API
    try:
        url3 = f"https://geoapi.heartrails.com/api/json?method=searchByPostal&postal={zip_code}"
        req3 = urllib.request.Request(url3, headers=headers)
        with urllib.request.urlopen(req3, timeout=6) as resp3:
            data3 = json.loads(resp3.read().decode("utf-8"))
            locs = (data3.get("response") or {}).get("location") or []
            if locs:
                loc = locs[0]
                address = f"{loc.get('prefecture', '')}{loc.get('city', '')}{loc.get('town', '')}"
                if address:
                    return JsonResponse({"ok": True, "address": address})
    except Exception:
        pass

    return JsonResponse({"ok": False, "address": "", "error": "not_found"})