from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import *

import requests, json

class HomeView(TemplateView):
    """
    Render Home page
    """
    template_name = "home.html"


class InstanceView(TemplateView):
    """
    Render Home page
    """
    template_name = "instance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs['id']

        data = {'id': 'A1B2C3'}
        # data = {'sku': id}

        # call rest api
        url = settings.URL + '/api/getinstancedetail/'
        headers = {'content-type': 'application/json'}
        r = requests.get(url, data=json.dumps(data), headers=headers)
        context['instance'] = r.json()

        print(context['instance'])

        return context


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

    return render(request, 'price.html', context)


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
