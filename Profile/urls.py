from django.urls import path, re_path
from Profile import views

urlpatterns = [

    re_path(r'^filter/$', views.FilterList.as_view(), name=''),
    re_path(r'^myfilter/$', views.MYFilterList.as_view(), name='')
]