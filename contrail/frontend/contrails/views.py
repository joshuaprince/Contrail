from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from contrail.frontend.api.discriminators import *
from .forms import *

import requests, json

class HomeView(TemplateView):
    """
    Render Home page
    """
    template_name = "home.html"


def priceview(request):
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


def instanceview(request):
    """
    Render Instance Detail page
    """
    context = {}
    params = {}

    # build request params
    if request.GET.get('provider', None) == 'AmazonEC2':
        for discriminator in discriminators['AmazonEC2']:
            params[discriminator] = request.GET.get(discriminator, None)

    elif request.GET.get('provider', None) == 'Azure':
        for discriminator in discriminators['Azure']:
            params[discriminator] = request.GET.get(discriminator, None)


    # call rest api
    url = settings.URL + '/api/getinstancedetail/'
    r = requests.get(url, params=params)
    print(r)
    # context['instance'] = r.json()
    #
    # print(context['instance'])

    return render(request, 'instance.html', context)


def compareview(request):
    """
    Render Price page
    """
    context = {'form':PriceForm()}

    if request.method == 'POST':
        form = PriceForm(request.POST)

        if form.is_valid():

            data = {
                "providers": {
                    "aws": True,
                    "gcp": False,
                    "azure": False
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
            r = requests.get(url, data=json.dumps(data), headers=headers).content.decode('utf-8')
            context['instances'] = json.loads(r)['instances']
            print(context['instances'])

    return render(request, 'compare.html', context)
