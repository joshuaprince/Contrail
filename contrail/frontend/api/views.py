from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from infi.clickhouse_orm.database import Database

from config import CLICKHOUSE_DB_NAME, CLICKHOUSE_DB_URL
from contrail.loader.warehouse import InstanceData
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
        "gpus": {
            "min": 0,
            "max": 10
        },
        "price": {
            "price_type": "On Demand"
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
            "instanceType": "c4.4xlarge",
            "region": "US East",
            "vcpus": 8,
            "memory": 8,
            "priceType": "On Demand",
            "priceHourly": 0.233,
            "priceUpfront": 0
        }, ...
    ]
    '''
    def post(self, request: Request):
        data = request.data
        print(data)

        instances = InstanceData.objects_in(db).distinct()\
            .only('region', 'instanceType', 'clockSpeed', 'memory', 'vcpu', 'pricePerHour', 'priceUpfront')
        # 'onDemandEffectiveDate', 'reservedEffectiveDate', 'spotTimestamp',

        # if request has a value, filter original query
        # TODO
        # if data['aws']: instances = instances.filter()
        # if data['gcp']: instances = instances.filter()
        # if data['azure']: instances = instances.filter()
        if data['region']: instances = instances.filter(region=data['region'])
        # if data['price']['price_type']['on_demand']: instances = instances.filter(price_type="On Demand")
        # if data['price']['price_type']['reserved']: instances = instances.filter(price_type="Reserved")
        # if data['price']['price_type']['spot']: instances = instances.filter(price_type="Spot")
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
        "id":  "A1B2C3"
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
            "price": [
                {
                    "type": "on_demand"
                    "hourly": 0.233,
                    "upfront": 0
                },
                {
                    "type": "reserved"
                    "hourly": 0.233,
                    "upfront": 0
                },
                {
                    "type": "reserved",
                    "hourly": 0.233,
                    "upfront": 0
                },
            ]
            "networkPerformance": "..."
            ...
            "priceHistory":
        }, ...
    ]
    '''
    def get(self, request: Request):
        data = json.loads(request.body)
        print(data['id'])

        # TODO on_demand_instances = InstanceData.objects_in(db).filter(instanceType__eq=data['id'], priceType__eq='On Demand').distinct() \

        on_demand_instances = InstanceData.objects_in(db).filter(instanceType__ne=data['id']).distinct() \
            .only('provider', 'region', 'clockSpeed', 'priceType', 'pricePerHour', 'priceUpfront', 'memory', 'vcpu', 'gpu', \
            'capacityStatus', 'clockSpeedIsUpTo', 'clockSpeed', 'currentGeneration', 'dedicatedEbsThroughputIsUpTo', 'dedicatedEbsThroughput', 'ebsOptimized', \
            'ecuIsVariable', 'ecu', 'elasticGraphicsType', 'enhancedNetworkingSupported', 'fromLocation', 'fromLocationType', 'gpuMemory', 'group', 'groupDescription', \
            'instance', 'instanceFamily', 'instanceType', 'intelAvx2Available', 'intelAvxAvailable', 'intelTurboAvailable', 'licenseModel', 'location', 'locationType', \
            'maxIopsBurstPerformance', 'maxIopsVolume', 'maxThroughputVolume', 'maxVolumeSize', 'networkPerformance', 'normalizationSizeFactor', 'operatingSystem', 'operation', \
            'physicalCores', 'physicalProcessor', 'preInstalledSw', 'processorArchitecture', 'processorFeatures', 'productFamily', 'provisioned', 'serviceName', \
            'storageIsEbsOnly', 'storageCount', 'storageCapacity', 'storageType', 'storageMedia', 'tenancy', 'toLocation', 'toLocationType', 'usageType', 'volumeType', \
            'appliesTo', 'description', 'effectiveDate', 'beginRange', 'endRange', 'leaseContractLength', 'offeringClass', 'purchaseOption', \
            'meterSubCategory', 'maxResourceVolumeMb', 'osVhdSizeMb', 'hyperVGenerations', 'maxDataDiskCount', 'lowPriorityCapable', 'premiumIo', 'vcpusAvailable', 'vcpusPerCore')\
            # .order_by('-crawlTime').limit(20)
            # 'crawlTime', 'ephemeralOsDiskSupported', 'acus', 'combinedTempDiskAndCachedReadBytesPerSecond', 'combinedTempDiskAndCachedWriteBytesPerSecond', 'combinedTempDiskAndCachedIOPS', \
            # 'uncachedDiskBytesPerSecond', 'uncachedDiskIOPS', 'cachedDiskBytes', 'maxWriteAcceleratorDisksAllowed')


        # hourly_reserved_instances = InstanceData.objects_in(db).filter(instanceType__ne=data['id'], priceType__eq='Reserved', reservedType__eq='hourly').distinct() \
        #     .only('crawlTime', 'pricePerHour', 'priceUpfront').order_by('-crawlTime')

        # partial_reserved_instances = InstanceData.objects_in(db).filter(instanceType__ne=data['id'], priceType__eq='Reserved', reservedType__eq='partial').distinct() \
        #     .only('crawlTime', 'pricePerHour', 'priceUpfront').order_by('-crawlTime')

        # upfront_reserved_instances = InstanceData.objects_in(db).filter(instanceType__ne=data['id'], priceType__eq='Reserved', reservedType__eq='upfront').distinct() \
        #     .only('crawlTime', 'pricePerHour', 'priceUpfront').order_by('-crawlTime')

        serialized_instance = {

            "instance_type": on_demand_instances[0].instanceType,
            "sku": on_demand_instances[0].sku,
            "provider": on_demand_instances[0].provider,
            "region": on_demand_instances[0].region,
            "vcpus": on_demand_instances[0].vcpu,
            "memory": on_demand_instances[0].memory,
            "gpu": on_demand_instances[0].gpu,
            "price": [
                {
                    "type": "on_demand",
                    "hourly": on_demand_instances[0].pricePerHour,
                    "upfront": on_demand_instances[0].priceUpfront
                },
                # {
                #     "type": "hourly_reserved",
                #     "hourly": hourly_reserved_instances[0].pricePerHour,
                #     "upfront": hourly_reserved_instances[0].priceUpfront,
                # },
                # {
                #     "type": "partial_reserved",
                #     "hourly": partial_reserved_instances[0].pricePerHour,
                #     "upfront": partial_reserved_instances[0].priceUpfront,
                # },
                # {
                #     "type": "upfront_reserved",
                #     "hourly": upfront_reserved_instances[0].pricePerHour,
                #     "upfront": upfront_reserved_instances[0].priceUpfront,
                # },
            ],
            "capacityStatus": on_demand_instances[0].gpu,
            "clockSpeedIsUpTo": on_demand_instances[0].clockSpeedIsUpTo,
            "clockSpeed": on_demand_instances[0].clockSpeed,
            "currentGeneration": on_demand_instances[0].currentGeneration,
            "dedicatedEbsThroughputIsUpTo": on_demand_instances[0].dedicatedEbsThroughputIsUpTo,
            "dedicatedEbsThroughput": on_demand_instances[0].dedicatedEbsThroughput,
            "ebsOptimized": on_demand_instances[0].ebsOptimized,
            "ecuIsVariable": on_demand_instances[0].ecuIsVariable,
            "ecu": on_demand_instances[0].ecu,
            "elasticGraphicsType": on_demand_instances[0].elasticGraphicsType,
            "enhancedNetworkingSupported": on_demand_instances[0].enhancedNetworkingSupported,
            "fromLocation": on_demand_instances[0].fromLocation,
            "fromLocationType": on_demand_instances[0].fromLocationType,
            "gpuMemory": on_demand_instances[0].gpuMemory,
            "group": on_demand_instances[0].group,
            "groupDescription": on_demand_instances[0].groupDescription,
            "instance": on_demand_instances[0].instance,
            "instanceFamily": on_demand_instances[0].instanceFamily,
            "instanceType": on_demand_instances[0].instanceType,
            "instanceSKU": on_demand_instances[0].instanceSKU,
            "intelAvx2Available": on_demand_instances[0].intelAvx2Available,
            "intelAvxAvailable": on_demand_instances[0].intelAvxAvailable,
            "capacityStatus": on_demand_instances[0].gpu,
            "capacityStatus": on_demand_instances[0].gpu,

        }

        return Response(serialized_instance, status=HTTP_200_OK)
