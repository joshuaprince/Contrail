from django.http import JsonResponse, HttpRequest
from django.views import View

from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK
)

from contrail.frontend.query import get_instance_details, check_instance_detail_filters, AmbiguousTimeSeries, \
    InstanceNotFound, get_instance_price_history
from contrail.loader.warehouse import InstanceData
from .serializers import *


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


class GetInstanceDetail(View):
    """
    Given attributes, return the details about a single instance, and the price history associated with that instance.

    Requires query string parameters of ``provider`` and ALL discriminators associated with that provider. Example:
    ``/detail?provider=AmazonEC2&instanceType=c4.4xlarge&region=useast1&operatingSystem=Linux``

    Returns a JSON dictionary containing:
      ``instanceDetail``, which lists ALL fields from the InstanceData table of the most recent entry matching the query

      ``priceHistory``, a list of price points, each with a crawlTime, priceType, pricePerHour, and priceUpfront

    Example return:
    {
      "instanceDetail": {
        "provider": "AmazonEC2",
        "processorArchitecture": "64-bit",
        "tenancy": "Shared",
        "instanceType": "c4.4xlarge",
        "usageType": "BoxUsage:c4.4xlarge",
        "enhancedNetworkingSupported": true,
        "physicalProcessor": "Intel Xeon E5-2666 v3 (Haswell)",
        "vcpu": 16,
        "crawlTime": "2019-05-10T01:44:21Z",
        "operatingSystem": "Linux",
        "description": "$0.796 per On Demand Linux c4.4xlarge Instance Hour",
        "locationType": "AWS Region",
        "region": "useast1",
        "location": "US East (N. Virginia)",
        "productFamily": "Compute Instance",
        "sku": "ARPJFM962U4P5HAT",
        "dedicatedEbsThroughput": 2000,
        "capacityStatus": "Used",
        "memory": 30.0,
      },
      "priceHistory": [
        {
          "crawlTime": "2019-05-10T01:44:21Z",
          "priceType": "On Demand",
          "pricePerHour": 0.796
        },
        {
          "crawlTime": "2019-05-10T01:44:21Z",
          "priceType": "Reserved",
          "leaseContractLength": "3yr",
          "pricePerHour": 0.407
        },
        {
          "crawlTime": "2019-05-10T01:44:21Z",
          "priceType": "Reserved",
          "leaseContractLength": "3yr",
          "priceUpfront": 9715.0
        },
      ]
    }
    """
    def get(self, request: HttpRequest):
        filter_parameters = dict(request.GET.items())

        # Validate the query parameters to ensure they produce exactly one unique instance.
        try:
            check_instance_detail_filters(**filter_parameters)
        except (AttributeError, AmbiguousTimeSeries) as e:
            return JsonResponse({'error': str(e)}, status=400)
        except InstanceNotFound as e:
            return JsonResponse({'error': str(e)}, status=404)

        latest_instance = get_instance_details(**filter_parameters)
        price_points = get_instance_price_history(**filter_parameters)

        return JsonResponse({
            'instanceDetail': latest_instance,
            'priceHistory': price_points
        })
