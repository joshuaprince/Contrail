from typing import List

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
    productFamily = fields.StringField(default='VM')  # VM, Storage
    provider = fields.StringField()
    crawlTime = fields.DateTimeField()
    region = fields.StringField()
    operatingSystem = fields.StringField()

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
    operation = fields.NullableField(fields.StringField())
    physicalCores = fields.NullableField(fields.Int32Field())
    physicalProcessor = fields.NullableField(fields.StringField())
    preInstalledSw = fields.NullableField(fields.StringField())
    processorArchitecture = fields.NullableField(fields.StringField())
    processorFeatures = fields.NullableField(fields.StringField())
    provisioned = fields.NullableField(BooleanField())
    serviceName = fields.NullableField(fields.StringField())
    sku = fields.NullableField(fields.StringField())
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
    meterId = fields.NullableField(fields.StringField())
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
    engine = engines.MergeTree(
        date_col='crawlTime',
        order_by=[
            'productFamily',
            'provider',
            'region',
            'instanceType',
            'operatingSystem',
            'priceType',
            'crawlTime'
        ]
    )


class LoadedFile(models.Model):
    """
    Table that holds the full S3 path names of each file that has already been loaded, so that we don't load the
    same file twice.
    """
    filename = fields.StringField()
    time_loaded = fields.DateTimeField()

    engine = engines.MergeTree('time_loaded', ('filename', 'time_loaded'))


class InstanceDataLastPointView(InstanceData):
    """
    Model that we can use to query the aggregated "latest points" of each instance. This is a "fake model" in that it
    wraps a view, and therefore cannot be created with create_table or the like, and must be set up with the raw SQL in
    the `create_contrail_table` function.

    **This view ONLY CONTAINS 1yr/no upfront variants of reserved models.**
    """
    # Extends InstanceData. Contains ALL fields of InstanceData, instead queries from the view instancedatalastpointview
    engine = None


class InstanceDataLastPointViewAllReserved(InstanceData):
    """
    Model that we can use to query the aggregated "latest points" of each instance. This is a "fake model" in that it
    wraps a view, and therefore cannot be created with create_table or the like, and must be set up with the raw SQL in
    the `create_contrail_table` function.
    """
    # Extends InstanceData. Contains ALL fields of InstanceData, instead queries from the view instancedatalastpointview
    engine = None


def create_contrail_table(recreate=False):
    if db.does_table_exist(InstanceData) and not recreate:
        return

    if db.does_table_exist(InstanceData):
        db.drop_table(InstanceData)

    if db.does_table_exist(LoadedFile):
        db.drop_table(LoadedFile)

    db.raw("DROP TABLE IF EXISTS instancedata_last_point_aws")
    db.raw("DROP TABLE IF EXISTS instancedata_last_point_aws_all_reserved")
    db.raw("DROP TABLE IF EXISTS instancedatalastpointview")
    db.raw("DROP TABLE IF EXISTS instancedatalastpointviewallreserved")

    db.create_table(InstanceData)
    db.create_table(LoadedFile)

    db.raw(_generate_materialized_view_sql(True))
    db.raw(_generate_view_sql(True))
    db.raw(_generate_materialized_view_sql(False))
    db.raw(_generate_view_sql(False))


def fix_aggregated_data():
    """
    There's a strange bug involving materialized views, where the data isn't reflected correctly in materialized views
    after insertion. It can be fixed by deleting and recreating the materialized view.
    """
    # Default 60-second timeout isn't enough, this operation takes a while
    db_long = Database(CLICKHOUSE_DB_NAME, db_url=CLICKHOUSE_DB_URL, timeout=99999)

    db_long.raw("DROP TABLE IF EXISTS instancedata_last_point_aws")
    db_long.raw("DROP TABLE IF EXISTS instancedata_last_point_aws_all_reserved")
    db_long.raw("DROP TABLE IF EXISTS instancedatalastpointview")
    db_long.raw("DROP TABLE IF EXISTS instancedatalastpointviewallreserved")

    print("Fixing materialized view data. This will take a while, be patient.")
    db_long.raw(_generate_materialized_view_sql(True))
    db_long.raw(_generate_view_sql(True))
    print("Halfway done....")
    db_long.raw(_generate_materialized_view_sql(False))
    db_long.raw(_generate_view_sql(False))
    print("Done.")


GROUPED_COLS = ['productFamily', 'provider', 'region', 'operatingSystem', 'priceType', 'instanceType',
                'leaseContractLength', 'purchaseOption', 'offeringClass', 'storageMedia', 'volumeType']
"""InstanceData columns that should be part of the GROUP BY clause in the last point view"""


def _generate_materialized_view_sql(limit_reserved: bool):
    """
    Generate the SQL used to generate the materialized view used by the last point view
    :return:
    """
    selects = []  # type: List[str]

    for field in InstanceData.fields():
        if field == 'crawlTime':
            continue
        elif field in GROUPED_COLS:
            selects.append(field)
        else:
            selects.append("argMaxState({0}, crawlTime) AS {0}".format(field))

    # {selects} -> provider, argMaxState(vcpu, crawlTime) AS vcpu, ...
    # {groups} -> provider, region, ...
    return """
        CREATE MATERIALIZED VIEW {table_name}
        ENGINE = AggregatingMergeTree() PARTITION BY tuple()
        ORDER BY (productFamily, provider, operatingSystem, region, instanceType, priceType) POPULATE AS
        SELECT
            maxState(crawlTime) AS max_crawlTime,
            {selects}
        FROM instancedata
        WHERE (offeringClass IS NULL OR offeringClass = '' OR offeringClass = 'standard')
            {reserved_filter}
        GROUP BY
            {groups}
    """.format(
        table_name='instancedata_last_point_aws' if limit_reserved else 'instancedata_last_point_aws_all_reserved',
        selects=',\n'.join(selects),
        groups=',\n'.join(GROUPED_COLS),
        reserved_filter="""
            AND (leaseContractLength IS NULL OR leaseContractLength == '' OR leaseContractLength == '1yr')
            AND (purchaseOption IS NULL OR purchaseOption == '' OR purchaseOption == 'No Upfront')
        """ if limit_reserved else ""
    )


def _generate_view_sql(limit_reserved: bool):
    """
    Generate the SQL query required to create the InstanceDataLastPointView view
    """
    selects = []  # type: List[str]

    for field in InstanceData.fields():
        if field == 'crawlTime':
            continue
        elif field in GROUPED_COLS:
            selects.append(field)
        else:
            selects.append("argMaxMerge({0}) AS {0}".format(field))

    return """
        CREATE VIEW {table_name} AS
        SELECT
            maxMerge(max_crawlTime) AS crawlTime,
            {selects}
        FROM {source_table}
        GROUP BY
            {groups}
    """.format(
        table_name='instancedatalastpointview' if limit_reserved else 'instancedatalastpointviewallreserved',
        source_table='instancedata_last_point_aws' if limit_reserved else 'instancedata_last_point_aws_all_reserved',
        selects=',\n'.join(selects),
        groups=',\n'.join(GROUPED_COLS)
    )
