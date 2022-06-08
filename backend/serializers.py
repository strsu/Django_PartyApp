from dataclasses import field
from rest_framework import serializers

from backend.models import *


class AcquainblockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquainblock
        fields = [ 
            'db_uuid',
            'db_phone'
        ]


class AnonyboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anonyboard
        fields = [ 
            'ab_uid',
            'ab_writer_uuid',
            'ab_writer_a',
            'ab_sex',
            'ab_type',
            'ab_title',
            'ab_content',
            'ab_wdate',
            'ab_udate',
            'ab_ddate',
            'ab_like',
            'ab_read',
            'ab_comment',
            'ab_image'
        ]


class AnonyboardCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonyboardComment
        fields = [
            'ac_uid',
            'ac_refid',
            'ac_replyer_uuid',
            'ac_replyer_a',
            'ac_sex',
            'ac_wdate',
            'ac_content',
            'ac_like',
            'ac_seqm',
            'ac_issub'
        ]


class BoardaddonSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Boardaddon
        fields = [ 
           'ba_uuid',
           'ba_tablename',
           'ba_type',
           'ba_boardid',
           'ba_commentid'
        ]


class CouponlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Couponlist
        fields = [
            'cl_couponid',
            'cl_title',
            'cl_createdate',
            'cl_issuedate',
            'cl_expiredate',
            'cl_couponcode',
            'cl_func',
            'cl_image'
        ]


class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = [
            'f_uid',
            'f_sort',
            'f_type',
            'f_name',
            'f_seq'
        ]


class FirebasetokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firebasetoken
        fields = [
            'fbt_uid',
            'fbt_useruuid',
            'fbt_usertoken',
            'fbt_generdate'
        ]


class IntroblockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introblock
        fields = [
            'ib_blocker',
            'ib_type',
            'ib_blocked'
        ]


class MainpartyAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainpartyAttend
        fields = [
            'mpa_uid',
            'mpa_boardid',
            'mpa_useruuid',
            'mpa_timeline',
            'mpa_signtime'
        ]

class MainpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mainparty
        fields=[
            'mp_uid',
            'mp_wdate',
            'mp_writer',
            'mp_title',
            'mp_type',
            'mp_place',
            'mp_content',
            'mp_maxage',
            'mp_minage',
            'mp_like',
            'mp_mdate',
            'mp_support',
            'mp_image',
        ]


class MainpartyReviewQnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainpartyReviewQna
        fields=[
            'mprq_uid',
            'mprq_boardid',
            'mprq_type',
            'mprq_uuid',
            'mprq_nickname',
            'mprq_content',
            'mprq_date',
            'mprq_adminuuid',
            'mprq_admincontent',
            'mprq_admindate',
            'mprq_score',
            'mprq_helpcnt'
        ]


class MainpartyTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainpartyTimeline
        fields = [
            'mpt_uid',
            'mpt_boardid',
            'mpt_time',
            'mpt_signm',
            'mpt_signw',
            'mpt_attendm',
            'mpt_attendw',
            'mpt_pricem',
            'mpt_pricew',
            'mpt_minagem',
            'mpt_maxagem',
            'mpt_minagew',
            'mpt_maxagew',
            'mpt_deadline',
            'mpt_condm',
            'mpt_condw'
        ]


class RecommanduserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommanduser
        fields = [
            'ru_uuida',
            'ru_uuidb',
            'ru_rcmdate',
            'ru_dateatob',
            'ru_datebtoa',
            'ru_scoreatob',
            'ru_scoebtoa',
            'ru_isreject'
        ]


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
            'u_withdrawaldate',
            'u_lastlogin',
            'u_introcode',
            'u_appversion'
        ]


class UserauthlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userauthlist
        fields = [
            'ual_useruuid',
            'ual_type',
            'ual_require',
            'ual_confirm',
            'ual_return',
            'ual_image'
        ]


class UsercouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usercoupon
        fields = [
            'uc_idx',
            'uc_useruuid',
            'uc_couponid',
            'uc_receivedate',
            'uc_expiredate',
            'uc_isuse'
        ]


class UserjwttokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userjwttoken
        fields = [
            'ujt_key',
            'ujt_useruuid'
        ]


class UserpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Userparty
        fields = [
            'up_uid',
            'up_useruuid',
            'up_nickname',
            'up_sex',
            'up_tags',
            'up_title',
            'up_content',
            'up_state',
            'up_wdate',
            'up_udate',
            'up_ddate',
            'up_mdate',
            'up_like',
            'up_read',
            'up_image'
        ]


class UserpartyAttendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserpartyAttend
        fields = [
            'upa_uid',
            'upa_boardid',
            'upa_ownuuid',
            'upa_useruuid',
            'upa_attend'
        ]


class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields = [
            'up_uid',
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
            'up_hobby',
            'up_interest',
            'up_datestyle',
            'up_requirepic',
            'up_extrapic'
        ]
