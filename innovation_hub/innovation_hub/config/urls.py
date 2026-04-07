from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # روابط المنصة الأولى (تطبيق core)
    path('', include('core.urls')), 
    
    # روابط المنصة الثانية (تطبيق innovation_platformlu)

    path('platform2/', include('innovation_platformlu.urls')),