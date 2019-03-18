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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
                'operating_system': form.cleaned_data['operating_system'],
                'aws': form.cleaned_data['amazon_web_services'],
                'gcp': form.cleaned_data['google_cloud_platform'],
                'azure': form.cleaned_data['microsoft_azure'],
                'region': form.cleaned_data['region'],
                'vcpus': form.cleaned_data['vcpus'],
                'memory': form.cleaned_data['memory'],
                # 'ecu': form.cleaned_data['ecu']
            }

            # call rest api
            url = settings.URL + '/api/getinstances/'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            context['instances'] = json.loads(r.text)['instances']

    return render(request, 'price.html', context)


class CompareView(TemplateView):
    """
    Render Compare page
    """
    template_name = "compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
