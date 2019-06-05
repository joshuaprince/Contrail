from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic.base import TemplateView

from contrail.frontend.apps.contrailsite.forms import PriceForm
from contrail.frontend.field_info import FIELD_INFO
from contrail.frontend.query import *


class HomeView(TemplateView):
    """
    Render Home page
    """
    template_name = "home.html"


def price_view(request):
    """
    Render Price page
    """

    context = {'form': PriceForm({
        'amazon_web_services': True,
        'microsoft_azure': True,
        'on_demand': True,
        'reserved': True,
        'spot': True,
    }), 'aws_regions': list_regions('aws'),
    'azure_regions': list_regions('azure')}

    instance_filters = {}

    if request.method == 'POST':
        form = PriceForm(request.POST)

        if form.is_valid():
            context['form'] = form

            instance_filters = {'provider__in': [], 'priceType__in': []}

            if form.cleaned_data['amazon_web_services']:
                instance_filters['provider__in'].append('AmazonEC2')
            if form.cleaned_data['microsoft_azure']:
                instance_filters['provider__in'].append('Azure')

            if form.cleaned_data['on_demand']:
                instance_filters['priceType__in'].append('On Demand')
            if form.cleaned_data['reserved']:
                instance_filters['priceType__in'].append('Reserved')
            if form.cleaned_data['spot']:
                instance_filters['priceType__in'].append('Spot')

            if form.cleaned_data['operating_system']:
                instance_filters['operatingSystem'] = form.cleaned_data['operating_system']

            regions = []

            if form.cleaned_data['aws_region']:
                regions.extend(form.cleaned_data['aws_region'])

            if form.cleaned_data['azure_region']:
                regions.extend(form.cleaned_data['azure_region'])

            if len(regions) > 0:
                instance_filters['region__in'] = regions

            if form.cleaned_data['memory_from']:
                instance_filters['memory__gte'] = form.cleaned_data['memory_from']
            if form.cleaned_data['memory_to']:
                instance_filters['memory__lte'] = form.cleaned_data['memory_to']

            if form.cleaned_data['vcpu_from']:
                instance_filters['vcpu__gte'] = form.cleaned_data['vcpu_from']
            if form.cleaned_data['vcpu_to']:
                instance_filters['vcpu__lte'] = form.cleaned_data['vcpu_to']

            if form.cleaned_data['pricehr_from']:
                instance_filters['pricePerHour__gte'] = form.cleaned_data['pricehr_from']
            if form.cleaned_data['pricehr_to']:
                instance_filters['pricePerHour__lte'] = form.cleaned_data['pricehr_to']

    if [] in instance_filters.values():
        instances = []
    else:
        instances = list_instances(page=1, **instance_filters)  # TODO properly paginate

    for instance in instances:
        instance['url'] = reverse('instance') + '?' + urlencode(generate_detail_link_dict(instance))

    context['instances'] = instances

    return render(request, 'list.html', context)


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
        'currentPrices': get_instance_current_prices(**filter_parameters)
    }

    return render(request, 'instance.html', context)


def history_graph_view(request: HttpRequest):
    """
    Render price history graph asynchronously
    """
    filter_parameters = dict(request.GET.items())

    try:
        check_instance_detail_filters(**filter_parameters)
    except (AttributeError, AmbiguousTimeSeries) as e:
        return render(request, 'error.html', {'error': str(e)}, status=400)
    except InstanceNotFound as e:
        return render(request, 'error.html', {'error': '404: ' + str(e)}, status=404)

    context = {
        'priceHistory': get_instance_price_history(**filter_parameters)
    }

    return render(request, 'history_graph.html', context)


class HelpView(TemplateView):
    """
    Render Help page
    """
    template_name = "help.html"


def storage_view(request: HttpRequest):
    all_instances = list_storage()

    for instance_dict in all_instances:
        instance_dict['header'] = instance_dict.get('storageMedia') + ' ' + instance_dict.get('volumeType')

    all_instances.sort(key=lambda i: (i['region'], i['header']))
    headers = []
    for inst in all_instances:
        if inst['header'] not in headers:
            headers.append(inst['header'])

    context = {
        'headers': headers,
        'allInstances': all_instances,
    }

    return render(request, 'storage/storage.html', context)


class AboutUs(TemplateView):
    """
    Render About Us page
    """
    template_name = "about.html"
