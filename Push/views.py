#from plistlib import UID
#from telnetlib import STATUS
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash # 나중에 비밀번호 바꿀때 사용
from django.utils import timezone # 장고 서버 시간
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from backend.models import (
    Firebasetoken,
    User
)

from backend.firebase import (
    send_to_firebase_cloud_messaging,
    send_to_firebase_cloud_notification
)

import json
import requests

# Create your views here.
class SendMsg(APIView):
    def post(self, request):
        

        # 앱 자체에서 온라인 오프라인 판단을 안해주면 아래 주석 코드 방식으로 해야한다.
        '''
        json_ = {
            'user':request.data['to'],
            'host':'localhost'
        }
        res = requests.post('http://192.168.1.243:5280/api/user_resources', data=json.dumps(json_))

        # 온라인 유저는 len(res.json())가 0이 아니어야 한다.
        # 연결된 자원이 있기 때문에
        # 0이라면 오프라인이기 때문에 푸쉬를 넣어준다.
        if res.status_code == 200 and len(res.json()) == 0:
            print('@@@@@@', request.data['to'][4:])
            try:
                userQuery = User.objects.get(u_uid=request.data['to'][4:])
                fireQuery = Firebasetoken.objects.get(fbt_useruuid=userQuery.u_uuid)
                # 게시글 작성자한테 댓글 달렸다고 푸쉬알림 보내기
                send_to_firebase_cloud_messaging(fireQuery.fbt_usertoken, f'{request.data["from"]}', f'{request.data["msg"]}')
                return Response( status=status.HTTP_200_OK )
            except Exception:
                return Response( status=status.HTTP_400_BAD_REQUEST )'''

        try:
            userQuery = User.objects.get(u_uid=request.data['to'][4:])
            fireQuery = Firebasetoken.objects.get(fbt_useruuid=userQuery.u_uuid)
            # 게시글 작성자한테 댓글 달렸다고 푸쉬알림 보내기
            send_to_firebase_cloud_messaging(fireQuery.fbt_usertoken, f'{request.data["from"]}', '채팅: '+f'{request.data["msg"]}')
            return Response( status=status.HTTP_200_OK )
        except Exception:
            return Response( status=status.HTTP_400_BAD_REQUEST )