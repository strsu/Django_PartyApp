#from plistlib import UID
#from telnetlib import STATUS
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, FileResponse
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import os

class Image(APIView):
    def get(self, request, format=None):
        if not 'imageName' in request.GET:
            return Response(
                {"message": 'need parameter'}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            name = request.GET['imageName'].replace(' ', '/')
            img = open(os.path.join(settings.MEDIA_ROOT, name), mode='rb')
        #return HttpResponse(img, content_type="image/jpg")
        return FileResponse(img)
