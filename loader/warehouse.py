from infi.clickhouse_orm import models, fields, engines
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.fields import Field


db: Database = Database('contrail')
"""ClickHouse Database connection object."""


class BooleanField(Field):
    # The ClickHouse column type to use
    db_type = 'UInt8'

    # The default value
    class_default = False

    def to_python(self, value, timezone_in_use):
        # Convert valid values to bool
        if value in (1, '1', True, 'True', 'Yes'):
            return True
        elif value in (0, '0', False, 'False', 'No'):
            return False
        else:
            raise ValueError('Invalid value for BooleanField: %r' % value)

    def to_db_string(self, value, quote=True):
        # The value was already converted by to_python, so it's a bool
        return '1' if value else '0'


class InstanceData(models.Model):
    capacityStatus = fields.NullableField(fields.StringField())
    clockSpeedIsUpTo = fields.NullableField(BooleanField())
    clockSpeed = fields.NullableField(fields.Float32Field()) #in GHz
    currentGeneration = fields.NullableField(BooleanField())
    dedicatedEbsThroughputIsUpTo = fields.NullableField(BooleanField())
    dedicatedEbsThroughput = fields.NullableField(fields.Int32Field()) #in Mbps
    ebsOptimized = fields.NullableField(BooleanField())
    ecuIsVariable = fields.NullableField(BooleanField())
    ecu = fields.NullableField(fields.Float32Field())
    elasticGraphicsType = fields.NullableField(fields.StringField())
    enhancedNetworkingSupported = fields.NullableField(BooleanField())
    fromLocation = fields.NullableField(fields.StringField())
    fromLocationType = fields.NullableField(fields.StringField())
    gpu = fields.NullableField(fields.Int32Field())
    gpuMemory = fields.NullableField(fields.StringField())
    group = fields.NullableField(fields.StringField())
    groupDescription = fields.NullableField(fields.StringField())
    instance = fields.NullableField(fields.StringField())
    instanceCapacity10xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity12xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity16xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity18xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity24xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity2xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity32xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity4xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity8xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacity9xlarge = fields.NullableField(fields.Int32Field())
    instanceCapacityLarge = fields.NullableField(fields.Int32Field())
    instanceCapacityMedium = fields.NullableField(fields.Int32Field())
    instanceCapacityXlarge = fields.NullableField(fields.Int32Field())
    instanceFamily = fields.NullableField(fields.StringField())
    instanceType = fields.NullableField(fields.StringField())
    instanceSKU = fields.NullableField(fields.StringField())
    intelAvx2Available = fields.NullableField(BooleanField())
    intelAvxAvailable = fields.NullableField(BooleanField())
    intelTurboAvailable = fields.NullableField(BooleanField())
    licenseModel = fields.NullableField(fields.StringField())
    location = fields.NullableField(fields.StringField())
    locationType = fields.NullableField(fields.StringField())
    maxIopsBurstPerformance = fields.NullableField(fields.StringField())
    maxIopsVolume = fields.NullableField(fields.StringField())
    maxThroughputVolume = fields.NullableField(fields.StringField())
    maxVolumeSize = fields.NullableField(fields.Int32Field()) #in TiB
    memory = fields.NullableField(fields.Float32Field()) #in GiB
    networkPerformance = fields.NullableField(fields.StringField())
    normalizationSizeFactor = fields.NullableField(fields.Float32Field())
    operatingSystem = fields.NullableField(fields.StringField())
    operation = fields.NullableField(fields.StringField())
    physicalCores = fields.NullableField(fields.Int32Field())
    physicalProcessor = fields.NullableField(fields.StringField())
    preInstalledSw = fields.NullableField(fields.StringField())
    processorArchitecture = fields.NullableField(fields.StringField())
    processorFeatures = fields.NullableField(fields.StringField())
    productFamily = fields.NullableField(fields.StringField())
    provisioned = fields.NullableField(BooleanField())
    serviceCode = fields.NullableField(fields.StringField())
    serviceName = fields.NullableField(fields.StringField())
    storageIsEbsOnly = fields.NullableField(BooleanField())
    storageCount = fields.NullableField(fields.Int32Field())
    storageCapacity = fields.NullableField(fields.Int32Field())
    storageType = fields.NullableField(fields.StringField())
    storageMedia = fields.NullableField(fields.StringField())
    tenancy = fields.NullableField(fields.StringField())
    toLocation = fields.NullableField(fields.StringField())
    toLocationType = fields.NullableField(fields.StringField())
    transferType = fields.NullableField(fields.StringField())
    usageType = fields.NullableField(fields.StringField())
    vcpu = fields.NullableField(fields.Int32Field())
    volumeType = fields.NullableField(fields.StringField())

    priceType = fields.NullableField(fields.StringField())
    appliesTo = fields.NullableField(fields.StringField())
    description = fields.NullableField(fields.StringField())
    effectiveDate = fields.NullableField(fields.DateTimeField())
    endRange = fields.NullableField(fields.Float32Field())
    offerTermCode = fields.NullableField(fields.StringField())
    rateCode = fields.NullableField(fields.StringField())
    pricePerUnit = fields.NullableField(fields.StringField())
    priceUnit = fields.NullableField(fields.StringField())
    leaseContractLength = fields.NullableField(fields.StringField())
    offeringClass = fields.NullableField(fields.StringField())
    purchaseOption = fields.NullableField(fields.StringField())
    timestamp = fields.NullableField(fields.StringField())
    spotInstanceType = fields.NullableField(fields.StringField())
    availabilityZone = fields.NullableField(fields.StringField())
    
    # onDemandAppliesTo = fields.NullableField(fields.StringField())
    # onDemandBeginRange = fields.NullableField(fields.StringField())
    # onDemandDescription = fields.NullableField(fields.StringField())
    # onDemandEffectiveDate = fields.NullableField(fields.DateTimeField())
    # onDemandEndRange = fields.NullableField(fields.Float32Field())
    # onDemandOfferTermCode = fields.NullableField(fields.StringField())
    # onDemandRateCode = fields.NullableField(fields.StringField())
    # onDemandPricePerUnit = fields.NullableField(fields.StringField())
    # onDemandPriceUnit = fields.NullableField(fields.StringField())

    # reservedAppliesTo = fields.NullableField(fields.StringField())
    # reservedBeginRange = fields.NullableField(fields.StringField())
    # reservedDescription = fields.NullableField(fields.StringField())
    # reservedEffectiveDate = fields.NullableField(fields.StringField())
    # reservedEndRange = fields.NullableField(fields.StringField())
    # reservedLeaseContractLength = fields.NullableField(fields.StringField())
    # reservedOfferTermCode = fields.NullableField(fields.StringField())
    # reservedOfferingClass = fields.NullableField(fields.StringField())
    # reservedPurchaseOption = fields.NullableField(fields.StringField())
    # reservedRateCode = fields.NullableField(fields.StringField())
    # reservedPricePerUnit = fields.NullableField(fields.StringField())
    # reservedPriceUnit = fields.NullableField(fields.StringField())

    # spotPrice = fields.NullableField(fields.StringField())
    # spotTimestamp = fields.NullableField(fields.StringField())
    # spotInstanceType = fields.NullableField(fields.StringField())
    # spotAvailabilityZone = fields.NullableField(fields.StringField())

    engine = engines.Memory()


def create_contrail_table(recreate=False):
    if db.does_table_exist(InstanceData):
        if recreate:
            db.drop_table(InstanceData)
        else:
            return

    db.create_table(InstanceData)
