#from plistlib import UID
#from telnetlib import STATUS
from tracemalloc import start
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
    Mainparty,
    MainpartyAttend,
    MainpartyReviewQna,
    MainpartyTimeline,
    Boardaddon,
    Filter
)

from backend.serializers import (
    MainpartyReviewQnaSerializer,
    MainpartySerializer,
    FilterSerializer
)

import time
import base64, json
import random

class Board(APIView):
    def get(self, request):
        board_id_list = []
        board_like_list = []
        print(request.GET)

        # 파라미터
        userUUID  = bytes.fromhex(request.headers['uuid'])
        #category  = request.GET['category']  # 글 카테고리
        fetchType = request.GET['type']      # 0: 처음 접속 / 1: 최신 글 / 2: 이전 글
        uid       = request.GET['page']      # 글 id

        startDay = request.GET['startDay']
        endDay = request.GET['endDay']
        location = json.loads(request.GET['location'])
        age = json.loads(request.GET['age'])

        # 게시판 리스트 가져오기
        filterQuery = Q()

        boardQuery = Mainparty.objects.prefetch_related()

        if startDay != '' and endDay == '':
            filterQuery.add(Q(mp_mdate=startDay), Q.AND)
        else:
            if startDay != '' and endDay != '':
                filterQuery.add(Q(mp_mdate__range=(startDay, endDay)), Q.AND)
        
        if len(location) > 0:
            filterQuery.add(Q(mp_place__in=location), Q.AND)
        
        if age[0] != 0 or age[1] != 100:
            filterQuery.add(Q(mp_minage__gt=age[0], mp_maxage__lt=age[1]), Q.AND)

        if fetchType == '0': # 처음 데이터
            boardQuery = Mainparty.objects.prefetch_related().filter(filterQuery).order_by('mp_uid').reverse()[:10]
        elif fetchType == '1': # 최신 데이터 요청시
            filterQuery.add(Q(mp_uid__gt=uid), Q.AND)
            boardQuery = Mainparty.objects.prefetch_related().filter(filterQuery).order_by('mp_uid').reverse()
        elif fetchType == '2': # 이전 데이터 요청시
            filterQuery.add(Q(mp_uid__lt=uid), Q.AND)
            boardQuery = Mainparty.objects.prefetch_related().filter(filterQuery).order_by('mp_uid').reverse()[:10]
        
        print(boardQuery._query)

        if len(boardQuery) == 0:
            return Response( status=status.HTTP_204_NO_CONTENT )
        
        board_id_list = [val.mp_uid for val in boardQuery]

        # 내가 좋아요 누른 글 가져오기
        addonQuery = Boardaddon.objects.prefetch_related().filter(
                                            ba_boardid__in = board_id_list, 
                                            ba_uuid = userUUID, 
                                            ba_tablename='mainparty', 
                                            ba_type='like')
        board_like_list = [val.ba_boardid for val in addonQuery]

        timelineQuery = MainpartyTimeline.objects.filter(mpt_boardid__in=board_id_list)
        timeline_dict = {}
        for val in timelineQuery:
            _json = {}
            _json['signm'] = val.mpt_signm
            _json['signw'] = val.mpt_signw
            _json['attendm'] = val.mpt_attendm
            _json['attendw'] = val.mpt_attendw
            _json['pricem'] = val.mpt_pricem
            _json['pricew'] = val.mpt_pricew
            _json['minagem'] = val.mpt_minagem
            _json['maxagem'] = val.mpt_maxagem
            _json['minagew'] = val.mpt_minagew
            _json['maxagew'] = val.mpt_maxagew
            _json['deadline'] = val.mpt_deadline

            if val.mpt_boardid in timeline_dict:
                timeline_dict[val.mpt_boardid] = {val.mpt_time: _json, **timeline_dict[val.mpt_boardid]}
            else:
                timeline_dict[val.mpt_boardid] = {val.mpt_time: _json}

        board_list = []
        for val in boardQuery:
            _json = {}

            _json["uid"]     = val.mp_uid
            _json["writer"]  = '관리자' #val.mp_writer
            _json["title"]   = val.mp_title
            _json["type"]    = val.mp_type
            _json["place"]   = val.mp_place
            _json["content"] = val.mp_content
            _json["minage"]  = val.mp_minage
            _json["maxage"]  = val.mp_maxage
            _json["images"]  = val.mp_image
            _json["like"]    = val.mp_like in board_like_list and True or False
            _json["mdate"]   = val.mp_mdate
            _json["support"] = val.mp_support
            _json["timeline"] = val.mp_uid in timeline_dict and timeline_dict[val.mp_uid] or {}

            if val.mp_image != '':
                _json["images"]   = settings.MEDIA_URL + '?imageName=mainParty ' + val.mp_image

            board_list.append(_json)
        
        return Response(board_list)


class Category(APIView):
    def get(self, request):
        category = Filter.objects.filter(f_sort='mainParty').order_by('f_seq').values()

        '''serializer = FilterSerializer(category, many=True)
        json = []
        for val in serializer.data:
            json.append({'name':val.f_name})'''
        return Response([val['f_name'] for val in category])

class Review(APIView):
    def get(self, request):
        reviewQuery = MainpartyReviewQna.objects.filter(
            mprq_boardid=request.GET['uid'],
            mprq_type='0',
        )

        attendQuery = MainpartyAttend.objects.filter(
            mpa_boardid=request.GET['uid'],
        )

        attend_dict = {}
        for val in attendQuery:
            attend_dict[val.mpa_useruuid.hex()] = {
                'timeline': val.mpa_timeline
            }

        reviewResponse = []
        for val in reviewQuery:
            _json = {}
            _json['nickname'] = val.mprq_nickname
            _json['content'] = val.mprq_content
            _json['date'] = val.mprq_date
            _json['admincontent'] = val.mprq_admincontent
            _json['admindate'] = val.mprq_admindate
            _json['score'] = val.mprq_score
            _json['helpcnt'] = val.mprq_helpcnt
            _json['timeline'] = ''
            if val.mprq_uuid.hex() in attend_dict:
                _json['timeline'] = attend_dict[val.mprq_uuid.hex()]['timeline']
            reviewResponse.append(_json)
        
        return Response(reviewResponse)

    def post(self, request):
        data = {
            'mprq_boardid':request.headers['uid'],
            'mprq_type':'review',
            'mprq_uuid':bytes.fromhex(request.headers['uuid']),
            'mprq_content':request['content'],
            'mprq_date': str(timezone.now()).split('.')[0],
            'mprq_score': request['score'],
            'mprq_helpcnt': 0
        }
    
class QNA(APIView):
    def get(self, request):
        qnaQuery = MainpartyReviewQna.objects.filter(
            mprq_boardid=request.GET['uid'],
            mprq_type__in=['1', '2']
        )

        response = []
        for val in qnaQuery:
            response.append({
                'content': val.mprq_content if val.mprq_type == '1' or val.mprq_uuid.hex() == request.headers['uuid'] else '작성자만 확인할 수 있습니다.',
                'date': val.mprq_date,
                'answer': val.mprq_admincontent,
                'answer_date':val.mprq_admindate,
                #'isMine': 1 if val.mprq_uuid.hex() == request.headers['uuid'] else 0
            })
        
        return Response(response)


    def post(self, request):
        data = {
            'mprq_boardid': request.data['uid'],
            'mprq_type': '2' if request.data['secret'] else '1',
            'mprq_uuid': bytes.fromhex(request.headers['uuid']),
            'mprq_nickname': '.',
            'mprq_content': request.data['content'],
            'mprq_date': str(timezone.now()).split('.')[0],
            'mprq_score': 0,
            'mprq_helpcnt': 0
        }
        serializer = MainpartyReviewQnaSerializer(data=data)
        if serializer.is_valid(): # 데이터 유효성 검사
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )



class Attend(APIView):
    def get(self, request):
        uid = request.GET['uid']

        attendQuery = MainpartyAttend.objects.filter(mpa_boardid=uid)
        attend_list = []
        for val in attendQuery:
            _json = {}
            _json['']