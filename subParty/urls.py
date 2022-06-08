from django.urls import path, re_path
from subParty import views

urlpatterns = [

    re_path(r'^board/$', views.Board.as_view(), name=''),
    re_path(r'^category/$', views.Category.as_view(), name=''),
    re_path(r'^addon/$', views.Addon.as_view(), name=''),
    re_path(r'^apply/$', views.Apply.as_view(), name=''),
    re_path(r'^myparty/$', views.MyParty.as_view(), name=''),
    re_path(r'^myattend/$', views.MyAttend.as_view(), name=''),
    re_path(r'^mydibs/$', views.MyDibs.as_view(), name=''),
    re_path(r'^userdetail/$', views.UserDetail.as_view(), name=''),
    re_path(r'^usersimpledetail/$', views.UserSimpleDetail.as_view(), name=''),
]
