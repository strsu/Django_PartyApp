# #backend
 장고프레임워크_리액트 네이티브 앱 백엔드

## #데이터 베이스
![ullim_20220707_195114](https://user-images.githubusercontent.com/25381921/177757269-697721fd-1899-4f12-bd38-d08af4a543fa.png)

## #라이브러리
 
 1. djangorestframework-simplejwt, JWT 토큰 방식으로 보안처리 하기 위해서
 2. bcrypt, 패스워드 암호화에 이용
 3. firebase_admin, google fcm을 이용해서 PUSH 알림 및 백그라운드 MSG 송신 처리

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

 
