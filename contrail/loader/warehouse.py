from infi.clickhouse_orm import models, fields, engines
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.fields import Field

from config import CLICKHOUSE_DB_URL, CLICKHOUSE_DB_NAME

db = Database(CLICKHOUSE_DB_NAME, db_url=CLICKHOUSE_DB_URL)
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
    # Universal fields ---------------------------------------------------------
    sku = fields.StringField()
    lastModified = fields.DateTimeField()
    region = fields.StringField()

    priceType = fields.StringField()  # On Demand, Reserved, Spot
    pricePerHour = fields.Float32Field(default=0)
    priceUpfront = fields.Float32Field(default=0)

    vcpu = fields.Int32Field()
    memory = fields.Float32Field()  # in GiB
    gpu = fields.NullableField(fields.Int32Field())

    # AWS Specific -------------------------------------------------------------
    capacityStatus = fields.NullableField(fields.StringField())
    clockSpeedIsUpTo = fields.NullableField(BooleanField())
    clockSpeed = fields.NullableField(fields.Float32Field())  # in GHz
    currentGeneration = fields.NullableField(BooleanField())
    dedicatedEbsThroughputIsUpTo = fields.NullableField(BooleanField())
    dedicatedEbsThroughput = fields.NullableField(fields.Int32Field())  # in Mbps
    ebsOptimized = fields.NullableField(BooleanField())
    ecuIsVariable = fields.NullableField(BooleanField())
    ecu = fields.NullableField(fields.Float32Field())
    elasticGraphicsType = fields.NullableField(fields.StringField())
    enhancedNetworkingSupported = fields.NullableField(BooleanField())
    fromLocation = fields.NullableField(fields.StringField())
    fromLocationType = fields.NullableField(fields.StringField())
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
    instanceType = fields.StringField()
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
    maxVolumeSize = fields.NullableField(fields.Int32Field())  # in TiB
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
    provider = fields.NullableField(fields.StringField())
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
    volumeType = fields.NullableField(fields.StringField())

    appliesTo = fields.NullableField(fields.StringField())
    description = fields.NullableField(fields.StringField())
    effectiveDate = fields.NullableField(fields.DateTimeField())
    beginRange = fields.NullableField(fields.Float32Field())
    endRange = fields.NullableField(fields.Float32Field())
    leaseContractLength = fields.NullableField(fields.StringField())
    offeringClass = fields.NullableField(fields.StringField())
    purchaseOption = fields.NullableField(fields.StringField())

    # Azure specific -----------------------------------------------------------
    meterSubCategory = fields.NullableField(fields.StringField())
    maxResourceVolumeMb = fields.NullableField(fields.Int32Field())
    osVhdSizeMb = fields.NullableField(fields.Int32Field())
    hyperVGenerations = fields.NullableField(fields.StringField())
    maxDataDiskCount = fields.NullableField(fields.Int16Field())
    lowPriorityCapable = fields.NullableField(BooleanField())
    premiumIo = fields.NullableField(BooleanField())
    vcpusAvailable = fields.NullableField(fields.Int16Field())
    vcpusPerCore = fields.NullableField(fields.Int16Field())
    ephemeralOsDiskSupported = fields.NullableField(BooleanField())
    acus = fields.NullableField(fields.UInt16Field())
    combinedTempDiskAndCachedReadBytesPerSecond = fields.NullableField(fields.UInt64Field())
    combinedTempDiskAndCachedWriteBytesPerSecond = fields.NullableField(fields.UInt64Field())
    combinedTempDiskAndCachedIOPS = fields.NullableField(fields.UInt64Field())
    uncachedDiskBytesPerSecond = fields.NullableField(fields.UInt64Field())
    uncachedDiskIOPS = fields.NullableField(fields.UInt64Field())
    cachedDiskBytes = fields.NullableField(fields.UInt64Field())
    maxWriteAcceleratorDisksAllowed = fields.NullableField(fields.StringField())

    # InstanceData ClickHouse configuration ====================================
    engine = engines.MergeTree('lastModified', ('priceType', 'instanceType'))


class LoadedFile(models.Model):
    """
    Table that holds the full S3 path names of each file that has already been loaded, so that we don't load the
    same file twice.
    """
    filename = fields.StringField()
    time_loaded = fields.DateTimeField()

    engine = engines.MergeTree('time_loaded', ('filename', 'time_loaded'))


def create_contrail_table(recreate=False):
    if db.does_table_exist(InstanceData) and not recreate:
        return

    if db.does_table_exist(InstanceData):
        db.drop_table(InstanceData)

    if db.does_table_exist(LoadedFile):
        db.drop_table(LoadedFile)

    db.create_table(InstanceData)
    db.create_table(LoadedFile)
