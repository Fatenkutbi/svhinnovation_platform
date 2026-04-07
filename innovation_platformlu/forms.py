from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from innovation_platformlu.models import Submission



BASE = "w-full border rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-sky-100 bg-white"



class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = [
            "submission_type",
            "administration_department",
            "department",
            "domain",
            "impact",
            "status",  # نخليه موجود لكن نتحكم بمتى يصير required

            "challenge_date",
            "challenge_title",
            "challenge_description",
            "has_suggested_solution",
            "suggested_solution",
            "challenge_notes",

            "idea_name",
            "idea_launch_date",
            "idea_leader_or_team",
            "idea_description",
            "idea_type",
            "idea_stage",
            "stage",
            "technologies_used",
            "idea_notes",
        ]

        widgets = {
            "submission_type": forms.Select(attrs={"class": BASE}),
            "administration_department": forms.Select(attrs={"class": BASE}),
            "department": forms.Select(attrs={"class": BASE}),
            "domain": forms.Select(attrs={"class": BASE}),
            "impact": forms.Select(attrs={"class": BASE}),
            "status": forms.Select(attrs={"class": BASE}),  # مهم

            "challenge_date": forms.DateInput(attrs={"type": "date", "class": BASE}),
            "challenge_title": forms.TextInput(attrs={"class": BASE}),
            "challenge_description": forms.Textarea(attrs={"class": BASE, "rows": 4}),
            "has_suggested_solution": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "suggested_solution": forms.Textarea(attrs={"class": BASE, "rows": 3}),
            "challenge_notes": forms.Textarea(attrs={"class": BASE, "rows": 3}),

            "idea_name": forms.TextInput(attrs={"class": BASE}),
            "idea_launch_date": forms.DateInput(attrs={"type": "date", "class": BASE}),
            "idea_leader_or_team": forms.TextInput(attrs={"class": BASE}),
            "idea_description": forms.Textarea(attrs={"class": BASE, "rows": 4}),
            "idea_type": forms.Select(attrs={"class": BASE}),
            "idea_stage": forms.Select(attrs={"class": BASE}),
            "stage": forms.TextInput(attrs={"class": BASE}),
            "technologies_used": forms.TextInput(attrs={"class": BASE}),
            "idea_notes": forms.Textarea(attrs={"class": BASE, "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["submission_type"].required = False

        st = (self.data.get("submission_type")
              or getattr(self.instance, "submission_type", None)
              or self.initial.get("submission_type"))

        # الافتراضي: status مو مطلوب (مفيد للتحدي)
        self.fields["status"].required = False

        # إذا "فكرة/حل" نخليه مطلوب
        if st == "idea":
            self.fields["status"].required = True