#from plistlib import UID
#from telnetlib import STATUS
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash # 나중에 비밀번호 바꿀때 사용
from django.http import Http404
from django.utils import timezone # 장고 서버 시간
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from Auth.models import (
    User, 
    Firebasetoken, 
    Userauthlist,
    Userjwttoken,
    Userprofile
    )
from Auth.serializers import (
    MyTokenObtainPairSerializer, 
    UserSerializer,
    UserprofileSerializer,
    AuthUserSerializer,
    FirebasetokenSerializer,
    UserauthlistSerializer,
    UserjwttokenSerializer
    )

import bcrypt
import base64, json
import time

from backend.views import verify_token, refrech_token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
#@csrf_exempt # 클래스에서는 데코레이터 사용 못함
class Login(APIView):
    permission_classes = (AllowAny,) # login만 권한 없이 접속 가능
    '''def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404'''
    
    def post(self, request, format=None):
        if 'accessToken' in request.data:
            val = request.data['accessToken'].split('.')[1]
            val_bytes = base64.b64decode(val + '=' * (-len(val) % 4))
            uuid = json.loads(val_bytes.decode('ascii'))['uuid']
            uuid = bytes.fromhex(uuid)

            if not verify_token(request.data['accessToken']): # 토큰 미유효
                jwtQuery = Userjwttoken.objects.get(ujt_useruuid = uuid) # 저장된 리프레쉬 토큰 가져온다
                request.data['accessToken'] = refrech_token(jwtQuery.ujt_key)
                

            user = User.objects.filter(u_uuid=uuid).first()
            userprofileQuery = Userprofile.objects.get(up_useruuid=uuid)
            firebase = Firebasetoken.objects.get(fbt_useruuid=user.u_uuid)

            response = Response(
                {
                    "uid": UserSerializer(user).data["u_uid"],
                    "uuid": user.u_uuid.hex(),
                    "grade": UserSerializer(user).data["u_grade"],
                    "sex": UserSerializer(user).data["u_sex"],
                    'mainpic': 'mainPic '+UserSerializer(user).data["u_mainpic"].replace('\"', ''),
                    'nickname': userprofileQuery.up_nickname,
                    "fcmToken": firebase.fbt_usertoken,
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie("access_token", request.data['accessToken'], httponly=True)

            return response

        else:
            id = request.data['id']
            pw = request.data['pw'].encode('utf-8')
            #users = User.objects.all()

            user = User.objects.filter(u_id=id).first()

            if user is None: # 유저가 없는경우
                return Response(
                    {'Message': '존재하지않는 id입니다.'}, status=status.HTTP_400_BAD_REQUEST
                )
            
            if not bcrypt.checkpw(pw, (user.u_pw).encode('utf-8')): # 비밀번호가 틀린경우
                return Response(
                    {'Message': '비밀번호가 틀렸습니다.'}, status=status.HTTP_400_BAD_REQUEST
                )

            if user is not None:

                firebase = Firebasetoken.objects.filter(fbt_useruuid=user.u_uuid).first()
                if firebase is None: # 첫 로그인, DB에 토큰이 없는 경우
                    fdata = {
                        'fbt_useruuid': user.u_uuid,
                        'fbt_usertoken': request.data['token'],
                        'fbt_generdate': str(timezone.now()).split('.')[0]
                    }
                    fserializer = FirebasetokenSerializer(data=fdata)
                    if fserializer.is_valid(): # 데이터 유효성 검사
                        fserializer.save()
                    else:
                        print(fserializer.errors)
                else:
                    if firebase.fbt_usertoken != request.data['token']: # 토큰이 바뀐 경우, 디바이스 변경 등?
                        firebase.fbt_usertoken = request.data['token']
                        firebase.save()
                
                token = MyTokenObtainPairSerializer.get_token(user)
                try:
                    jwtQuery = Userjwttoken.objects.get(ujt_useruuid = user.u_uuid)
                    jwtQuery.ujt_key = str(token) # refrech 토큰 변경
                    jwtQuery.save()
                        
                #refresh_token = str(token)
                except Exception:
                    jwtData = {
                        'ujt_key':str(token),
                        'ujt_useruuid':user.u_uuid
                    }
                    jwtSerializer = UserjwttokenSerializer(data=jwtData)
                    if jwtSerializer.is_valid(): # 데이터 유효성 검사
                        jwtSerializer.save()
                    else:
                        return Response(
                            {"message": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
                        )

                access_token = str(token.access_token)
                response = Response(
                    {
                        "message": "login success",
                        "uid": UserSerializer(user).data["u_uid"],
                        "uuid": user.u_uuid.hex(),
                        "grade": UserSerializer(user).data["u_grade"],
                        "sex": UserSerializer(user).data["u_sex"],                    
                    },
                    status=status.HTTP_200_OK
                )
                response.set_cookie("access_token", access_token, httponly=True)
                #response.set_cookie("refresh_token", refresh_token, httponly=True)
                return response
            else: # 그 외
                return Response(
                    {"message": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
                )

class Register(APIView):
    permission_classes = (AllowAny,) # login만 권한 없이 접속 가능
    
    def post(self, request, format=None):
        import string, random, uuid
        uuid_ = bytes.fromhex(uuid.uuid4().hex)
        
        userData = {
            'u_uuid':uuid_,
            'u_grade':'N',
            'u_id':request.data['email'],
            'u_pw':bcrypt.hashpw(request.data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'u_phone':request.data['phone'],
            'u_sex':request.data['sex'],
            'u_mainpic':'""',
            'u_point':0,
            'u_emailnotify':'1'.encode(),
            'u_smsnotify':'1'.encode(),
            'u_pushnotify':'1'.encode(),
            'u_registerdate':str(timezone.now()).split('.')[0],
            'u_lastlogin':str(timezone.now()).split('.')[0],
            'u_introcode':''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15)), # 중복문제 해결해야 함
            'u_appversion':'0.0.1'
        }

        profileData = {
            'up_useruuid':uuid_,
            'up_name':request.data['name'],
            'up_sex':request.data['sex'],
            'up_birth':request.data['birth'],
            'up_height':request.data['height'],
            'up_body':request.data['body'],
            'up_edu':request.data['edu'],
            'up_eduname':request.data['eduName'],
            'up_live':request.data['region'],
            'up_religion':request.data['religion'],
            'up_smoke':request.data['smoke'],
            'up_alcohol':request.data['drinking'],
            'up_nickname':request.data['nickname'],
            #'up_selfintro':'',
            #'up_character':'',
            'up_requirepic':'["",""]',
            'up_extrapic':'["","",""]'
        }
        _UserSerializer = UserSerializer(data=userData)
        _UserprofileSerializer = UserprofileSerializer(data=profileData)
        if _UserSerializer.is_valid(): # 데이터 유효성 검사
            if _UserprofileSerializer.is_valid():
                _UserSerializer.save()
                _UserprofileSerializer.save()

                # 토큰 생성
                user = User.objects.filter(u_id=request.data['email']).first()
                token = MyTokenObtainPairSerializer.get_token(user)
                
                refresh_token = str(token)
                access_token = str(token.access_token)
                response = Response(
                    status=status.HTTP_200_OK
                )
                response.set_cookie("access_token", access_token, httponly=True)
                return response

            else:
                print(_UserprofileSerializer.errors)
                return Response(
                    {"message": "프로필작성에 오류가 있습니다."}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            print(_UserSerializer.errors)
            return Response(
                {"message": "회원정보에 오류가 있습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class Badge(APIView):
    permission_classes = (AllowAny,) # login만 권한 없이 접속 가능

    def get(self, request, format=None):
        _Userauthlist = Userauthlist.objects.filter(
                                        ual_useruuid = bytes.fromhex(request.headers['uuid'])
                                    )
        _UserauthlistSerializer = UserauthlistSerializer(_Userauthlist, many=True).data

        return Response(_UserauthlistSerializer)
        print(dir(_UserauthlistSerializer))

        for d in _UserauthlistSerializer:
            print(dir(d.values()))
            print(d.values())
            print()

    
    def post(self, request, format=None):
        
        data = dict(request.data)
        
        badgeData = {
            "mainPic": data["mainPic"],
            "requirePic": data["requirePic"],
            "extraPic": data["extraPic"],
            "professional": data["professional"],
            "businessman": data["businessman"],
            "highSalary": data["highSalary"],
            "a100million": data["a100million"],
            "gangnamAPT": data["gangnamAPT"],
            "expensiveAPT": data["expensiveAPT"],
            "foreignCar": data["foreignCar"],
            "superCar": data["superCar"],
            "highAsset": data["highAsset"],
            "ultraHighAsset": data["ultraHighAsset"],
            "eliteFamily": data["eliteFamily"],
            "highCaliberFamily": data["highCaliberFamily"],
            "prestigiousUniv": data["prestigiousUniv"],
            "aboardPrestigiousUniv": data["aboardPrestigiousUniv"],
            "height": data["height"]
        }

        isAllFine = True

        for key, val in badgeData.items():
            if val != [''] and val != '':
                name = ''
                for v in val:
                    if v == '':
                        continue
                    imgName = f'{key}_'+str(request.headers['uuid'])+'_'+str(time.time()).replace('.','')+'.png'
                    with open(settings.MEDIA_ROOT + key + '/' + imgName, 'wb') as f:
                        f.write(base64.decodebytes(v.encode('utf-8')))
                        name += f'"{imgName}",'

                name = '[' + name[:-1] + ']'
                
                data = {
                    'ual_useruuid':bytes.fromhex(request.headers['uuid']),
                    'ual_type':key[:15],
                    'ual_require':str(timezone.now()).split('.')[0],
                    'ual_comfirm':'',
                    'ual_return':'',
                    'ual_image': name
                }
                _UserauthlistSerializer = UserauthlistSerializer(data = data)

                if _UserauthlistSerializer.is_valid():
                    _UserauthlistSerializer.save()
                    pass
                else:
                    print(_UserauthlistSerializer.errors)

                    isAllFine = False
                    return Response(
                        {"message": "인증과정에서 오류가 발생했습니다."}, status=status.HTTP_400_BAD_REQUEST
                    )
        
        if isAllFine:
            response = Response(
                    status=status.HTTP_200_OK
                )
            return response

class Check(APIView):
    def post(self, request):
        nickname = request.data['nickname']

        nick_cnt = Userprofile.objects.filter(up_nickname = nickname).count()
        if nick_cnt == 0:
            response = Response(
                    {"result":True},
                    status=status.HTTP_200_OK
                )
            return response
        else:
            response = Response(
                    {"result":False},
                    status=status.HTTP_200_OK
                )
            return response
