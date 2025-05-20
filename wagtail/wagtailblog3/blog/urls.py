# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('api/reactions/<int:page_id>/toggle/', views.toggle_reaction, name='toggle_reaction'),
    path('api/reactions/<int:page_id>/counts/', views.get_reaction_counts, name='get_reaction_counts'),
]