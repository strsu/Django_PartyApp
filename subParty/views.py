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
    Boardaddon,
    Userparty,
    UserpartyAttend,
    User,
    Userprofile,
    Firebasetoken
)

from backend.serializers import (
    UserpartySerializer,
    UserpartyAttendSerializer,
    BoardaddonSerializer
)

from backend.firebase import (
    send_to_firebase_cloud_messaging,
    send_to_firebase_cloud_notification
)

import time
import base64
import random
import json
import datetime

class Board(APIView):
    def get(self, request):
        board_id_list = []
        board_attend_list = []
        board_like_list = []
        board_dib_list = []

        #print(request.GET)

        # 파라미터
        userUUID  = bytes.fromhex(request.headers['uuid'])
        category  = json.loads(request.GET['category']) # 글 카테고리
        fetchType = request.GET['type']      # 0: 처음 접속 / 1: 최신 글 / 2: 이전 글
        uid       = request.GET['page']      # 글 id
        mSex      = True if request.GET['mSex'] == 'true' else False     # 가져올 성별
        wSex      = True if request.GET['wSex'] == 'true' else False     # 
        startDay  = request.GET['startDay']  #
        endDay    = request.GET['endDay']    #
        
        # 게시판 리스트 가져오기
        boardQuery = None

        query = Q()
        if '종합' not in category:
            for tag in category:
                query.add(Q(up_tags__contains=tag), Q.OR)
        if mSex and not wSex:
            query.add(Q(up_sex='0'), Q.AND)
        elif not mSex and wSex:
            query.add(Q(up_sex='1'), Q.AND)
        if startDay != '':
            sy, sm, sd = map(int, startDay.split('-'))
            if endDay != '':
                ey, em, ed = map(int, endDay.split('-'))
                query.add(Q(up_wdate__range=(datetime.datetime(sy, sm, sd, 0, 0, 0), datetime.datetime(ey, em, ed, 23, 59, 59))), Q.AND)
            else:
                query.add(Q(up_wdate__range=(datetime.datetime(sy, sm, sd, 0, 0, 0), datetime.datetime(sy, sm, sd, 23, 59, 59))), Q.AND)

        if fetchType == '0': # 처음 데이터 
            boardQuery = Userparty.objects.prefetch_related().filter(query).order_by('up_uid').reverse()[:9]
        elif fetchType == '1': # 최신 데이터 요청시
            boardQuery = Userparty.objects.prefetch_related().filter(Q(up_uid__gt=uid) & query).order_by('up_uid').reverse()
        elif fetchType == '2': # 이전 데이터 요청시
            boardQuery = Userparty.objects.prefetch_related().filter(Q(up_uid__lt=uid) & query).order_by('up_uid').reverse()[:9]
        elif fetchType == '3': # 비슷한 태그
                boardQuery = Userparty.objects.prefetch_related().filter(query).order_by('up_uid').exclude(up_uid=uid).exclude(up_useruuid=userUUID).reverse()[:9]
        
        #print(boardQuery._query)
        
        if len(boardQuery) == 0:
            return Response( status=status.HTTP_204_NO_CONTENT )
        
        board_id_list = [val.up_uid for val in boardQuery]

        # 내가 참가신청 누른 글
        attendQuery = UserpartyAttend.objects.prefetch_related().filter(
                                            upa_boardid__in = board_id_list, 
                                            upa_useruuid = userUUID)
        board_attend_list = [val.upa_boardid for val in attendQuery]

        # 내가 좋아요 누른 글 가져오기
        addonQuery = Boardaddon.objects.prefetch_related().filter(
                                                                    ba_boardid__in = board_id_list, 
                                                                    ba_uuid = userUUID, 
                                                                    ba_tablename='userparty')
        board_like_list = [val.ba_boardid for val in addonQuery if val.ba_type == 'like']
        board_dib_list = [val.ba_boardid for val in addonQuery if val.ba_type == 'dibs']

        response_list = {}
        
        for val in boardQuery:
            _json = {}

            _json["uid"] = val.up_uid
            _json["nickname"] = val.up_nickname
            _json["sex"] = val.up_sex
            _json["title"] = val.up_title
            _json["content"] = val.up_content
            _json["date"] = val.up_wdate
            _json["like"] = val.up_like
            _json["state"] = val.up_state
            _json["isMine"] = val.up_useruuid == userUUID and True or False
            _json["isApply"] = val.up_uid in board_attend_list and True or False
            _json["isLike"] = val.up_uid in board_like_list and True or False
            _json["isDibs"] = val.up_uid in board_dib_list and True or False
            _json["images"] = ''

            if val.up_image != '':
                _json["images"] = settings.MEDIA_URL + '?imageName=userParty ' + val.up_image
            
            if ',' in val.up_tags:
                tags = val.up_tags.replace("'","").replace("[","").replace("]","").replace(", ",",")
                _json["tags"] = tags.split(',')
            else:
                _json["tags"] = [val.up_tags.replace("'","").replace("[","").replace("]","")]

            response_list[val.up_uid] = _json
        
        return Response(response_list)

    def post(self, request):

        nickName = settings.NICKNAME_ADJECTIVE[random.randint(0, len(settings.NICKNAME_ADJECTIVE)-1)] + ' ' + \
                   settings.NICKNAME_NOUN[random.randint(0, len(settings.NICKNAME_NOUN)-1)]
        
        imgName = ''
        if request.data['img'] != '':
            imgName = 'userParty'+str(request.headers['uuid'])+'_'+str(time.time()).replace('.','')+'.png'
            with open(settings.MEDIA_ROOT + 'userParty/' + imgName, 'wb') as f:
                f.write(base64.decodebytes(request.data['img'].encode('utf-8')))

        data = {
            'up_useruuid' : bytes.fromhex(request.headers['uuid']),
            'up_nickname' : nickName,
            'up_sex' : request.data['sex'],
            'up_tags' : f"'{request.data['category']}'",
            'up_title' : request.data['title'],
            'up_content' : request.data['content'],
            'up_wdate' : str(timezone.now()).split('.')[0],
            'up_image' : imgName,
            'up_like' : 0,
            'up_read' : 0,
            'up_state' : request.data['state'],
            'up_mdate' : request.data['date'],
        }

        serializer = UserpartySerializer(data=data)
        if serializer.is_valid(): # 데이터 유효성 검사
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )


class Category(APIView):
    def get(self, request):
        category = Filter.objects.filter(f_sort='subParty').order_by('f_seq').values()
        return Response([val['f_name'] for val in category])


class Addon(APIView):
    def post(self, request):
        _request = request.data['data']
        data = {
            'ba_uuid':bytes.fromhex(request.headers['uuid']),
            'ba_tablename':'userparty',
            'ba_type':_request['type'],
            'ba_boardid':_request['uid'],
        }
        serializer = BoardaddonSerializer(data=data)
        if serializer.is_valid(): # 데이터 유효성 검사
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request):
        try:
            addon = Boardaddon.objects.get(
                ba_uuid=bytes.fromhex(request.headers['uuid']),
                ba_tablename='userparty',
                ba_type=request.data['type'],
                ba_boardid=request.data['uid'])
            addon.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"message": Exception}, status=status.HTTP_400_BAD_REQUEST
            )

class Apply(APIView):
    def get(self, request):
        # 참가자 가져와서
        attendQuery = UserpartyAttend.objects.prefetch_related().filter(
            upa_boardid=request.GET['uid'],
            upa_ownuuid=bytes.fromhex(request.headers['uuid']) )
        user_list = [val.upa_useruuid for val in attendQuery]
            
        # 사용자 닉네임, 이미지 가져오기
        userQuery = User.objects.prefetch_related().filter(u_uuid__in = user_list)
        userprofileQuery = Userprofile.objects.prefetch_related().filter(up_useruuid__in = user_list)
            
        json = {}
        for aval, uval, pval in zip(attendQuery, userQuery, userprofileQuery):
            if aval.upa_useruuid.hex() in json: # 메인사진
                json[aval.upa_useruuid.hex()] = {'attend': aval.upa_attend, **json[aval.upa_useruuid.hex()]}
            else:
                json[aval.upa_useruuid.hex()] = {'attend': aval.upa_attend}

            if uval.u_uuid.hex() in json: # 메인사진
                json[uval.u_uuid.hex()] = {'image': uval.u_mainpic, 'phone': uval.u_phone, 'chatid': 'user'+str(uval.u_uid), **json[uval.u_uuid.hex()]}
            else:
                json[uval.u_uuid.hex()] = {'image': uval.u_mainpic, 'phone': uval.u_phone, 'chatid': 'user'+str(uval.u_uid)}

            if pval.up_useruuid.hex() in json: # 닉네임
                json[pval.up_useruuid.hex()] = {'nickname': pval.up_nickname, **json[pval.up_useruuid.hex()]}
            else:
                json[pval.up_useruuid.hex()] = {'nickname': pval.up_nickname}

        response_json = []
        for val, key in json.items():
            print(key)
            response_json.append({
                'user': val,
                'image': settings.MEDIA_URL + '?imageName=mainPic ' + key['image'].replace('"',''),
                'nickname': key['nickname'],
                'attend': key['attend'],
                'phone': key['attend'] == 2 and key['phone'] or None,
                #'chatid': key['attend'] == 1 and key['chatid'] or None
            })
            
        return Response(response_json)
            

    def post(self, request):

        ownuuid = Userparty.objects.get(up_uid=request.data['uid']).up_useruuid

        data = {
            'upa_boardid':request.data['uid'],
            'upa_ownuuid':ownuuid,
            'upa_useruuid':bytes.fromhex(request.headers['uuid']),
            'upa_attend':0,
        }

        try:
            ownToken = Firebasetoken.objects.get(fbt_useruuid = ownuuid).fbt_usertoken
            send_to_firebase_cloud_messaging(ownToken, '파티', '게시판 파티에 신청이 왔습니다.')
        except Exception:
            #게시글 생성자의 토큰이 없는경우
            print(Exception)
        finally:
            serializer = UserpartyAttendSerializer(data=data)
            if serializer.is_valid(): # 데이터 유효성 검사
                #send_to_firebase_cloud_notification(ownToken, '게시판 파티에 신청이 왔습니다.')
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
    def put(self, request):
        try:
            attendQuery = UserpartyAttend.objects.get(
                        upa_boardid=request.data['uid'],
                        upa_useruuid=bytes.fromhex(request.data['useruuid']) )
            
            if attendQuery.upa_attend == 0: # 수락만 한 경우
                attendQuery.upa_attend = 1
                attendQuery.save()
                userQuery = User.objects.get(u_uuid=bytes.fromhex(request.data['useruuid']))
                return Response({
                    'chatid':'user'+str(userQuery.u_uid),
                    'nickname': Userprofile.objects.get(up_uid=bytes.fromhex(request.data['useruuid'])).up_nickname
                    }, status=status.HTTP_200_OK)
            elif attendQuery.upa_attend == 1: # 번호 오픈 요청시

                userQuery = User.objects.get(
                            u_uuid=bytes.fromhex(request.data['useruuid']) )
                
                if userQuery.u_point > 20:
                    userQuery.u_point -= 20
                    attendQuery.upa_attend = 2

                    userQuery.save
                    attendQuery.save()
                    return Response({'phone': userQuery.u_phone}, status=status.HTTP_200_OK)
                else:
                    return Response({'phone': userQuery.u_phone}, status=status.HTTP_304_NOT_MODIFIED)
        except Exception:
            return Response(
                {"message": Exception}, status=status.HTTP_400_BAD_REQUEST
            )



class MyParty(APIView):
    def get(self, request):
        boardQuery = Userparty.objects.filter(up_useruuid=bytes.fromhex(request.headers['uuid']))

        response_list = []
        for val in boardQuery:
            json = {}

            json["uid"] = val.up_uid
            json["nickname"] = val.up_nickname
            json["sex"] = val.up_sex
            json["title"] = val.up_title
            json["content"] = val.up_content
            json["date"] = val.up_wdate
            json["like"] = val.up_like
            json["isMine"] = True
            json["isApply"] = False
            json["isLike"] = False
            json["isDibs"] = False
            json["state"] = val.up_state

            if ',' in val.up_tags:
                tags = val.up_tags.replace("'","").replace("[","").replace("]","").replace(", ",",")
                json["tags"] = tags.split(',')
            else:
                json["tags"] = [val.up_tags.replace("'","")]

            if val.up_image != '':
                json["images"]   = settings.MEDIA_URL + '?imageName=userParty ' + val.up_image
            response_list.append(json)
            
        return Response(response_list)

class MyAttend(APIView):
    def get(self, request):
        userUUID = bytes.fromhex(request.headers['uuid'])
        
        # 내가 참가신청 누른 글
        attendQuery = UserpartyAttend.objects.prefetch_related().filter(upa_useruuid = userUUID)
        board_attend_list = [val.upa_boardid for val in attendQuery]

        boardQuery = Userparty.objects.filter(up_uid__in=board_attend_list)

        # 내가 좋아요 누른 글 가져오기
        addonQuery = Boardaddon.objects.prefetch_related().filter(
                                            ba_boardid__in = board_attend_list, 
                                            ba_uuid = userUUID, 
                                            ba_tablename='userparty')

        board_like_list = [val.ba_boardid for val in addonQuery if val.ba_type == 'like']
        board_dib_list = [val.ba_boardid for val in addonQuery if val.ba_type == 'dibs']
                
        response_list = []

        for val in boardQuery:
            json = {}

            json["uid"] = val.up_uid
            json["nickname"] = val.up_nickname
            json["sex"] = val.up_sex
            json["title"] = val.up_title
            json["content"] = val.up_content
            json["date"] = val.up_wdate
            json["like"] = val.up_like
            json["state"] = val.up_state
            json["isMine"] = False
            json["isApply"] = True
            json["isLike"] = val.up_uid in board_like_list and True or False
            json["isDibs"] = val.up_uid in board_dib_list and True or False

            if ',' in val.up_tags:
                tags = val.up_tags.replace("'","").replace("[","").replace("]","").replace(", ",",")
                json["tags"] = tags.split(',')
            else:
                json["tags"] = [val.up_tags.replace("'","")]

            if val.up_image != '':
                json["images"]   = settings.MEDIA_URL + '?imageName=userParty ' + val.up_image
            response_list.append(json)
        
        
        return Response(response_list)

class MyDibs(APIView):
    def get(self, request):
        userUUID = bytes.fromhex(request.headers['uuid'])

        # 내가 찜 누른 글 가져오기
        addonQuery = Boardaddon.objects.prefetch_related().filter(
                                            ba_uuid = userUUID, 
                                            ba_tablename='userparty')

        board_like_list = [val.ba_boardid for val in addonQuery if val.ba_type == 'like']
        board_dib_list = [val.ba_boardid for val in addonQuery if val.ba_type == 'dibs']

        # 글 불러오기
        boardQuery = Userparty.objects.filter(up_uid__in=board_dib_list)        

        # 내가 참가신청 누른 글
        attendQuery = UserpartyAttend.objects.prefetch_related().filter(
                                            upa_boardid__in = board_dib_list, 
                                            upa_useruuid = userUUID)
        board_attend_list = [val.upa_boardid for val in attendQuery]
                
        response_list = []
        for val in boardQuery:
            json = {}

            json["uid"] = val.up_uid
            json["nickname"] = val.up_nickname
            json["sex"] = val.up_sex
            json["title"] = val.up_title
            json["content"] = val.up_content
            json["date"] = val.up_wdate
            json["like"] = val.up_like
            json["state"] = val.up_state
            json["isMine"] = False
            json["isApply"] = val.up_uid in board_attend_list and True or False
            json["isLike"] = val.up_uid in board_like_list and True or False
            json["isDibs"] = True

            if ',' in val.up_tags:
                tags = val.up_tags.replace("'","").replace("[","").replace("]","").replace(", ",",")
                json["tags"] = tags.split(',')
            else:
                json["tags"] = [val.up_tags.replace("'","")]

            if val.up_image != '':
                json["images"]   = settings.MEDIA_URL + '?imageName=userParty ' + val.up_image
            response_list.append(json)
        
        
        return Response(response_list)

class UserDetail(APIView):
    def get(self, request):
        userUUID = bytes.fromhex(request.GET['useruuid'])
        userprofileQuery = Userprofile.objects.prefetch_related().get(up_useruuid = userUUID)

        filterQuery = Filter.objects.prefetch_related().filter(f_sort='profile')
        
        #for val in filterQuery:
        #    print(val.f_type, val.f_name, val.f_seq)

        print(filterQuery.get(f_type='음주', f_seq=0).f_name)

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

class UserSimpleDetail(APIView):
    def get(self, request):
        uid = request.GET['uid']
        userUUID = Userparty.objects.get(up_uid=uid).up_useruuid
        userMainPic = User.objects.get(u_uuid = userUUID).u_mainpic
        userprofileQuery = Userprofile.objects.prefetch_related().get(up_useruuid = userUUID)

        json = {
            'mainpic' : settings.MEDIA_URL + '?imageName=mainPic ' + userMainPic.replace('"',''),
            'requirepic' : userprofileQuery.up_requirepic[1:-1].replace('"','').split(','),
            'extrapic' : userprofileQuery.up_extrapic[1:-1].replace('"','').split(','),
        }

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