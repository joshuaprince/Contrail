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

from loader.warehouse import InstanceData
from .serializers import *

import json

db = Database('contrail', db_url='http://54.153.73.138:8123', readonly=True)


class GetInstances(APIView):
        '''
        Given atributes, return instances and their prices
        Return
        {
            "instance_type": "c4"
            "operating_system": "Linux",
            "provider": "AWS",
            "region": "US East",
            "vcpus": 8,
            "memory": 8,
            "reserved", "spot",
            "price_type": "on_demand",
            "price": 0.233,
            "price_unit": "per hour"
        }
        '''
        def post(self, request: Request):
            data = json.loads(request.body)

            instances = InstanceData.objects_in(db).filter(onDemandPricePerUnit__ne=None).distinct()\
                .filter(instanceType__ne=None, onDemandPricePerUnit__ne='0.0000000000')\
                .only('location', 'instanceType', 'clockSpeed', 'memory', 'vcpu',
                      # 'onDemandEffectiveDate', 'reservedEffectiveDate', 'spotTimestamp',
                      'onDemandPricePerUnit', 'onDemandPriceUnit')\

            # if request has a value, filter original query
            # TODO
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
