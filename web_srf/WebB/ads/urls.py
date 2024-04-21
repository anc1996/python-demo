from django.urls import re_path,include
from ads import views

urlpatterns = [
    re_path(r'^$',views.AdsView.as_view()),
]