from rest_framework import serializers

from .models import *


class InstanceDataSerializer(serializers.Serializer):
    region = serializers.CharField(source='location', allow_blank=True, max_length=127)
    instance_type = serializers.CharField(source='instanceType', allow_blank=True, max_length=127)
    clockSpeed = serializers.FloatField()
    memory = serializers.FloatField()
    retrieved_date = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()
    price_type = serializers.SerializerMethodField()
    price_unit = serializers.SerializerMethodField()

    # TODO temporary dummy fields
    vcpus = serializers.SerializerMethodField()
    operating_system = serializers.SerializerMethodField()

    def get_retrieved_date(self, obj):
        date = obj.onDemandEffectiveDate or obj.reservedEffectiveDate or obj.spotTimestamp
        if type(date) == str:
            return date
        return date.isoformat()

    def get_price_type(self, obj):
        if obj.onDemandEffectiveDate:
            return 'on_demand'

        if obj.reservedEffectiveDate:
            return 'reserved'

        if obj.spotTimestamp:
            return 'spot'

    def get_price(self, obj):
        price = obj.onDemandPricePerUnit or obj.reservedPricePerUnit
        return price

    def get_price_unit(self, obj):
        type = obj.onDemandPriceUnit or obj.reservedPriceUnit
        return type

    def get_vcpus(self, obj):
        return 8

    def get_operating_system(self, obj):
        return "Linux"
