from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Auth.models import (
    User, 
    Userprofile, 
    AuthUser, 
    Userjwttoken, 
    Firebasetoken,
    Userauthlist
    )

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['uuid'] = user.u_uuid.hex()
        #token['id'] = user.u_id
        #token['pw'] = user.u_pw
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 
                   'u_uid',
                   'u_uuid',
                   'u_grade',
                   'u_id',
                   'u_pw',
                   'u_phone',
                   'u_sex',
                   'u_mainpic',
                   'u_point',
                   'u_emailnotify',
                   'u_smsnotify',
                   'u_pushnotify',
                   'u_registerdate',
                   #'u_withdrawaldate',
                   'u_lastlogin',
                   'u_introcode',
                   'u_appversion']

class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = [ 
            'up_useruuid',
            'up_name',
            'up_sex',
            'up_birth',
            'up_height',
            'up_body',
            'up_edu',
            'up_eduname',
            'up_live',
            'up_religion',
            'up_smoke',
            'up_alcohol',
            'up_nickname',
            'up_selfintro',
            'up_character',
            'up_requirepic',
            'up_extrapic'
            ]

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = [
            'password',
            'last_login',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined'
        ]

class UserjwttokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userjwttoken
        fields = [
            'ujt_key',
            'ujt_useruuid',
        ]

class FirebasetokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firebasetoken
        fields = [ 'fbt_useruuid',
                   'fbt_usertoken',
                   'fbt_generdate']

class UserauthlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userauthlist
        fields = [ 'ual_useruuid',
                   'ual_type',
                   'ual_require',
                   'ual_confirm',
                   'ual_return',
                   'ual_image'
                ]