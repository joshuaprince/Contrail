from django import forms

from contrail.loader.warehouse import InstanceData, db


class PriceForm(forms.Form):
    OPSYS_CHOICES = ((x, x) for x in map(lambda i: i.operatingSystem, InstanceData.objects_in(db).distinct().only('operatingSystem')))


    PRICE_TYPE_CHOICES = (
        ('', 'All'),
        ('on_demand', 'On Demand'),
        ('reserved', 'Reserved'),
        ('spot', 'Spot')
    )

    REGION_CHOICES = ((x, x) for x in map(lambda i: i.region, InstanceData.objects_in(db).distinct().only('region')))

    amazon_web_services = forms.BooleanField(required=False, initial=True)
    microsoft_azure = forms.BooleanField(required=False, initial=True)

    operating_system = forms.ChoiceField(choices=OPSYS_CHOICES, required=False)
    region = forms.MultipleChoiceField(choices=REGION_CHOICES, required=False)
    memory_from = forms.FloatField(required=False)
    memory_to = forms.FloatField(required=False)

    vcpu_from = forms.IntegerField(required=False)
    vcpu_to = forms.IntegerField(required=False)

    on_demand = forms.BooleanField(required=False, initial=True)
    reserved = forms.BooleanField(required=False, initial=True)
    spot = forms.BooleanField(required=False, initial=True)

    # price_from = forms.CharField(required=False)
    # price_to = forms.CharField(required=False)

    pricehr_from = forms.FloatField(required=False)
    pricehr_to = forms.FloatField(required=False)
