from django.http import JsonResponse, HttpRequest
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View

from contrail.frontend.query import *


class GetInstances(View):
    """
    Given filter parameters in querystring in the format accepted by Infi Clickhouse, return a paginated list of
    instances.

    Example querystring:
    ``/instances?page=1&vcpu__gte=2&provider=Azure&region__ne=uswest1``
    Returns only instances with at least 2 vCPUs and that use Azure, but none that are in region uswest1.

    Example JSON return:
    {
      "instances": [
        {
          "priceType": "Reserved",
          "location": "US East (Ohio)",
          "sku": "PUVQARX8GDMUJC2E",
          "gpu": 0,
          "instanceType": "r5a.large",
          "provider": "AmazonEC2",
          "href": "/api/getinstancedetail/?instanceType=r5a.large&operatingSystem=Linux&region=useast2&provider=AmazonEC2",
          "operatingSystem": "Linux",
          "pricePerHour": 0.082,
          "priceUpfront": 0.0,
          "memory": 16.0,
          "crawlTime": "2019-05-19T03:15:38Z",
          "region": "useast2",
          "vcpu": 2
        },
        ...
      }
    }
    """
    def get(self, request: HttpRequest):
        filter_parameters = {k: v for k, v in request.GET.items() if k != 'page'}
        page_num = int(request.GET.get('page', 1))

        instances = list_instances(page_num, **filter_parameters)

        for instance in instances:
            instance['href'] = reverse('getinstancedetail') + '?' + urlencode(generate_detail_link_dict(instance))

        return JsonResponse({'instances': instances})


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
