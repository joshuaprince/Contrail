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

from config import CLICKHOUSE_DB_NAME, CLICKHOUSE_DB_URL
from loader.warehouse import InstanceData
from .serializers import *

import json

db = Database(CLICKHOUSE_DB_NAME, db_url=CLICKHOUSE_DB_URL, readonly=True)


class GetInstances(APIView):
        '''
        Given atributes, return instances and their prices
        Takes in (All fields optional)::
        {
            "providers": {
                "aws": true,
                "gcp": false,
                "azure": false
             },
             "vcpus": {
                "min": 0,
                "max": 10
             },
             "memory": {
                "min": 0,
                "max": 10
             },
             "price": {
                "min_hourly": 0,
                "max_hourly": 10,
                "min_upfront": 0,
                "max_upfront": 10
             },
             "regions": ["us-west-1"],
        }

        TODO paginate
        Returns (All fields required):
        [
            {
                "sku": "A1B2C3",
                "provider": "aws",
                "instance_type": "c4.4xlarge",
                "region": "US East",
                "vcpus": 8,
                "memory": 8,
                "price": {
                    "type": "on_demand"
                    "hourly": 0.233,
                    "upfront": 0
                }
            }, ...
        ]
        '''
        def get(self, request: Request):
            data = request.data
            print(data)

            # instances = InstanceData.objects_in(db).filter(onDemandPricePerUnit__ne=None).distinct()\
            #     .filter(instanceType__ne=None)\
            #     .only('location', 'instanceType', 'clockSpeed', 'memory', 'vcpu',
            #           # 'onDemandEffectiveDate', 'reservedEffectiveDate', 'spotTimestamp',
            #           'onDemandPricePerUnit', 'onDemandPriceUnit')\

            instances = InstanceData.objects_in(db).distinct()\
                .only('sku', 'region', 'instanceType', 'clockSpeed', 'memory', 'vcpu', 'pricePerHour', 'priceUpfront')
            # 'onDemandEffectiveDate', 'reservedEffectiveDate', 'spotTimestamp',

            # if request has a value, filter original query
            # TODO
            # if data['aws']: instances = instances.filter()
            # if data['gcp']: instances = instances.filter()
            # if data['azure']: instances = instances.filter()
            if data['region']: instances = instances.filter(region=data['region'])
            instances = instances.filter(
                vcpu__gte=data['vcpus']['min'], vcpu__lte=data['vcpus']['max'],
                memory__gte=data['memory']['min'], memory__lte=data['memory']['max'],
                pricePerHour__gte=data['price']['min_hourly'], pricePerHour__lte=data['price']['max_hourly'],
                priceUpfront__gte=data['price']['min_upfront'], priceUpfront__lte=data['price']['max_upfront']
            )

            # truncate query
            instances = instances.paginate(page_num=1, page_size=100).objects

            return Response({'instances': [InstanceDataSerializer(obj).data for obj in instances]}, status=HTTP_200_OK)




class GetInstanceDetail(APIView):
        '''
        Given atributes, return instances and their prices
        Takes in (All fields optional)::
        {
            "sku":  "A1B2C3"
        }

        TODO paginate
        Returns (All fields required):
        [
            {
                "sku": "A1B2C3",
                "provider": "aws",
                "instance_type": "c4.4xlarge",
                "region": "US East",
                "vcpus": 8,
                "memory": 8,
                "price": {
                    "type": "on_demand"
                    "hourly": 0.233,
                    "upfront": 0
                }
            }, ...
        ]
        '''
        def get(self, request: Request):
            # data = json.loads(request.body)
            data = request.POST
            print(data['sku'])

            instance = InstanceData.objects_in(db).filter(instanceType__ne=data['sku']).distinct()\
                .only('instanceType', 'region', 'clockSpeed', 'memory', 'vcpu', 'pricePerHour', 'priceUpfront',
                'networkPerformance', 'physicalCores', 'physicalProcessor', 'storageIsEbsOnly', 'storageCount',
                'storageCapacity', 'storageType', 'volumeType')[0]

            instance_serialized = InstanceDetailSerializer(instance)
            # instance = instance.paginate(page_num=1, page_size=100).objects

            # instance_serialized.priceHistory = InstanceData.objects_in(db).filter(sku=data['sku'])

            return Response({'instance': [instance_serialized.data]}, status=HTTP_200_OK)
            return Response(status=HTTP_200_OK)
