from rest_framework import serializers


class InstanceDataSerializer(serializers.Serializer):
    # sku = serializers.CharField(source='instanceSKU', max_length=127)
    sku = serializers.SerializerMethodField()

    provider = serializers.CharField(max_length=127)
    crawlTime = serializers.DateTimeField()
    region = serializers.CharField(allow_blank=True, max_length=127)

    priceType = serializers.CharField(max_length=127)
    pricePerHour = serializers.FloatField()
    priceUpfront = serializers.FloatField()

    vcpus = serializers.IntegerField(source='vcpu')
    memory = serializers.FloatField()
    gpu = serializers.CharField(max_length=127)

    instance_type = serializers.CharField(source='instanceType', allow_blank=True, max_length=127)
    clock_speed = serializers.FloatField(source='clockSpeed')

    def get_sku(self, obj):
        return 'A1B2C3'



class InstanceDetailSerializer(serializers.Serializer):
    # sku = serializers.CharField(source='instanceSKU', max_length=127)
    sku = serializers.SerializerMethodField()

    provider = serializers.CharField(max_length=127)
    crawlTime = serializers.DateTimeField()
    region = serializers.CharField(allow_blank=True, max_length=127)

    priceType = serializers.CharField(max_length=127)
    pricePerHour = serializers.FloatField()
    priceUpfront = serializers.FloatField()

    vcpus = serializers.IntegerField(source='vcpu')
    memory = serializers.FloatField()
    gpu = serializers.CharField(max_length=127)

    capacityStatus = serializers.CharField(max_length=127)
    clockSpeedIsUpTo = serializers.BooleanField()
    clockSpeed = serializers.FloatField()  # in GHz
    currentGeneration = serializers.BooleanField()
    dedicatedEbsThroughputIsUpTo = serializers.BooleanField()
    dedicatedEbsThroughput = serializers.IntegerField()  # in Mbps
    ebsOptimized = serializers.BooleanField()
    ecuIsVariable = serializers.BooleanField()
    ecu = serializers.FloatField()
    elasticGraphicsType = serializers.CharField(max_length=127)
    enhancedNetworkingSupported = serializers.BooleanField()
    fromLocation = serializers.CharField(max_length=127)
    fromLocationType = serializers.CharField(max_length=127)
    gpuMemory = serializers.CharField(max_length=127)
    group = serializers.CharField(max_length=127)
    groupDescription = serializers.CharField(max_length=127)
    instance = serializers.CharField(max_length=127)
    instanceCapacity10xlarge = serializers.IntegerField()
    instanceCapacity12xlarge = serializers.IntegerField()
    instanceCapacity16xlarge = serializers.IntegerField()
    instanceCapacity18xlarge = serializers.IntegerField()
    instanceCapacity24xlarge = serializers.IntegerField()
    instanceCapacity2xlarge = serializers.IntegerField()
    instanceCapacity32xlarge = serializers.IntegerField()
    instanceCapacity4xlarge = serializers.IntegerField()
    instanceCapacity8xlarge = serializers.IntegerField()
    instanceCapacity9xlarge = serializers.IntegerField()
    instanceCapacityLarge = serializers.IntegerField()
    instanceCapacityMedium = serializers.IntegerField()
    instanceCapacityXlarge = serializers.IntegerField()
    instanceFamily = serializers.CharField(max_length=127)
    instanceType = serializers.CharField(max_length=127)
    instanceSKU = serializers.CharField(max_length=127)
    intelAvx2Available = serializers.BooleanField()
    intelAvxAvailable = serializers.BooleanField()
    intelTurboAvailable = serializers.BooleanField()
    licenseModel = serializers.CharField(max_length=127)
    location = serializers.CharField(max_length=127)
    locationType = serializers.CharField(max_length=127)
    maxIopsBurstPerformance = serializers.CharField(max_length=127)
    maxIopsVolume = serializers.CharField(max_length=127)
    maxThroughputVolume = serializers.CharField(max_length=127)
    maxVolumeSize = serializers.IntegerField()  # in TiB
    networkPerformance = serializers.CharField(max_length=127)
    normalizationSizeFactor = serializers.FloatField()
    operatingSystem = serializers.CharField(max_length=127)
    operation = serializers.CharField(max_length=127)
    physicalCores = serializers.IntegerField()
    physicalProcessor = serializers.CharField(max_length=127)
    preInstalledSw = serializers.CharField(max_length=127)
    processorArchitecture = serializers.CharField(max_length=127)
    processorFeatures = serializers.CharField(max_length=127)
    productFamily = serializers.CharField(max_length=127)
    provisioned = serializers.BooleanField()
    serviceName = serializers.CharField(max_length=127)
    storageIsEbsOnly = serializers.BooleanField()
    storageCount = serializers.IntegerField()
    storageCapacity = serializers.IntegerField()
    storageType = serializers.CharField(max_length=127)
    storageMedia = serializers.CharField(max_length=127)
    tenancy = serializers.CharField(max_length=127)
    toLocation = serializers.CharField(max_length=127)
    toLocationType = serializers.CharField(max_length=127)
    transferType = serializers.CharField(max_length=127)
    usageType = serializers.CharField(max_length=127)
    volumeType = serializers.CharField(max_length=127)

    appliesTo = serializers.CharField(max_length=127)
    description = serializers.CharField(max_length=127)
    effectiveDate = serializers.DateTimeField()
    beginRange = serializers.FloatField()
    endRange = serializers.FloatField()
    leaseContractLength = serializers.CharField(max_length=127)
    offeringClass = serializers.CharField(max_length=127)
    purchaseOption = serializers.CharField(max_length=127)

    # Azure specific -----------------------------------------------------------
    meterSubCategory = serializers.CharField(max_length=127)
    maxResourceVolumeMb = serializers.IntegerField()
    osVhdSizeMb = serializers.IntegerField()
    hyperVGenerations = serializers.CharField(max_length=127)
    maxDataDiskCount = serializers.IntegerField()
    lowPriorityCapable = serializers.BooleanField()
    premiumIo = serializers.BooleanField()
    vcpusAvailable = serializers.IntegerField()
    vcpusPerCore = serializers.IntegerField()
    ephemeralOsDiskSupported = serializers.BooleanField()
    acus = serializers.IntegerField()
    combinedTempDiskAndCachedReadBytesPerSecond = serializers.IntegerField()
    combinedTempDiskAndCachedWriteBytesPerSecond = serializers.IntegerField()
    combinedTempDiskAndCachedIOPS = serializers.IntegerField()
    uncachedDiskBytesPerSecond = serializers.IntegerField()
    uncachedDiskIOPS = serializers.IntegerField()
    cachedDiskBytes = serializers.IntegerField()
    maxWriteAcceleratorDisksAllowed = serializers.CharField(max_length=127)




    # def get_retrieved_date(self, obj):
    #     date = obj.onDemandEffectiveDate or obj.reservedEffectiveDate or obj.spotTimestamp
    #     if date is None:
    #         return None
    #     if type(date) == str:
    #         return date
    #     return date.isoformat()
    #
    # def get_price_type(self, obj):
    #     if obj.onDemandEffectiveDate:
    #         return 'on_demand'
    #
    #     if obj.reservedEffectiveDate:
    #         return 'reserved'
    #
    #     if obj.spotTimestamp:
    #         return 'spot'

    def get_sku(self, obj):
        return 'A1B2C3'
