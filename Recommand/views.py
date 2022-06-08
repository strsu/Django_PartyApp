import enum
#from plistlib import UID
#from telnetlib import STATUS
from unicodedata import category
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash # 나중에 비밀번호 바꿀때 사용
from django.http import Http404
from django.utils import timezone # 장고 서버 시간
from django.conf import settings

from django.db.models import Max, Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from backend.models import (
    Filter,
    User,
    Userprofile
)

from backend.serializers import (
    BoardaddonSerializer
)

import time
import base64
import random

# Create your views here.
class UserDetail(APIView):
    def get(self, request):
        userUUID = bytes.fromhex(request.GET['useruuid'])
        userprofileQuery = Userprofile.objects.prefetch_related().get(up_useruuid = userUUID)

        filterQuery = Filter.objects.prefetch_related().filter(f_sort='profile')
        
        json = {}

        json["name"]       = userprofileQuery.up_name      
        json["sex"]        = userprofileQuery.up_sex       
        json["birth"]      = userprofileQuery.up_birth     
        json["height"]     = userprofileQuery.up_height    
        json["body"]       = filterQuery.get(f_type='체형', f_seq=userprofileQuery.up_body).f_name
        json["edu"]        = filterQuery.get(f_type='학력', f_seq=userprofileQuery.up_edu).f_name
        json["eduname"]    = userprofileQuery.up_eduname   
        json["live"]       = userprofileQuery.up_live      
        json["religion"]   = filterQuery.get(f_type='종교', f_seq=userprofileQuery.up_religion).f_name
        json["smoke"]      = filterQuery.get(f_type='흡연', f_seq=userprofileQuery.up_smoke).f_name
        json["alcohol"]    = filterQuery.get(f_type='음주', f_seq=userprofileQuery.up_alcohol).f_name
        json["nickname"]   = userprofileQuery.up_nickname
        json["selfintro"]  = userprofileQuery.up_selfintro
        json["character"]  = userprofileQuery.up_character
        json["hobby"]      = userprofileQuery.up_hobby
        json["interest"]   = userprofileQuery.up_interest
        json["datestyle"]  = userprofileQuery.up_datestyle
        json["requirepic"] = userprofileQuery.up_requirepic[1:-1].replace('"','').split(',')
        json["extrapic"]   = userprofileQuery.up_extrapic[1:-1].replace('"','').split(',')

        arr = []
        for val in json["requirepic"]:
            if val != '':
                arr.append(settings.MEDIA_URL + '?imageName=requirePic ' + val)
        json["requirepic"] = arr

        arr = []
        for val in json["extrapic"]:
            if val != '':
                arr.append(settings.MEDIA_URL + '?imageName=extrapic ' + val)
        json["extrapic"] = arr

        return Response(json)