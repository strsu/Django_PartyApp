from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from media import views

urlpatterns = [
    re_path(r'^image/$', views.Image.as_view(), name='user_list'),
    re_path(r'^image2/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]