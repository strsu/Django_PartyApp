from django.urls import path, re_path
from Anony import views

urlpatterns = [

    re_path(r'^board/$', views.Board.as_view(), name='user_list'),
    re_path(r'^comment/$', views.BoardComment.as_view(), name='user_list'),
    re_path(r'^category/$', views.Category.as_view(), name='user_list'),
]