from django.contrib import admin
from .models import Submission, BoardItem # تأكدي من وجود الفاصلة والاسم الصحيح

admin.site.register(Submission)
admin.site.register(BoardItem)