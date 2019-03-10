from django.core import serializers
from django.shortcuts import render
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from .models import *
from .serializers import *

import json

class DataViewSet(viewsets.ModelViewSet):
    # queryset =
    # serializer_class = 

    @action(detail=False)
    def getinstances(self, request):
        '''
        Given atributes, return instances and their prices
        '''


        return Response({}, status=HTTP_200_OK)
