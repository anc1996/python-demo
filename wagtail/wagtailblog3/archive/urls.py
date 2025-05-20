# archive/urls.py
from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('api/archives/', views.archives_api, name='archives_api'),
    path('year/<int:year>/', views.year_archive, name='year_archive'),
    path('year/<int:year>/month/<int:month>/', views.month_archive, name='month_archive'),
]