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