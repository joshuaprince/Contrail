from django.conf import settings
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .forms import *

import requests, json

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def priceview(request):
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
            text = r.text
            context['instances'] = json.loads(r.text)['instances']

    return render(request, 'price.html', context)


# class PriceView(FormView):
#     template_name = "price.html"
#     form_class = PriceForm
#     success_url = reverse_lazy('price')
#     instances = None
#
#     def form_valid(self, form):
#         print("FORM VALID")
#         data = {
#             'operating_system': form.cleaned_data['operating_system'],
#             'aws': form.cleaned_data['aws'],
#             'gcp': form.cleaned_data['gcp'],
#             'azure': form.cleaned_data['azure'],
#             'region': form.cleaned_data['region'],
#             'vcpus': form.cleaned_data['vcpus'],
#             'memory': form.cleaned_data['memory'],
#             'ecu': form.cleaned_data['ecu']
#         }
#         print(data)
#
#         # call rest api
#         url = settings.URL + '/api/getinstances/'
#         headers = {'content-type': 'application/json'}
#
#         r = requests.post(url, data=json.dumps(data), headers=headers)
#
#         self.instances = json.loads(r.text)['instances']
#         print(self.instances)
#
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(self.instances)
#         if self.instances: context['instances'] = self.instances
#         return context


class CompareView(TemplateView):
    template_name = "compare.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
