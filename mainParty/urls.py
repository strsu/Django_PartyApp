from django.urls import path, re_path
from mainParty import views

urlpatterns = [

    re_path(r'^board/$', views.Board.as_view(), name=''),
    re_path(r'^review/$', views.Review.as_view(), name=''),
    re_path(r'^qna/$', views.QNA.as_view(), name=''),
    re_path(r'^category/$', views.Category.as_view(), name=''),
]