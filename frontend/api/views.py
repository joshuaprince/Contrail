from django.core import serializers
from django.shortcuts import render
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, action
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from infi.clickhouse_orm.database import Database

from loader.loader import InstanceData
from .models import *
from .serializers import *


db = Database('contrail', db_url='http://54.153.73.138:8123', readonly=True)


class GetInstances(APIView):
        '''
        Given atributes, return instances and their prices
        @Josh
        Return (you can alter if need be)
        {
            "retrieved_date":
            "instance_type":
            TODO "operating_system":
            "provider":
            "region":
            TODO "vcpus":
            "memory":
            TODO "ecu":
            "pricing_method": "on_demand", "reserved", "spot"
            TODO "price":
        }
        '''
        def post(self, request: Request):
            c = InstanceData.objects_in(db).only('location', 'instanceType', 'clockSpeed', 'memory',
                                                 'onDemandEffectiveDate', 'reservedEffectiveDate', 'spotTimestamp').\
                distinct()#.paginate(page_num=1, page_size=100)

            return Response({'instances': [InstanceDataSerializer(obj).data for obj in c]}, status=HTTP_200_OK)
