from django.core import serializers
from django.shortcuts import render
from rest_framework import status, viewsets, generics
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

class DataViewSet(APIView):

    def post(self, request):

        return Response({}, status=HTTP_200_OK)
