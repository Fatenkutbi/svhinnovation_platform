from django.db import models

class Submission(models.Model):  # تأكدي من سبيرنج الكلمة هنا
    TYPE_CHOICES = [
        ('challenge', 'Challenge'),
        ('initiative', 'Initiative'),
        ('innovation', 'Innovation'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('review', 'Under Review'),
        ('progress', 'In Progress'),
        ('done', 'Completed'),
        ('archived', 'Archived'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BoardItem(models.Model):
    COLUMN_CHOICES = [
        ('define', 'Define'),
        ('ideate', 'Ideate'),
        ('prototype', 'Prototype'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    column = models.CharField(max_length=20, choices=COLUMN_CHOICES, default='define')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

    from django.db import models

class Submission(models.Model):
    TYPE_CHOICES = [('challenge', 'Challenge'), ('initiative', 'Initiative')]
    
    # قائمة الإدارات التي طلبتِها
    DEPT_CHOICES = [
        ('sandbox', 'إدارة الساندبوكس'),
        ('ai', 'إدارة الذكاء الاصطناعي'),
        ('consulting', 'الإدارة العامة للاستشارات الطبية'),
        ('cardiology', 'قسم القلب'),
        ('radiology', 'قسم الأشعة'),
        ('strokes', 'قسم الجلطات'),
        ('icu', 'قسم العناية المركزة'),
        ('hr', 'إدارة الموارد البشرية'),
        ('quality', 'إدارة الجودة'),
        ('shared_services', 'إدارة الخدمات المشتركة'),
        ('digital_empowerment', 'إدارة التمكين الرقمي'),
        ('data', 'إدارة البيانات'),
        ('finance', 'الإدارة المالية'),
        ('insurance', 'إدارة التأمين الصحي'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    department = models.CharField(max_length=50, choices=DEPT_CHOICES, default='sandbox') # الحقل الجديد
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BoardItem(models.Model):
    COLUMN_CHOICES = [('define', 'Define'), ('ideate', 'Ideate'), ('prototype', 'Prototype')]
    title = models.CharField(max_length=200)
    content = models.TextField()
    column = models.CharField(max_length=20, choices=COLUMN_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)