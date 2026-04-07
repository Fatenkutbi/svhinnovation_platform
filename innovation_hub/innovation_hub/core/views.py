from django.shortcuts import render, redirect
from .models import Submission, BoardItem
from django.http import HttpResponse
import openpyxl
import json  # ضروري لتحويل البيانات للرسم البياني

# صفحة لوحة التحكم (Dashboard)
def dashboard(request):
    # قائمة الإدارات مع الأيقونات (Font Awesome)
    dept_icons = {
        'sandbox': 'fa-vials',
        'ai': 'fa-robot',
        'consulting': 'fa-user-md',
        'cardiology': 'fa-heartbeat',
        'radiology': 'fa-x-ray',
        'strokes': 'fa-brain',
        'icu': 'fa-procedures',
        'hr': 'fa-users-cog',
        'quality': 'fa-clipboard-check',
        'shared_services': 'fa-handshake',
        'digital_empowerment': 'fa-laptop-medical',
        'data': 'fa-database',
        'finance': 'fa-file-invoice-dollar',
        'insurance': 'fa-shield-halved',
    }

    dept_stats = []
    labels_list = []
    data_list = []

    # حساب الإحصائيات لكل إدارة
    for code, name in Submission.DEPT_CHOICES:
        count = Submission.objects.filter(department=code).count()
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
        # تحويل البيانات لصيغة JSON ليتمكن الـ JavaScript في المتصفح من قراءتها
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
    sheet.append(['العنوان', 'النوع', 'الإدارة', 'تاريخ الرفع'])
    
    for item in Submission.objects.all():
        # الحصول على الاسم المقروء للإدارة والنوع من الاختيارات
        sheet.append([
            item.title, 
            item.get_type_display(), 
            item.get_department_display(), 
            item.created_at.replace(tzinfo=None)
        ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Innovation_Report.xlsx'
    workbook.save(response)
    return response

# صفحة تقارير Power BI
def powerbi_page(request):
    return render(request, 'powerbi.html')

