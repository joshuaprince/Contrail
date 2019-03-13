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

import json

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
            data = json.loads(request.body)
            # print(data)

            instances = InstanceData.objects_in(db).filter(onDemandPricePerUnit__ne=None).distinct()\
                .filter(instanceType__ne=None, onDemandPricePerUnit__ne='0.0000000000')\
                .only('location', 'instanceType', 'clockSpeed', 'memory', 'vcpu',
                      # 'onDemandEffectiveDate', 'reservedEffectiveDate', 'spotTimestamp',
                      'onDemandPricePerUnit', 'onDemandPriceUnit')\

            # print(type(instances))
            # if request has a value, filter original query

            # if data['operating_system']: instances = instances.filter(operating_system=data['operating_system'])
            # if data['aws']: instances = instances.filter()
            # if data['gcp']: instances = instances.filter()
            # if data['azure']: instances = instances.filter()
            if data['region']: instances = instances.filter(location=data['region'])
            # if data['vcpus']: instances = instances.filter(=data['vcpus'])
            if data['memory']: instances = instances.filter(memory=data['memory'])
            # if data['ecu']: instances = instances.filter(=data['ecu'])

            # truncate query
            instances = instances.paginate(page_num=1, page_size=100).objects

            return Response({'instances': [InstanceDataSerializer(obj).data for obj in instances]}, status=HTTP_200_OK)
