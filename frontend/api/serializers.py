from rest_framework import serializers

from loader.warehouse import InstanceData, db


class InstanceDataSerializer(serializers.Serializer):
    # sku = serializers.CharField(source='instanceSKU', max_length=127)
    sku = serializers.CharField()

    region = serializers.CharField(allow_blank=True, max_length=127)
    instance_type = serializers.CharField(source='instanceType', allow_blank=True, max_length=127)
    clock_speed = serializers.FloatField(source='clockSpeed')
    memory = serializers.FloatField()
    vcpus = serializers.IntegerField(source='vcpu')
    # effectiveDate = serializers.SerializerMethodField()

    pricePerHour = serializers.FloatField()
    priceUpfront = serializers.FloatField()

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


class InstancePriceSerializer(serializers.Serializer):
    lastModified = serializers.DateTimeField()
    pricePerHour = serializers.FloatField()


class InstanceDetailSerializer(serializers.Serializer):
    # sku = serializers.CharField(source='instanceSKU', max_length=127)
    sku = serializers.CharField()

    region = serializers.CharField(allow_blank=True, max_length=127)
    instance_type = serializers.CharField(source='instanceType', allow_blank=True, max_length=127)
    clock_speed = serializers.FloatField(source='clockSpeed')
    memory = serializers.FloatField()
    vcpus = serializers.IntegerField(source='vcpu')
    # effectiveDate = serializers.SerializerMethodField()

    pricePerHour = serializers.FloatField()
    priceUpfront = serializers.FloatField()

    priceHistory = serializers.SerializerMethodField()

    networkPerformance = serializers.CharField(max_length=127)
    physicalCores = serializers.IntegerField()
    physicalProcessor = serializers.CharField(max_length=127)
    storageIsEbsOnly = serializers.BooleanField()
    storageCount = serializers.IntegerField()
    storageCapacity = serializers.IntegerField()
    storageType = serializers.CharField(max_length=127)

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

    def get_priceHistory(self, obj):
        return InstancePriceSerializer(list(InstanceData.objects_in(db).filter(sku=obj.sku)), many=True)
