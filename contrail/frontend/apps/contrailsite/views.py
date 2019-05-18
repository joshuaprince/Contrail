import json
import requests

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from contrail.frontend.field_info import FIELD_INFO
from contrail.frontend.query import check_instance_detail_filters, InstanceNotFound, AmbiguousTimeSeries, \
    get_instance_details, get_instance_price_history
from .forms import *


class HomeView(TemplateView):
    """
    Render Home page
    """
    template_name = "home.html"


def price_view(request):
    """
    Render Price page
    """
    context = {'form':PriceForm()}

    if request.method == 'POST':
        form = PriceForm(request.POST)

        if form.is_valid():

            data = {
                "providers": {
                    "aws": form.cleaned_data['amazon_web_services'],
                    "gcp": form.cleaned_data['google_cloud_platform'],
                    "azure": form.cleaned_data['microsoft_azure']
                 },
                 "vcpus": {
                    "min": int(form.cleaned_data['vcpu_from']),
                    "max": int(form.cleaned_data['vcpu_to'])
                 },
                 "memory": {
                    "min": int(form.cleaned_data['memory_from']),
                    "max": int(form.cleaned_data['memory_to'])
                 },
                 "price": {
                    "price_type": {
                        "on_demand": form.cleaned_data['on_demand'],
                        "reserved": form.cleaned_data['reserved'],
                        "spot": form.cleaned_data['spot'],
                    },
                    "min_hourly": float(form.cleaned_data['pricehr_from']),
                    "max_hourly": float(form.cleaned_data['pricehr_to']),
                    "min_upfront": float(form.cleaned_data['price_from']),
                    "max_upfront": float(form.cleaned_data['price_to'])
                 },
                 "region": form.cleaned_data['region'],
            }


            # call rest api
            url = settings.URL + '/api/getinstances/'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(data), headers=headers).content.decode('utf-8')
            context['instances'] = json.loads(r)['instances']
            print(context['instances'])

            # Build instance url
            for instance in context['instances']:
                instance['url'] = "?"

                # if instance['provider'] == 'AmazonEC2':
                for discriminator in discriminators['AmazonEC2']:
                    if instance['url'][-1] != '?': instance['url'] += '&'
                    instance['url'] += discriminator
                    instance['url'] += '='
                    instance['url'] += instance[discriminator]

                print(instance['url'])



    return render(request, 'price.html', context)


def instance_view(request: HttpRequest):
    """
    Render Instance Detail page
    """

    filter_parameters = dict(request.GET.items())

    try:
        check_instance_detail_filters(**filter_parameters)
    except (AttributeError, AmbiguousTimeSeries) as e:
        return render(request, 'error.html', {'error': str(e)}, status=400)
    except InstanceNotFound as e:
        return render(request, 'error.html', {'error': '404: ' + str(e)}, status=404)

    instance_details = get_instance_details(**filter_parameters)  # raw instance details from database
    displayed_instance_details = []  # formatted instance details

    for key, value in instance_details.items():
        field_info = FIELD_INFO.get(key)

        if field_info and field_info.get('exclude'):
            continue

        if field_info:
            displayed_instance_details.append({
                'key': key,
                'name': field_info.get('friendlyName') or key,
                'value': value,
                'unit': field_info.get('unit') or '',
                'hint': field_info.get('hint') or '',
                'link': field_info.get('link') or ''
            })
        else:
            displayed_instance_details.append({'key': key, 'name': key, 'value': value})

    # Sort details by their order in FIELD_INFO, with fields that are not defined in FIELD_INFO last.
    displayed_instance_details.sort(key=lambda detail: list(FIELD_INFO.keys()).index(detail['key']) if detail['key'] in FIELD_INFO.keys() else 999)

    context = {
        'rawInstanceDetails': instance_details,
        'instanceDetails': displayed_instance_details,
        'priceHistory': get_instance_price_history(**filter_parameters)
    }

    return render(request, 'instance.html', context)


class HelpView(TemplateView):
    """
    Render Help page
    """
    template_name = "help.html"
