from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('submissions/', views.submissions),
    path('board/', views.board),
    path('excel/', views.export_excel),
    path('powerbi/', views.powerbi_page),
    path('board/', views.board),

]
