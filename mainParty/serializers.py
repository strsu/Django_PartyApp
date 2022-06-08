from rest_framework import serializers

from mainParty.models import (
    Mainparty,
    Boardaddon
)

class MainpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Mainparty
        fields = [ 
                    'mp_uid',
                    'mp_wdate',
                    'mp_writer',
                    'mp_title',
                    'mp_type',
                    'mp_place',
                    'mp_content',
                    'mp_pricem',
                    'mp_pricef',
                    'mp_ablem',
                    'mp_ablef',
                    'mp_condm',
                    'mp_condf',
                    'mp_like',
                    'mp_mdate',
                    'mp_support',
                    'mp_image'
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