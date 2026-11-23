from django import forms
from .models import SkillSheet, Staff


SHIFT_CHOICES = [
    ("day", "昼勤のみ / Diurno / Day shift"),
    ("night", "夜勤のみ / Noturno / Night shift"),
    ("2shift", "2交代 / 2 turnos / Two-shift rotation"),
    ("3shift", "3交代 / 3 turnos / Three-shift rotation"),
    ("any", "特に選ばない / Sem preferência / No preference"),
]

MARITAL_STATUS_CHOICES = getattr(
    Staff,
    "MARITAL_STATUS_CHOICES",
    [
        ("single", "未婚 / Solteiro(a) / Single"),
        ("married", "既婚 / Casado(a) / Married"),
    ],
)


class StaffSkillRegistrationForm(forms.ModelForm):
    # Staff基本情報 ※生年月日の次に年齢・携帯番号、性別のあとに婚姻状況
    full_name = forms.CharField(
        label="1. 名前 / Nome / Name *",
        widget=forms.TextInput(attrs={"placeholder": "回答を入力してください"}),
    )
    postal_code = forms.CharField(
        label="2. 〒 郵便番号 / Caixa postal / postal cod *",
        widget=forms.TextInput(attrs={"placeholder": "例：430-0000"}),
    )
    address = forms.CharField(
        label="3. 住所 / Endereço / Address *",
        widget=forms.TextInput(attrs={"placeholder": "郵便番号を入力すると自動表示されます"}),
    )
    gender = forms.ChoiceField(
        label="4. 性別 / Sexo / Gender *",
        choices=Staff.GENDER_CHOICES,
        widget=forms.RadioSelect,
    )
    marital_status = forms.ChoiceField(
        label="5. 婚姻状況 / Estado civil / Marital status *",
        choices=MARITAL_STATUS_CHOICES,
        widget=forms.RadioSelect,
    )
    birth_date = forms.DateField(
        label="6. 生年月日 / Data de nascimento / Date of birth *",
        input_formats=["%Y-%m-%d", "%Y%m%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "min": "1930-01-01",
                "max": "2020-12-31",
            },
        ),
    )
    age = forms.IntegerField(
        label="7. 年齢 / Idade / Age *",
        min_value=15,
        max_value=99,
        required=False,
        widget=forms.NumberInput(
            attrs={
                "readonly": "readonly",
                "placeholder": "生年月日を選択すると自動計算されます",
            }
        ),
    )
    phone = forms.CharField(
        label="8. 携帯番号 / Numero de Telefone / Cell phone number *",
        widget=forms.TextInput(attrs={"placeholder": "例：090-1234-5678"}),
    )
    nationality = forms.ChoiceField(
        label="9. 国籍 / Nacionalidade / Nationality *",
        choices=Staff.NATIONALITY_CHOICES,
        widget=forms.RadioSelect,
    )
    visa_type = forms.ChoiceField(
        label="10. ビザの種類 / Tipo do Visto / Visa type *",
        choices=Staff.VISA_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    # 勤務条件 (11〜16)
    drivers_license = forms.ChoiceField(
        label="11. 日本車免許 / Habilitação Japonesa / Japanese driver's license *",
        choices=SkillSheet.YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    commute_method = forms.ChoiceField(
        label="12. 通勤方法 / Método de trajeto / Mode of transportation *",
        choices=SkillSheet.COMMUTE_CHOICES,
        widget=forms.RadioSelect,
    )
    commute_other = forms.CharField(
        label="その他（通勤方法） / Outros",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "「その他」を選んだ場合のみ入力"}),
    )
    overtime = forms.ChoiceField(
        label="13. 残業 / Horas extras / Overtime *",
        choices=SkillSheet.OVERTIME_CHOICES,
        widget=forms.RadioSelect,
    )
    holiday_work = forms.ChoiceField(
        label="14. 休日出勤 / Trabalho no dia de folga / Holiday work *",
        choices=SkillSheet.YES_NO_MAYBE_CHOICES,
        widget=forms.RadioSelect,
    )
    early_shift = forms.ChoiceField(
        label="15. 早出 / Entrada antecipada / Early shift *",
        choices=SkillSheet.YES_NO_MAYBE_CHOICES,
        widget=forms.RadioSelect,
    )
    preferred_shift = forms.MultipleChoiceField(
        label="16. 希望勤務時間 / Horário de trabalho desejado / Preferred working hours *",
        choices=SHIFT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )

    # 職歴 ① (17〜22)
    wh1_company = forms.CharField(label="17. ① 会社名 / Nome da empresa / Company name", required=False)
    wh1_job = forms.CharField(label="18. ① 業務内容 / Tipo de serviço / Job description", required=False)
    wh1_period = forms.CharField(label="19. ① 期間 / Tempo de trabalho / Employment period", required=False)
    wh1_agency = forms.CharField(label="20. ① 派遣会社 / Empreiteira / Staffing agency", required=False)
    wh1_wage = forms.CharField(label="21. ① 時給 / Salário por hora / Hourly wage", required=False)
    wh1_reason = forms.ChoiceField(
        label="22. ① 退職理由 / Motivo da saída / Reason for leaving",
        choices=SkillSheet.LEAVE_REASON_CHOICES,
        required=False,
    )
    wh1_reason_other = forms.CharField(
        label="その他（退職理由） / Outros",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "「その他」を選んだ場合のみ入力"}),
    )

    # 職歴 ②
    wh2_company = forms.CharField(label="② 会社名 / Nome da empresa / Company name", required=False)
    wh2_job = forms.CharField(label="② 業務内容 / Tipo de serviço / Job description", required=False)
    wh2_period = forms.CharField(label="② 期間 / Tempo de trabalho / Employment period", required=False)
    wh2_agency = forms.CharField(label="② 派遣会社 / Empreiteira / Staffing agency", required=False)
    wh2_wage = forms.CharField(label="② 時給 / Salário por hora / Hourly wage", required=False)
    wh2_reason = forms.ChoiceField(
        label="② 退職理由 / Motivo da saída / Reason for leaving",
        choices=SkillSheet.LEAVE_REASON_CHOICES,
        required=False,
    )
    wh2_reason_other = forms.CharField(
        label="その他（退職理由） / Outros",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "「その他」を選んだ場合のみ入力"}),
    )

    # 職歴 ③
    wh3_company = forms.CharField(label="③ 会社名 / Nome da empresa / Company name", required=False)
    wh3_job = forms.CharField(label="③ 業務内容 / Tipo de serviço / Job description", required=False)
    wh3_period = forms.CharField(label="③ 期間 / Tempo de trabalho / Employment period", required=False)
    wh3_agency = forms.CharField(label="③ 派遣会社 / Empreiteira / Staffing agency", required=False)
    wh3_wage = forms.CharField(label="③ 時給 / Salário por hora / Hourly wage", required=False)
    wh3_reason = forms.ChoiceField(
        label="③ 退職理由 / Motivo da saída / Reason for leaving",
        choices=SkillSheet.LEAVE_REASON_CHOICES,
        required=False,
    )
    wh3_reason_other = forms.CharField(
        label="その他（退職理由） / Outros",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "「その他」を選んだ場合のみ入力"}),
    )

    # 日本語力 (43〜45)
    jp_speaking = forms.ChoiceField(
        label="43. 日本語レベル / Nível de idioma japonês / Japanese proficiency *",
        choices=SkillSheet.JP_LEVEL_CHOICES,
        widget=forms.RadioSelect,
    )
    jp_reading = forms.ChoiceField(
        label="44. 日本語 読み / Leitura em japonês / Japanese reading skills *",
        choices=SkillSheet.JP_LEVEL_CHOICES,
        widget=forms.RadioSelect,
    )
    jp_writing = forms.ChoiceField(
        label="45. 日本語 書き / Escrita em japonês / Japanese writing skills *",
        choices=SkillSheet.JP_LEVEL_CHOICES,
        widget=forms.RadioSelect,
    )

    # 作業服 (46〜48)
    uniform_jacket = forms.ChoiceField(
        label="46. 上着 / Camisa / Jacket *",
        choices=SkillSheet.SIZE_CHOICES,
        widget=forms.RadioSelect,
    )
    uniform_pants = forms.ChoiceField(
        label="47. ズボン / Calça / Pants *",
        choices=SkillSheet.SIZE_CHOICES,
        widget=forms.RadioSelect,
    )
    safety_shoes = forms.CharField(
        label="48. 靴 / Sapato / Safety shoes *",
        widget=forms.TextInput(attrs={"placeholder": "例：26.5cm"}),
    )

    class Meta:
        model = Staff
        fields = [
            "full_name",
            "postal_code",
            "address",
            "gender",
            "marital_status",
            "birth_date",
            "age",
            "phone",
            "nationality",
            "visa_type",
        ]

    def clean(self):
        cleaned_data = super().clean()
        nationality = (cleaned_data.get("nationality") or "").strip().lower()
        visa_type = cleaned_data.get("visa_type")

        is_japan = nationality in ("japan", "jp", "日本")
        if is_japan:
            cleaned_data["visa_type"] = ""
        elif nationality and not visa_type:
            self.add_error("visa_type", "外国籍の方はビザの種類を選択してください。")

        return cleaned_data