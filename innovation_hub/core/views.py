from django.shortcuts import render, redirect
from innovation_platformlu.models import Submission
from .models import BoardItem
from django.http import HttpResponse
import openpyxl
import json  # ضروري لتحويل البيانات للرسم البياني

# صفحة لوحة التحكم (Dashboard)
def dashboard(request):
    # قائمة الإدارات مع الأيقونات (Font Awesome)
    dept_icons = {
        'sandbox': 'fa-vials',
        'ai': 'fa-robot',
        'medical_consulting': 'fa-user-md',
        'cardiology': 'fa-heartbeat',
        'radiology': 'fa-x-ray',
        'stroke': 'fa-brain',
        'icu': 'fa-procedures',
        'hr': 'fa-users-cog',
        'quality': 'fa-clipboard-check',
        'shared_services': 'fa-handshake',
        'digital_enablement': 'fa-laptop-medical',
        'data': 'fa-database',
        'finance': 'fa-file-invoice-dollar',
        'insurance': 'fa-shield-halved',
    }

    dept_stats = []
    labels_list = []
    data_list = []

    # حساب الإحصائيات لكل إدارة
    for code, name in Submission.ADMINISTRATION_DEPARTMENT_CHOICES:
        count = Submission.objects.filter(administration_department=code).count()
        dept_stats.append({
            'name': name,
            'count': count,
            'icon': dept_icons.get(code, 'fa-building')
        })
        labels_list.append(name)
        data_list.append(count)

    total = Submission.objects.count()

    context = {
        'dept_stats': dept_stats,
        'total': total,
        'chart_labels': json.dumps(labels_list),
        'chart_data': json.dumps(data_list),
    }
    return render(request, 'dashboard.html', context)
# صفحة عرض التحديات والمبادرات (Submissions)
def submissions(request):
    data = Submission.objects.all().order_by('-created_at')
    return render(request, 'submissions.html', {'data': data})

# صفحة لوحة الورشة التفاعلية (Board)
def board(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        column = request.POST.get('column')
        BoardItem.objects.create(title=title, content=content, column=column)
        return redirect('/board/')

    context = {
        'define_items': BoardItem.objects.filter(column='define'),
        'ideate_items': BoardItem.objects.filter(column='ideate'),
        'prototype_items': BoardItem.objects.filter(column='prototype'),
    }
    return render(request, 'board.html', context)

# ميزة تصدير البيانات إلى ملف Excel
def export_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "مبادرات الابتكار"

    # رؤوس الأعمدة
    sheet.append([
        'العنوان',
        'النوع',
        'الإدارة / القسم',
        'المجال',
        'مستوى التأثير',
        'الحالة',
        'وصف التحدي / الفكرة',
        'هل يوجد حل مقترح؟',
        'الحل المقترح',
        'ملاحظات التحدي',
        'التقنيات المستخدمة',
        'اسم الفكرة',
        'تاريخ الإطلاق',
        'قائد الفكرة / الفريق',
        'وصف الفكرة',
        'نوع الفكرة',
        'مرحلة الفكرة',
        'ملاحظات الفكرة',
        'تاريخ الإضافة',
    ])

    for item in Submission.objects.all().order_by('-created_at'):
        title = item.challenge_title or item.idea_name or "بدون عنوان"

        sheet.append([
            title,
            item.get_submission_type_display(),
            item.get_administration_department_display() if item.administration_department else '',
            item.get_domain_display() if item.domain else '',
            item.get_impact_display() if item.impact else '',
            item.get_status_display() if item.status else '',
            item.challenge_description or item.idea_description or '',
            'نعم' if item.has_suggested_solution else 'لا',
            item.suggested_solution or '',
            item.challenge_notes or '',
            item.technologies_used or '',
            item.idea_name or '',
            item.idea_launch_date.strftime('%Y-%m-%d') if item.idea_launch_date else '',
            item.idea_leader_or_team or '',
            item.idea_description or '',
            item.get_idea_type_display() if item.idea_type else '',
            item.get_idea_stage_display() if item.idea_stage else '',
            item.idea_notes or '',
            item.created_at.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M'),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=Innovation_Report.xlsx'
    workbook.save(response)
    return response

# صفحة تقارير Power BI
def powerbi_page(request):
    return render(request, 'powerbi.html')

