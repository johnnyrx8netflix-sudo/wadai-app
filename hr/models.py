from django.db import models


class Staff(models.Model):
    GENDER_CHOICES = [
        ("male", "男性 / Homem / Male"),
        ("female", "女性 / Mulher / Female"),
    ]
    MARITAL_STATUS_CHOICES = [
        ("single", "未婚 / Solteiro(a) / Single"),
        ("married", "既婚 / Casado(a) / Married"),
    ]
    NATIONALITY_CHOICES = [
        ("japan", "日本 / Japão / Japan"),
        ("brazil", "ブラジル / Brazil"),
        ("philippines", "フィリピン / Philippines"),
        ("peru", "ペルー / Peru"),
        ("vietnam", "ベトナム / Vietnam"),
        ("other", "その他 / Outros / Other"),
    ]
    VISA_CHOICES = [
        ("permanent", "永住者 / Visto Permanente / Permanent Resident"),
        ("long_term", "定住者 / Visto com prazo de validade / Long-Term Resident"),
        ("spouse_jp", "日本人の配偶者等 / Cônjuge ou Filho de Japonês / Spouse or Child of Japanese National"),
        ("spouse_pr", "永住者の配偶者等 / Cônjuge ou Filho de Residente Permanente / Spouse or Child of Permanent Resident"),
        ("designated", "特定活動 / Atividades Designadas / Work Visa"),
        ("other", "その他 / Outros / Other"),
    ]
    STATUS_CHOICES = [
        ("standby", "稼働待ち（登録済）"),
        ("working", "稼働中"),
        ("inactive", "退職・休止"),
    ]

    full_name = models.CharField("1. 名前 / Nome / Name", max_length=100)
    age = models.PositiveIntegerField("2. 年齢 / Idade / Age", null=True, blank=True)
    phone = models.CharField("3. 携帯番号 / Numero de Telefone / Cell phone number", max_length=30)
    postal_code = models.CharField("4. 〒 郵便番号 / Caixa postal / postal cod", max_length=20, blank=True)
    address = models.CharField("5. 住所 / Endereço / Address", max_length=255, blank=True)
    gender = models.CharField("6. 性別 / Sexo / Gender", max_length=10, choices=GENDER_CHOICES, blank=True)
    marital_status = models.CharField("婚姻状況 / Estado civil / Marital status", max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True)
    birth_date = models.CharField("7. 生年月日 / Data de nascimento (yyyymmdd) / Date of birth (YYYYMMDD)", max_length=12, blank=True)
    nationality = models.CharField("8. 国籍 / Nacionalidade / Nationality", max_length=30, choices=NATIONALITY_CHOICES, blank=True)
    visa_type = models.CharField("9. ビザの種類 / Tipo do Visto / Visa type", max_length=30, choices=VISA_CHOICES, blank=True)
    status = models.CharField("稼働ステータス", max_length=20, choices=STATUS_CHOICES, default="standby")
    created_at = models.DateTimeField("登録日時", auto_now_add=True)

    class Meta:
        verbose_name = "スタッフ"
        verbose_name_plural = "スタッフ一覧"

    def __str__(self):
        return f"{self.full_name} ({self.get_nationality_display()})"


class SkillSheet(models.Model):
    YES_NO_CHOICES = [
        ("yes", "はい / Yes"),
        ("no", "いいえ / No"),
    ]
    YES_NO_MAYBE_CHOICES = [
        ("yes", "はい / Yes"),
        ("no", "いいえ / No"),
        ("maybe", "予定が合えば対応可 / Às vezes posso / Available upon request"),
    ]
    COMMUTE_CHOICES = [
        ("car", "車 / Carro / Car"),
        ("shuttle", "送迎 / Souguei / Transportation"),
        ("moto", "バイク / Moto / Motorcycle"),
        ("bicycle", "自転車 / Bicicleta / Bicycle"),
        ("walk", "徒歩 / A pé / Walking"),
        ("other", "その他 / Outros / Other"),
    ]
    OVERTIME_CHOICES = [
        ("0h", "0h"),
        ("1h", "1h"),
        ("2h", "2h"),
        ("3h", "3h"),
        ("any", "何時間でも対応可 / Sem preferência / Any time"),
    ]
    LEAVE_REASON_CHOICES = [
        ("", "選択してください / Selecione"),
        ("personal", "自己都合 / Motivos pessoais / Personal reasons"),
        ("contract_end", "契約満了 / Término de contrato / End of contract"),
        ("other", "その他 / Outros / Other"),
    ]
    JP_LEVEL_CHOICES = [
        ("0%", "0%"),
        ("10%", "10%"),
        ("25%", "25%"),
        ("50%", "50%"),
        ("75%", "75%"),
        ("100%", "100%"),
    ]
    SIZE_CHOICES = [
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("LL", "LL"),
        ("3L", "3L"),
        ("4L", "4L"),
        ("5L", "5L"),
    ]

    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name="skillsheet", verbose_name="スタッフ")

    # 通勤・勤務条件 (10〜15)
    drivers_license = models.CharField("10. 日本車免許 / Habilitação Japonesa / Japanese driver's license", max_length=10, choices=YES_NO_CHOICES, blank=True)
    commute_method = models.CharField("11. 通勤方法 / Método de trajeto / Mode of transportation", max_length=20, choices=COMMUTE_CHOICES, blank=True)
    commute_other = models.CharField("11-2. 通勤方法（その他詳細）", max_length=100, blank=True)
    overtime = models.CharField("12. 残業 / Horas extras / Overtime", max_length=10, choices=OVERTIME_CHOICES, blank=True)
    holiday_work = models.CharField("13. 休日出勤 / Trabalho no dia de folga / Holiday work", max_length=10, choices=YES_NO_MAYBE_CHOICES, blank=True)
    early_shift = models.CharField("14. 早出 / Entrada antecipada / Early shift", max_length=10, choices=YES_NO_MAYBE_CHOICES, blank=True)
    preferred_shift = models.CharField("15. 希望勤務時間 / Horário de trabalho desejado / Preferred working hours", max_length=200, blank=True)

    # 職歴 ①
    wh1_company = models.CharField("① 会社名 / Nome da empresa / Company name", max_length=150, blank=True)
    wh1_job = models.CharField("① 業務内容 / Tipo de serviço / Job description", max_length=200, blank=True)
    wh1_period = models.CharField("① 期間 / Tempo de trabalho / Employment period", max_length=100, blank=True)
    wh1_agency = models.CharField("① 派遣会社 / Empreiteira / Staffing agency", max_length=150, blank=True)
    wh1_wage = models.CharField("① 時給 / Salário por hora / Hourly wage", max_length=50, blank=True)
    wh1_reason = models.CharField("① 退職理由 / Motivo da saída / Reason for leaving", max_length=30, choices=LEAVE_REASON_CHOICES, blank=True)
    wh1_reason_other = models.CharField("① 退職理由（その他）", max_length=150, blank=True)

    # 職歴 ②
    wh2_company = models.CharField("② 会社名 / Nome da empresa / Company name", max_length=150, blank=True)
    wh2_job = models.CharField("② 業務内容 / Tipo de serviço / Job description", max_length=200, blank=True)
    wh2_period = models.CharField("② 期間 / Tempo de trabalho / Employment period", max_length=100, blank=True)
    wh2_agency = models.CharField("② 派遣会社 / Empreiteira / Staffing agency", max_length=150, blank=True)
    wh2_wage = models.CharField("② 時給 / Salário por hora / Hourly wage", max_length=50, blank=True)
    wh2_reason = models.CharField("② 退職理由 / Motivo da saída / Reason for leaving", max_length=30, choices=LEAVE_REASON_CHOICES, blank=True)
    wh2_reason_other = models.CharField("② 退職理由（その他）", max_length=150, blank=True)

    # 職歴 ③
    wh3_company = models.CharField("③ 会社名 / Nome da empresa / Company name", max_length=150, blank=True)
    wh3_job = models.CharField("③ 業務内容 / Tipo de serviço / Job description", max_length=200, blank=True)
    wh3_period = models.CharField("③ 期間 / Tempo de trabalho / Employment period", max_length=100, blank=True)
    wh3_agency = models.CharField("③ 派遣会社 / Empreiteira / Staffing agency", max_length=150, blank=True)
    wh3_wage = models.CharField("③ 時給 / Salário por hora / Hourly wage", max_length=50, blank=True)
    wh3_reason = models.CharField("③ 退職理由 / Motivo da saída / Reason for leaving", max_length=30, choices=LEAVE_REASON_CHOICES, blank=True)
    wh3_reason_other = models.CharField("③ 退職理由（その他）", max_length=150, blank=True)

    # 日本語力 (43〜45)
    jp_speaking = models.CharField("43. 日本語レベル / Nível de idioma japonês / Japanese proficiency", max_length=10, choices=JP_LEVEL_CHOICES, blank=True)
    jp_reading = models.CharField("44. 日本語 読み / Leitura em japonês / Japanese reading skills", max_length=10, choices=JP_LEVEL_CHOICES, blank=True)
    jp_writing = models.CharField("45. 日本語 書き / Escrita em japonês / Japanese writing skills", max_length=10, choices=JP_LEVEL_CHOICES, blank=True)

    # 作業服 (46〜48)
    uniform_jacket = models.CharField("46. 上着 / Camisa / Jacket", max_length=10, choices=SIZE_CHOICES, blank=True)
    uniform_pants = models.CharField("47. ズボン / Calça / Pants", max_length=10, choices=SIZE_CHOICES, blank=True)
    safety_shoes = models.CharField("48. 靴 / Sapato / Safety shoes", max_length=20, blank=True)

    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "スキルシート"
        verbose_name_plural = "スキルシート一覧"

    def __str__(self):
        return f"{self.staff.full_name} のスキルシート"


class RecruitmentCase(models.Model):
    STATUS_CHOICES = [
        ("open", "募集中"),
        ("interviewing", "選考・見学中"),
        ("closed", "充足・終了"),
    ]
    client_name = models.CharField("取引先企業名", max_length=150)
    title = models.CharField("案件・募集職種名", max_length=150)
    work_location = models.CharField("勤務地", max_length=150, blank=True)
    hourly_wage = models.CharField("時給・単価", max_length=50, blank=True)
    headcount = models.PositiveIntegerField("募集人数", default=1)
    status = models.CharField("ステータス", max_length=20, choices=STATUS_CHOICES, default="open")
    notes = models.TextField("備考・条件", blank=True)
    created_at = models.DateTimeField("作成日", auto_now_add=True)

    class Meta:
        verbose_name = "採用・案件"
        verbose_name_plural = "採用・案件一覧"

    def __str__(self):
        return f"{self.client_name} - {self.title}"


class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "未承認"),
        ("approved", "承認済"),
        ("rejected", "却下"),
    ]
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="スタッフ")
    leave_date = models.DateField("休暇希望日")
    reason = models.TextField("理由", blank=True)
    status = models.CharField("承認ステータス", max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField("申請日時", auto_now_add=True)

    class Meta:
        verbose_name = "休暇申請"
        verbose_name_plural = "休暇申請一覧"

    def __str__(self):
        return f"{self.staff.full_name} ({self.leave_date})"