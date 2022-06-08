from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from Auth import views

urlpatterns = [

    re_path(r'^login/$', views.Login.as_view(), name='user_list'),
    re_path(r'^register/$', views.Register.as_view(), name='register'),
    re_path(r'^badge/$', views.Badge.as_view(), name='register'),
    re_path(r'^check/$', views.Check.as_view(), name='register'),

    re_path(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #re_path(r'^token/$', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]