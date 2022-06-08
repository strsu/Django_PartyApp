from rest_framework import serializers
from Profile.models import Filter

class FilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filter
        fields = [ #'f_uid',
                   'f_sort',
                   'f_type',
                   'f_name',
                   'f_seq']
