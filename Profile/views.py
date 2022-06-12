#from plistlib import UID
#from telnetlib import STATUS
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenVerifyView

from backend.models import Userprofile, Filter, User
from backend.serializers import UserprofileSerializer, FilterSerializer

from tokenVerify import verify
import json

# Create your views here.
class FilterList(APIView):
    def get(self, request):
        #userQuery = Userprofile.objects.get(up_uid=bytes.fromhex(request.headers['uuid']))
        filerQuesry = Filter.objects.filter(f_sort='profile')
        return Response( FilterSerializer(filerQuesry, many=True).data ,status=status.HTTP_200_OK )

class MYFilterList(APIView):
    def get(self, request):
        userQuery = User.objects.get(u_uuid=bytes.fromhex(request.headers['uuid']))
        userProfileQuery = Userprofile.objects.get(up_useruuid=bytes.fromhex(request.headers['uuid']))
        filerQuesry = Filter.objects.filter(f_sort='profile')
        _json = {
            'name': userProfileQuery.up_name,
            'sex': userProfileQuery.up_sex,
            'birth': userProfileQuery.up_birth,
            'height': userProfileQuery.up_height,
            'body': userProfileQuery.up_body,
            'edu': userProfileQuery.up_edu,
            'eduname': userProfileQuery.up_eduname,
            'live': userProfileQuery.up_live,
            'religion': userProfileQuery.up_religion,
            'smoke': userProfileQuery.up_smoke,
            'alcohol': userProfileQuery.up_alcohol,
            'nickname': userProfileQuery.up_nickname,
            'selfintro': userProfileQuery.up_selfintro,
            'character': userProfileQuery.up_character,
            'hobby': userProfileQuery.up_hobby,
            'interest': userProfileQuery.up_interest,
            'datestyle': userProfileQuery.up_datestyle,
            'requirepic': '',
            'extrapic': '',
            'mainpic': '',
            'phone': userQuery.u_phone,
            'email': userQuery.u_id,
        }
    
        if userQuery.u_mainpic:
            _json['mainpic'] = 'mainPic ' + userQuery.u_mainpic.replace('"', '')
        if userProfileQuery.up_requirepic:
            img_list = []
            for img in userProfileQuery.up_requirepic[1:-1].split(','):
                img = img.replace('"', '')
                if img != '':
                    img_list.append('requirePic '+img)
                else:
                    img_list.append('')
            _json['requirepic'] = img_list
        if userProfileQuery.up_extrapic:
            img_list = []
            for img in userProfileQuery.up_extrapic[1:-1].split(','):
                img = img.replace('"', '')
                if img != '':
                    img_list.append('extraPic '+img)
                else:
                    img_list.append('')
            _json['extrapic'] = img_list

        return Response( {
            'filter': FilterSerializer(filerQuesry, many=True).data,
            'my': _json
        } ,status=status.HTTP_200_OK )

class Profile(APIView):
    def put(self, request):
        userQuery = Userprofile.objects.get(up_useruuid=bytes.fromhex(request.headers['uuid']))
        info = request.data['info']
        try:
            userQuery.up_height = info['Height']
            userQuery.up_body = info['Body']
            userQuery.up_edu = info['Grade']
            userQuery.up_eduname = info['eduname']
            userQuery.up_live = f"{info['Region']} {info['RegionAddon']}"
            userQuery.up_religion = info['Religion']
            userQuery.up_smoke = info['Smoke']
            userQuery.up_alcohol = info['Alcohol']
            userQuery.up_selfintro = info['aboutMe']
            userQuery.up_character = info['character']
            userQuery.save()
            return Response( status=status.HTTP_200_OK )
        except Exception:
            print(Exception)
            return Response( status=status.HTTP_400_BAD_REQUEST )