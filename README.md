# #backend
 장고프레임워크_리액트 네이티브 앱 백엔드

## #데이터 베이스
![ullim_20220707_195114](https://user-images.githubusercontent.com/25381921/177757269-697721fd-1899-4f12-bd38-d08af4a543fa.png)

## #라이브러리
 
 1. djangorestframework-simplejwt, JWT 토큰 방식으로 보안처리 하기 위해서
 2. bcrypt, 패스워드 암호화에 이용
 3. firebase_admin, google fcm을 이용해서 PUSH 알림 및 백그라운드 MSG 송신 처리    
  -> AWS Lightsail에서는 Ram때문에 설치 안 됨. EC2는 열어야...

## #Swagger식 표현

 > **Auth**
 ```python
    re_path(r'^login/$', views.Login.as_view(), name='user_list'), # 사용자 로그인 검증
    re_path(r'^register/$', views.Register.as_view(), name='register'),  # 회원가입
    re_path(r'^badge/$', views.Badge.as_view(), name='register'),  # 각종 인증 (학력, 재산 등)
    re_path(r'^check/$', views.Check.as_view(), name='register'),  # 닉네임 중복 체크, Ajax 처럼 입력시 자동 체크 하려고,,,

    re_path(r'^token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 토큰 생성
    re_path(r'^token/verify/$', TokenVerifyView.as_view(), name='token_verify'),  # 토큰 인증
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 재생성
 ```
 
 #### * 중요 로직
 ![image](https://user-images.githubusercontent.com/25381921/177764175-0ca12f06-bd2e-4c66-9b09-7dd3f67d3082.png)
 JWT를 통한 로그인은 동일 디바이스에서만 가능하기 때문에 FCM의 재발행이 필요없다.    
 JWT는 Cookie를 통해 전달된다. 이는 SSL, HTTPS를 사용하기 위함이다.
 Ejabberd계정은 URL을 통해 생성 할 수 있다. (ejabberd.yml 수정 필요)     
 ![image](https://user-images.githubusercontent.com/25381921/177765597-f3d6c713-c6f4-42ba-a3ed-9c8e6e54d580.png)

 > **Anony** - 익명 게시판
 ```python
    re_path(r'^board/$', views.Board.as_view(), name='user_list'),  # 게시물 
    re_path(r'^comment/$', views.BoardComment.as_view(), name='user_list'),  # 댓글
    re_path(r'^category/$', views.Category.as_view(), name='user_list'),  # 게시물 필터 - 연애, 직장, 추천 등
 ```
 
 #### * 기능
 1. 게시물 올리기 - 사진 포함     
   -> 글쓴이 익명 처리 - 졸린 다람쥐 등
 2. 필터 별 게시물 확인
 3. 댓글 달기     
   -> 각 게시물 별 고유 익명, 단 게시물 별 익명 유지
 4. 좋아요 누르기/취소
 -----------------------
 > **MainParty**
 ```python
    re_path(r'^board/$', views.Board.as_view(), name=''),  # 게시물
    re_path(r'^review/$', views.Review.as_view(), name=''),  # 리뷰
    re_path(r'^qna/$', views.QNA.as_view(), name=''),  # 질문답변
    re_path(r'^category/$', views.Category.as_view(), name=''),  # 게시물 필터
    re_path(r'^attend/$', views.Attend.as_view()),  # 참석
 ```
 
#### * 기능
1. 리뷰는 참석자만 올릴 수 있다.
2. 필터 - 날짜, 참석나이, 위치로 분류해서 게시물 확인 가능
--------------------
> **SubParty**
```python
    re_path(r'^board/$', views.Board.as_view(), name=''),  # 게시물
    re_path(r'^category/$', views.Category.as_view(), name=''),  # 카테고리
    re_path(r'^addon/$', views.Addon.as_view(), name=''),  # 부가기능 - 찜, 좋아요
    re_path(r'^apply/$', views.Apply.as_view(), name=''),  # 파티 지원
    re_path(r'^myparty/$', views.MyParty.as_view(), name=''),  # 내 파티만
    re_path(r'^myattend/$', views.MyAttend.as_view(), name=''),  # 내가 참석한 파티만
    re_path(r'^mydibs/$', views.MyDibs.as_view(), name=''),  # 내가 찜한 파티만
    re_path(r'^userdetail/$', views.UserDetail.as_view(), name=''),  # 사용자 디테일 정보
    re_path(r'^usersimpledetail/$', views.UserSimpleDetail.as_view(), name=''),  # 사용자 기본 정보
```

#### * 기능
1. 필터 - 날짜, 성별, 카테고리로 분류해서 게시물 확인 가능
2. 각 게시물 별 찜, 좋아요 기능 제공
3. 참여하고 싶은 파티에 신청 가능
4. 서랍에서 "내가 만든 파티, 참석한 파티, 찜한 파티"로 나눠서 확인 가능
5. 요금 지불 시 사용자 신청자 디테일 정보 확인 가능
6. 요금 지불 시 주최자 기본 정보 확인 가능
----------------------------

> **PUSH**

#### * 기능
 사용자 FCM Token을 이용해 PUSH 서비스 처리
