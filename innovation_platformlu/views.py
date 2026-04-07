from urllib import request

from django.shortcuts import render, redirect
from innovation_platformlu.models import Submission
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # لو واجهتك CSRF بالجافاسكربت، نحلها بأفضل طريقة لاحقًا
from innovation_platformlu.models import Submission, Room
from .forms import SubmissionForm
from django.shortcuts import get_object_or_404


def home(request):
    if request.user.is_staff:
        qs = Submission.objects.all()
    elif request.user.is_authenticated:
        qs = Submission.objects.filter(created_by=request.user)
    else:
        # زائر: يعرض المشاركات اللي انضافت بدون تسجيل
        qs = Submission.objects.filter(created_by__isnull=True)

    counts = {
        "challenges": qs.filter(submission_type="challenge").count(),
        "ideas": qs.filter(submission_type="idea").count(),
        "innovations": qs.filter(submission_type="idea", status="done").count(),
        "ideas_in_progress": qs.filter(submission_type="idea").exclude(status="done").count(),
    }

    return render(request, "innovation/home.html", {"counts": counts})



def submit(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            # created_by: فقط إذا المستخدم مسجل دخول
            if request.user.is_authenticated:
               obj.created_by = request.user if request.user.is_authenticated else None
            else:
                obj.created_by = None

            # منطق حسب النوع
            if obj.submission_type == "challenge":
                obj.status = "new"     # التحدي: الحالة تلقائي
                obj.idea_name = ""     # تنظيف حقول الفكرة
            elif obj.submission_type == "idea":
                obj.challenge_title = ""  # تنظيف حقول التحدي

            obj.save()
            return redirect("platform2:home")
    else:
        form = SubmissionForm()

    return render(request, "innovation/submit.html", {"form": form})


def room_join(request):
    if request.method == "POST":
        code = (request.POST.get("code") or "").strip().upper()
        try:
            room = Room.objects.get(code=code, is_active=True)
        except Room.DoesNotExist:
            return render(request, "innovation/room_join.html", {"error": "الكود غير صحيح أو الغرفة غير مفعّلة."})

        request.session["room_code"] = room.code
        return redirect("platform2:board")

    return render(request, "innovation/room_join.html")


def board(request):
    
    code = request.session.get("room_code")
    if not code:
     return redirect('platform2:room_join')

    room = Room.objects.get(code=code)
    cards = Submission.objects.filter(room=room).order_by("-created_at")
    return render(request, "innovation/board.html", {"room": room, "cards": cards})

def board_add_challenge(request):
    return _board_add(request, "challenge")

def board_add_idea(request):
     from .forms import SubmissionForm   # استيراد محلي لتجنب circular import
     return _board_add(request, "idea")

def _board_add(request, submission_type):
    from .forms import SubmissionForm   # استيراد محلي لتجنب circular import

    code = request.session.get("room_code")
    if not code:
        return redirect('platform2:room_join')
    room = Room.objects.get(code=code)

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.submission_type = submission_type 
            obj.room = room


            obj.created_by = request.user if request.user.is_authenticated else None

            # قواعدك السابقة
            if obj.submission_type == "challenge":
                obj.status = "new"  # التحدي بدون status من المستخدم
                obj.idea_name = ""
            else:
                # idea: status يجي من المستخدم (حسب طلبك)
                obj.challenge_title = ""

            obj.save()
            return redirect("platform2:board")
    else:
        form = SubmissionForm(initial={"submission_type": submission_type})

    return render(request, "innovation/board_form.html", {"form": form, "mode": submission_type})

@require_POST
def update_layout(request, pk):
    try:
        s = Submission.objects.get(pk=pk)
        s.pos_x = int(request.POST.get("x"))
        s.pos_y = int(request.POST.get("y"))
        s.width = int(request.POST.get("w"))
        s.height = int(request.POST.get("h"))
        s.save(update_fields=["pos_x", "pos_y", "width", "height"])
        return JsonResponse({"ok": True})
    except Exception as e:
        return HttpResponseBadRequest("bad data")

@require_POST
def toggle_check(request, pk):
    s = Submission.objects.get(pk=pk)
    s.is_checked = not s.is_checked
    s.save(update_fields=["is_checked"])
    return JsonResponse({"ok": True, "checked": s.is_checked})

@require_POST
def board_delete(request, pk):
    obj = get_object_or_404(Submission, pk=pk)

   
    # حماية: غير الأدمن ما يحذف إلا حقه
    if (not request.user.is_staff) and obj.created_by_id != request.user.id:
        return HttpResponseForbidden("not allowed")

    obj.delete()
    return JsonResponse({"deleted": True})

@require_POST
def board_approve(request, pk):
    obj = get_object_or_404(Submission, pk=pk)

    # نعتمد الفكرة فقط
    if obj.submission_type == "idea":
        obj.status = "done"
        obj.save(update_fields=["status"])

    return JsonResponse({"approved": True, "status": obj.status})