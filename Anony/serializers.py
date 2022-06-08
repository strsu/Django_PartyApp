from rest_framework import serializers

from Anony.models import (
    Anonyboard, 
    AnonyboardComment, 
    Boardaddon, 
    Filter, 
    Firebasetoken
)

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

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = [ 
                   #'f_uid',
                   'f_sort',
                   #'f_type',
                   'f_name',
                   'f_seq'
                ]

class FirebasetokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firebasetoken
        fields = [ 
                    'fbt_useruuid',
                    'fbt_usertoken',
                    'fbt_generdate'
                ]
