from django.contrib import admin
from innovation_platformlu.models import Submission, Department, Domain


@admin.action(description="✅ تحويل (فكرة) مكتملة إلى (ابتكار)")
def move_done_ideas_to_innovations(modeladmin, request, queryset):
    queryset.filter(submission_type="idea", progress_percent=100).update(submission_type="innovation", status="done")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "submission_type", "department", "domain", "impact", "status", "created_by", "created_at",
        "challenge_title", "idea_name",
    )
    list_filter = ("submission_type", "impact", "status", "department", "domain")
    search_fields = ("challenge_title", "idea_name", "challenge_description", "idea_description")
    actions = [move_done_ideas_to_innovations]


admin.site.register(Department)
admin.site.register(Domain)
