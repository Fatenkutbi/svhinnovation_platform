from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
import string


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


# صفحة البورد
def generate_room_code(length=6):
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class Room(models.Model):
    code = models.CharField(max_length=10, unique=True, default=generate_room_code)
    title = models.CharField(max_length=150, blank=True, default="")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.code


class Submission(models.Model):
    # Choices
    DOMAIN_CHOICES = [
        ("health", "صحي"),
        ("operational", "تشغيلي"),
        ("technical", "تقني"),
        ("service", "خدمي"),
        ("financial", "مالي"),
        ("administrative", "إداري"),
        ("research", "بحثي/تطوير"),
        ("other", "أخرى"),
    ]

    IDEA_TYPE_CHOICES = [
        ("service_improvement", "تحسين خدمة"),
        ("tech_product", "منتج / حل تقني"),
        ("process_improvement", "تحسين إجراء"),
        ("ux", "تجربة مستخدم"),
        ("rnd", "بحث / تطوير"),
    ]

    IDEA_STAGE_CHOICES = [
        ("study", "قيد الدراسة"),
        ("progress", "قيد التنفيذ"),
        ("done", "مكتملة"),
        ("stopped", "متوقفة"),
    ]

    TYPE_CHOICES = [
        ("challenge", "مشكلة/تحدي"),
        ("idea", "فكرة/حل"),
    ]

    IMPACT_CHOICES = [
        ("low", "منخفض"),
        ("medium", "متوسط"),
        ("high", "عالي"),
    ]

    STATUS_CHOICES = [
        ("new", "جديد"),
        ("review", "قيد المراجعة"),
        ("progress", "قيد التنفيذ"),
        ("done", "منفذ"),
    ]

    ADMINISTRATION_DEPARTMENT_CHOICES = [
        ("sandbox", "ادارة الساندبوكس"),
        ("ai", "ادارة الذكاء الاصطناعي"),
        ("medical_consulting", "الادارة العامة للاستشارات الطبية"),
        ("cardiology", "قسم القلب"),
        ("radiology", "قسم الاشعة"),
        ("stroke", "قسم الجلطات"),
        ("icu", "قسم العناية المركزة"),
        ("hr", "ادارة الموارد البشرية"),
        ("quality", "ادارة الجودة"),
        ("shared_services", "ادارة الخدمات المشتركة"),
        ("digital_enablement", "ادارة التمكين الرقمي"),
        ("data", "ادارة البيانات"),
        ("finance", "الادارة المالية"),
        ("insurance", "ادارة التامين الصحي"),
    ]

    # عام
    submission_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="challenge",
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ الحقل الجديد لليست الإدارة / القسم
    administration_department = models.CharField(
        max_length=100,
        choices=ADMINISTRATION_DEPARTMENT_CHOICES,
        blank=True,
        default="",
    )

    # أبقيته مثل ما هو حتى ما نخرب أي شيء قديم عندك
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    domain = models.CharField(
        max_length=30,
        choices=DOMAIN_CHOICES,
        blank=True,
        default="",
    )

    impact = models.CharField(
        max_length=10,
        choices=IMPACT_CHOICES,
        default="medium",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    # Layout on board
    pos_x = models.IntegerField(default=40)
    pos_y = models.IntegerField(default=40)
    width = models.IntegerField(default=520)
    height = models.IntegerField(default=320)

    # check / pin
    is_checked = models.BooleanField(default=False)

    # حقول التحديات (Excel 1)
    challenge_date = models.DateField(null=True, blank=True)
    challenge_title = models.CharField(max_length=200, blank=True, default="")
    challenge_description = models.TextField(blank=True, default="")
    has_suggested_solution = models.BooleanField(default=False)
    suggested_solution = models.TextField(blank=True, default="")
    challenge_notes = models.TextField(blank=True, default="")
    technologies_used = models.CharField(max_length=255, blank=True, default="")

    # حقول الأفكار/الحلول (Excel 2)
    idea_name = models.CharField(max_length=220, blank=True, default="")
    idea_launch_date = models.DateField(null=True, blank=True)
    idea_leader_or_team = models.CharField(max_length=220, blank=True, default="")
    idea_description = models.TextField(blank=True, default="")
    idea_type = models.CharField(
        max_length=40,
        choices=IDEA_TYPE_CHOICES,
        blank=True,
        default="",
    )
    idea_stage = models.CharField(
        max_length=20,
        choices=IDEA_STAGE_CHOICES,
        blank=True,
        default="",
    )

    # (هذه حقول إضافية عندك - خليتها مثل ما هي)
    stage = models.CharField(max_length=150, blank=True, default="")
    idea_notes = models.TextField(blank=True, default="")

    # AI output لاحقًا للأدمن
    ai_solutions = models.TextField(blank=True, default="")

    def __str__(self):
        name = self.challenge_title or self.idea_name or "Submission"
        return f"{self.get_submission_type_display()} - {name}"