from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('', lambda request: redirect('/dashboard/')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')), 
    path('platform2/', include('innovation_platformlu.urls')), 
]