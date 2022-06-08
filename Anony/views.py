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

from django.db.models import Max

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from Anony.models import (
    Anonyboard,
    AnonyboardComment,
    Boardaddon,
    Filter,
    Firebasetoken
)

from Anony.serializers import (
    AnonyboardSerializer,
    AnonyboardCommentSerializer,
    BoardaddonSerializer,
    FilterSerializer,
    FirebasetokenSerializer
)

import time
import base64
import random

class Board(APIView):
    def get(self, request):
        board_id_list = []
        board_like_list = []

        # 파라미터
        userUUID  = bytes.fromhex(request.headers['uuid'])
        category  = request.GET['category']  # 글 카테고리
        fetchType = request.GET['type']      # 0: 처음 접속 / 1: 최신 글 / 2: 이전 글
        uid       = request.GET['page']      # 글 id

        # 게시판 리스트 가져오기

        boardQuery = None

        if fetchType == '0':
            if category == '종합':
                boardQuery = Anonyboard.objects.prefetch_related().all().order_by('ab_uid').reverse()[:10]
            else:
                boardQuery = Anonyboard.objects.prefetch_related().filter(ab_type=category).order_by('ab_uid').reverse()[:10]
        elif fetchType == '1':
            if category == '종합':
                boardQuery = Anonyboard.objects.prefetch_related().filter(ab_uid__gt=uid).order_by('ab_uid').reverse()
            else:
                boardQuery = Anonyboard.objects.prefetch_related().filter(ab_uid__gt=uid, ab_type=category).order_by('ab_uid').reverse()
        elif fetchType == '2':
            if category == '종합':
                boardQuery = Anonyboard.objects.prefetch_related().filter(ab_uid__lt=uid).order_by('ab_uid').reverse()[:10]
            else:
                boardQuery = Anonyboard.objects.prefetch_related().filter(ab_uid__lt=uid, ab_type=category).order_by('ab_uid').reverse()[:10]

        if len(boardQuery) == 0:
            return Response( status=status.HTTP_204_NO_CONTENT )
        
        board_id_list = [val.ab_uid for val in boardQuery]

        # 내가 좋아요 누른 글 가져오기
        addonQuery = Boardaddon.objects.prefetch_related().filter(
                                                                    ba_boardid__in = board_id_list, 
                                                                    ba_uuid = userUUID, 
                                                                    ba_tablename='anonyboard', 
                                                                    ba_type='like')
        board_like_list = [val.ba_boardid for val in addonQuery]

        response_list = []
        for val in boardQuery:
            json = {}
            json["uid"]      = val.ab_uid
            json["wdate"]    = val.ab_wdate
            json["writer"]   = val.ab_writer_a
            json["type"]     = val.ab_type
            json["title"]    = val.ab_title
            json["content"]  = val.ab_content
            json["like"]     = val.ab_like
            json["read"]     = val.ab_read
            json["sex"]      = val.ab_sex
            json["replyCnt"] = val.ab_comment
            json["isMine"]   = val.ab_writer_uuid == userUUID and True or False
            json["isLike"]   = val.ab_uid in board_like_list and True or False
            json["images"]   = ''
            if val.ab_image != '':
                json["images"]   = settings.MEDIA_URL + '?imageName=anony ' + val.ab_image
            response_list.append(json)


        '''print()
        print(boardQuery._query)
        print()
        print(addonQuery._query)
        print()'''  
        
        '''serializer = AnonyboardSerializer(boardQuery, many=True)
        for val in serializer.data:
            print(val)'''
        
        return Response(response_list)

    def post(self, request):

        nickName = settings.NICKNAME_ADJECTIVE[random.randint(0, len(settings.NICKNAME_ADJECTIVE)-1)] + ' ' + \
                   settings.NICKNAME_NOUN[random.randint(0, len(settings.NICKNAME_NOUN)-1)]
        
        imgName = ''
        if request.data['img'] != '':
            imgName = 'anony_'+str(request.headers['uuid'])+'_'+str(time.time()).replace('.','')+'.png'
            with open(settings.MEDIA_ROOT + 'anony/' + imgName, 'wb') as f:
                f.write(base64.decodebytes(request.data['img'].encode('utf-8')))

        data = {
            'ab_writer_uuid' : bytes.fromhex(request.headers['uuid']),
            'ab_writer_a' : nickName,
            'ab_sex' : request.data['sex'],
            'ab_type' : request.data['category'],
            'ab_title' : request.data['title'],
            'ab_content' : request.data['content'],
            'ab_wdate' : str(timezone.now()).split('.')[0],
            'ab_image' : imgName,
            'ab_like' : 0,
            'ab_read' : 0,
            'ab_comment' : 0
        }

        serializer = AnonyboardSerializer(data=data)
        if serializer.is_valid(): # 데이터 유효성 검사
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request):
        try:
            # 해당 게시글 가져와서
            boardQuery = Anonyboard.objects.get( ab_uid=request.data['uid'] )
            
            if request.data['type'] == 'read':
                boardQuery.ab_read += 1
                return Response(status=status.HTTP_200_OK)
            elif request.data['type'] == 'like':
                if request.data['isLike']: # 기존에 좋아요를 눌렀던 글이면
                    boardQuery.ab_like -= 1
                    addonQuery = Boardaddon.objects.get(ba_boardid=request.data['uid'], ba_uuid=bytes.fromhex(request.headers['uuid']))
                    addonQuery.delete()
                else:
                    data = {
                        'ba_uuid' : bytes.fromhex(request.headers['uuid']),
                        'ba_tablename':'anonyboard',
                        'ba_type':'like',
                        'ba_boardid':request.data['uid']
                    }

                    boardQuery.ab_like += 1

                    serializer = BoardaddonSerializer(data=data) # 내가 좋아요 한 글 저장
                    if serializer.is_valid(): # 데이터 유효성 검사
                        serializer.save()
                        boardQuery.save()
                        return Response(status=status.HTTP_200_OK)
                    else:
                        print(serializer.errors)
                        return Response(
                            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                        )
            elif request.data['type'] == 'update': # 글 수정
                boardQuery.ab_type = request.data['category']
                boardQuery.ab_title = request.data['title']
                boardQuery.ab_content = request.data['content']

                # 이미지가 변경된 경우
                if len(request.data['img']) > 200 :
                    imgName = boardQuery.ab_image
                    if imgName == '':
                        imgName = 'anony_'+str(request.headers['uuid'])+'_'+str(time.time()).replace('.','')+'.png'
                        boardQuery.ab_image = imgName

                    with open(settings.MEDIA_ROOT + 'anony/' + imgName, 'wb') as f:
                        f.write(base64.decodebytes(request.data['img'].encode('utf-8')))
                elif request.data['img'] == '' :
                    boardQuery.ab_image = ''
                
                boardQuery.save()
                return Response(status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"message": Exception}, status=status.HTTP_400_BAD_REQUEST
            )


class BoardComment(APIView):
    def get(self, request):
        commentQuery = AnonyboardComment.objects.prefetch_related().filter(ac_refid=request.GET['uid']).order_by('ac_seqm', 'ac_wdate')
        addonQuery = Boardaddon.objects.prefetch_related().filter(
                                                ba_boardid = request.GET['uid'], # 해당 게시물에서
                                                ba_uuid = bytes.fromhex(request.headers['uuid']),  # 내 정보 중
                                                ba_tablename='anonycomment',     # 댓글 정보에 관해서
                                                ba_type='like')                  # 좋아요를 눌렀는지 아닌지를
        
        my_like_list = [val.ba_commentid for val in addonQuery]
        
        response_list = []
        response_bigcomment_list = []
        for val in commentQuery:
            json = {}
            json["index"]      = val.ac_uid
            json["refid"]      = val.ac_refid
            json["replyer"]    = val.ac_replyer_a
            json["sex"]        = val.ac_sex
            json["wdate"]      = val.ac_wdate
            json["content"]    = val.ac_content
            json["like"]       = val.ac_like
            json["seqM"]       = val.ac_seqm
            json["isSub"]      = val.ac_issub
            json["isMine"]     = val.ac_replyer_uuid == bytes.fromhex(request.headers['uuid']) and True or False
            json["isLike"]     = val.ac_uid in my_like_list and True or False
            json["bigComment"] = []

            if val.ac_issub == -1: # 대댓글이 아니면
                response_list.append(json)
                response_bigcomment_list.append([])
            else:
                response_bigcomment_list[val.ac_seqm].append(json)
        
        for i in range(len(response_bigcomment_list)):
                response_list[i]['bigComment'] = response_bigcomment_list[i]

        #return Response( status=status.HTTP_400_BAD_REQUEST )
        return Response(response_list)
    
    def post(self, request):

        # 게시글 댓글 카운트 1 up
        boardQuery = Anonyboard.objects.get( ab_uid=request.data['uid'] )
        boardQuery.ab_comment += 1

        # 기존에 댓글을 달았는지
        commentQuery = AnonyboardComment.objects.prefetch_related().filter(ac_refid=request.data['uid'])
            
        # 댓글 순서
        forMaxSeq = commentQuery.all().aggregate(Max('ac_seqm'))['ac_seqm__max']
        
        if forMaxSeq is None:
            forMaxSeq = 0
        else:
            if request.data['isSub'] != -1:
                forMaxSeq = request.data['isSub']
            else:
                forMaxSeq += 1                

        nickName = request.data['nickname']

        # 게시글 작성자가 아니면
        if nickName == '':
            has_nickName = commentQuery.filter( ac_replyer_uuid=bytes.fromhex(request.headers['uuid'])).first()
            
            # 기존에 댓글을 달지 않았다면
            if has_nickName is None:
                # 닉네임 생성
                nickName = settings.NICKNAME_ADJECTIVE[random.randint(0, len(settings.NICKNAME_ADJECTIVE)-1)] + ' ' + \
                    settings.NICKNAME_NOUN[random.randint(0, len(settings.NICKNAME_NOUN)-1)]
            else:
                nickName = has_nickName.ac_replyer_a
        
        print(request.headers['uuid'])
        
        # 댓글 입력
        data = {
            'ac_refid' : request.data['uid'],
            'ac_replyer_uuid' : bytes.fromhex(request.headers['uuid']),
            'ac_replyer_a' : nickName,
            'ac_sex' : request.data['sex'],
            'ac_wdate' : str(timezone.now()),
            'ac_content' : request.data['content'],
            'ac_like' : 0,
            'ac_seqm' : forMaxSeq,
            'ac_issub' : request.data['isSub']
        }

        serializer = AnonyboardCommentSerializer(data=data)
        if serializer.is_valid(): # 데이터 유효성 검사
            serializer.save()
            boardQuery.save()
            return Response(status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(
                {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request):
        try:
            print(request.data)
            if request.data['type'] == 'read':
                pass
            elif request.data['type'] == 'like':
                commentQuery = AnonyboardComment.objects.get(ac_refid=request.data['refid'], ac_uid=request.data['uid'])

                if request.data['isLike']: # 기존에 좋아요를 눌렀던 글이면
                    
                    addonQuery = Boardaddon.objects.get(
                                        ba_boardid=request.data['refid'],
                                        ba_commentid=request.data['uid'],
                                        ba_tablename='anonycomment',
                                        ba_uuid=bytes.fromhex(request.headers['uuid']))
                    addonQuery.delete()
                    commentQuery.ac_like -= 1
                    commentQuery.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    data = {
                        'ba_uuid' : bytes.fromhex(request.headers['uuid']),
                        'ba_tablename':'anonycomment',
                        'ba_type':'like',
                        'ba_boardid':request.data['refid'],
                        'ba_commentid':request.data['uid']
                    }
                    commentQuery.ac_like += 1
                    serializer = BoardaddonSerializer(data=data) # 내가 좋아요 한 글 저장
                    if serializer.is_valid(): # 데이터 유효성 검사
                        serializer.save()
                        commentQuery.save()
                        return Response(status=status.HTTP_200_OK)
                    else:
                        print(serializer.errors)
                        return Response(
                            {"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                        )
        except Exception:
            return Response(
                {"message": Exception}, status=status.HTTP_400_BAD_REQUEST
            )


class Category(APIView):
    def get(self, request):
        category = Filter.objects.filter(f_sort='anony').order_by('f_seq')
        
        '''
        # 이것도 가능, 뭐가 나은지?
        for val in category:
            print(val.f_name)'''
        
        serializer = FilterSerializer(category, many=True)
        json = []
        for val in serializer.data:
            #print(dict(val)['f_name'])
            json.append({'name':val['f_name']})

            #같음
            #print(list(val.values())[1])
            #json.append({'name':list(val.values())[1]})
        return Response(json)

