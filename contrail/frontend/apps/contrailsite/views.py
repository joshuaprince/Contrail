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
    context = {'form': PriceForm(), 'regions': (x for x in map(lambda i: i.region, InstanceData.objects_in(db).distinct().only('region')))}

    if request.method == 'POST':
        form = PriceForm(request.POST)

        if form.is_valid():
            instances = list_instances(
                page=0,
                amazonec2=bool(form.cleaned_data['amazon_web_services']),
                azure=bool(form.cleaned_data['microsoft_azure']),
                os=form.cleaned_data['operating_system'],
                region=form.cleaned_data['region'],
                onDemand=bool(form.cleaned_data['on_demand']),
                reserved=bool(form.cleaned_data['reserved']),
                spot=bool(form.cleaned_data['spot']),
                memory=(float(form.cleaned_data['memory_from']), float(form.cleaned_data['memory_to'])),
                vcpus=(int(form.cleaned_data['vcpu_from']), int(form.cleaned_data['vcpu_to'])),
                pricePerHour=(float(form.cleaned_data['pricehr_from']), float(form.cleaned_data['pricehr_to'])),
            )  # TODO properly paginate

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
        'priceHistory': get_instance_price_history(**filter_parameters)
    }

    return render(request, 'instance.html', context)


class HelpView(TemplateView):
    """
    Render Help page
    """
    template_name = "help.html"
