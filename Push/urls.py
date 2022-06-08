from django.urls import path, re_path
from Push import views

urlpatterns = [

    re_path(r'^sendMsg/$', views.SendMsg.as_view(), name=''),
]
