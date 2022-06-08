from django.urls import path, re_path
from Recommand import views

urlpatterns = [

    re_path(r'^userdetail/$', views.UserDetail.as_view(), name='')
]