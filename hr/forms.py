from django import forms
from .models import Staff, SkillSheet


class SkillSheetApplicationForm(forms.Form):
    # --- Staff (1〜9 + 婚姻状況) ---
    full_name = forms.CharField(label="1. 名前 / Nome / Name", max_length=100)
    age = forms.IntegerField(label="2. 年齢 / Idade / Age", required=False, min_value=0, max_value=120)
    phone = forms.CharField(label="3. 携帯番号 / Numero de Telefone / Cell phone number", max_length=30)
    postal_code = forms.CharField(label="4. 〒 郵便番号 / Caixa postal / postal cod", max_length=20, required=False)
    address = forms.CharField(label="5. 住所 / Endereço / Address", max_length=255, required=False)
    gender = forms.ChoiceField(
        label="6. 性別 / Sexo / Gender",
        choices=[("", "---------")] + Staff.GENDER_CHOICES,
        required=False,
    )
    marital_status = forms.ChoiceField(
        label="婚姻状況 / Estado civil / Marital status",
        choices=[("", "---------")] + Staff.MARITAL_STATUS_CHOICES,
        required=False,
    )
    birth_date = forms.CharField(
        label="7. 生年月日 / Data de nascimento (yyyymmdd) / Date of birth (YYYYMMDD)",
        max_length=12,
        required=False,
    )
    nationality = forms.ChoiceField(
        label="8. 国籍 / Nacionalidade / Nationality",
        choices=[("", "---------")] + Staff.NATIONALITY_CHOICES,
        required=False,
    )
    visa_type = forms.ChoiceField(
        label="9. ビザの種類 / Tipo do Visto / Visa type",
        choices=[("", "---------")] + Staff.VISA_CHOICES,
        required=False,
    )

    # --- SkillSheet (10〜15) ---
    drivers_license = forms.ChoiceField(
        label="10. 日本車免許 / Habilitação Japonesa / Japanese driver's license",
        choices=[("", "---------")] + SkillSheet.YES_NO_CHOICES,
        required=False,
    )
    commute_method = forms.ChoiceField(
        label="11. 通勤方法 / Método de trajeto / Mode of transportation",
        choices=[("", "---------")] + SkillSheet.COMMUTE_CHOICES,
        required=False,
    )
    commute_other = forms.CharField(label="11-2. 通勤方法（その他詳細）", max_length=100, required=False)
    overtime = forms.ChoiceField(
        label="12. 残業 / Horas extras / Overtime",
        choices=[("", "---------")] + SkillSheet.OVERTIME_CHOICES,
        required=False,
    )
    holiday_work = forms.ChoiceField(
        label="13. 休日出勤 / Trabalho no dia de folga / Holiday work",
        choices=[("", "---------")] + SkillSheet.YES_NO_MAYBE_CHOICES,
        required=False,
    )
    early_shift = forms.ChoiceField(
        label="14. 早出 / Entrada antecipada / Early shift",
        choices=[("", "---------")] + SkillSheet.YES_NO_MAYBE_CHOICES,
        required=False,
    )
    preferred_shift = forms.CharField(
        label="15. 希望勤務時間 / Horário de trabalho desejado / Preferred working hours",
        max_length=200,
        required=False,
    )

    # --- 職歴 ① ---
    wh1_company = forms.CharField(label="① 会社名 / Nome da empresa / Company name", max_length=150, required=False)
    wh1_job = forms.CharField(label="① 業務内容 / Tipo de serviço / Job description", max_length=200, required=False)
    wh1_period = forms.CharField(label="① 期間 / Tempo de trabalho / Employment period", max_length=100, required=False)
    wh1_agency = forms.CharField(label="① 派遣会社 / Empreiteira / Staffing agency", max_length=150, required=False)
    wh1_wage = forms.CharField(label="① 時給 / Salário por hora / Hourly wage", max_length=50, required=False)
    wh1_reason = forms.ChoiceField(
        label="① 退職理由 / Motivo da saída / Reason for leaving",
        choices=SkillSheet.LEAVE_REASON_CHOICES,
        required=False,
    )
    wh1_reason_other = forms.CharField(label="① 退職理由（その他）", max_length=150, required=False)

    # --- 職歴 ② ---
    wh2_company = forms.CharField(label="② 会社名 / Nome da empresa / Company name", max_length=150, required=False)
    wh2_job = forms.CharField(label="② 業務内容 / Tipo de serviço / Job description", max_length=200, required=False)
    wh2_period = forms.CharField(label="② 期間 / Tempo de trabalho / Employment period", max_length=100, required=False)
    wh2_agency = forms.CharField(label="② 派遣会社 / Empreiteira / Staffing agency", max_length=150, required=False)
    wh2_wage = forms.CharField(label="② 時給 / Salário por hora / Hourly wage", max_length=50, required=False)
    wh2_reason = forms.ChoiceField(
        label="② 退職理由 / Motivo da saída / Reason for leaving",
        choices=SkillSheet.LEAVE_REASON_CHOICES,
        required=False,
    )
    wh2_reason_other = forms.CharField(label="② 退職理由（その他）", max_length=150, required=False)

    # --- 職歴 ③ ---
    wh3_company = forms.CharField(label="③ 会社名 / Nome da empresa / Company name", max_length=150, required=False)
    wh3_job = forms.CharField(label="③ 業務内容 / Tipo de serviço / Job description", max_length=200, required=False)
    wh3_period = forms.CharField(label="③ 期間 / Tempo de trabalho / Employment period", max_length=100, required=False)
    wh3_agency = forms.CharField(label="③ 派遣会社 / Empreiteira / Staffing agency", max_length=150, required=False)
    wh3_wage = forms.CharField(label="③ 時給 / Salário por hora / Hourly wage", max_length=50, required=False)
    wh3_reason = forms.ChoiceField(
        label="③ 退職理由 / Motivo da saída / Reason for leaving",
        choices=SkillSheet.LEAVE_REASON_CHOICES,
        required=False,
    )
    wh3_reason_other = forms.CharField(label="③ 退職理由（その他）", max_length=150, required=False)

    # --- 日本語力 (43〜45) ---
    jp_speaking = forms.ChoiceField(
        label="43. 日本語レベル / Nível de idioma japonês / Japanese proficiency",
        choices=[("", "---------")] + SkillSheet.JP_LEVEL_CHOICES,
        required=False,
    )
    jp_reading = forms.ChoiceField(
        label="44. 日本語 読み / Leitura em japonês / Japanese reading skills",
        choices=[("", "---------")] + SkillSheet.JP_LEVEL_CHOICES,
        required=False,
    )
    jp_writing = forms.ChoiceField(
        label="45. 日本語 書き / Escrita em japonês / Japanese writing skills",
        choices=[("", "---------")] + SkillSheet.JP_LEVEL_CHOICES,
        required=False,
    )

    # --- 作業服 (46〜48) ---
    uniform_jacket = forms.ChoiceField(
        label="46. 上着 / Camisa / Jacket",
        choices=[("", "---------")] + SkillSheet.SIZE_CHOICES,
        required=False,
    )
    uniform_pants = forms.ChoiceField(
        label="47. ズボン / Calça / Pants",
        choices=[("", "---------")] + SkillSheet.SIZE_CHOICES,
        required=False,
    )
    safety_shoes = forms.CharField(label="48. 靴 / Sapato / Safety shoes", max_length=20, required=False)