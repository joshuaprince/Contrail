from rest_framework import serializers


class InstanceDataSerializer(serializers.Serializer):
    region = serializers.CharField(allow_blank=True, max_length=127)
    instance_type = serializers.CharField(source='instanceType', allow_blank=True, max_length=127)
    clock_speed = serializers.FloatField(source='clockSpeed')
    memory = serializers.FloatField()
    vcpus = serializers.IntegerField(source='vcpu')
    # effectiveDate = serializers.SerializerMethodField()

    pricePerHour = serializers.FloatField()
    priceUpfront = serializers.FloatField()

    # TODO temporary dummy fields
    # operating_system = serializers.SerializerMethodField()

    def get_retrieved_date(self, obj):
        date = obj.onDemandEffectiveDate or obj.reservedEffectiveDate or obj.spotTimestamp
        if date is None:
            return None
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
