from typing import Dict, List

from cachetools import cached, TTLCache
from infi.clickhouse_orm.database import Database

from contrail.configuration import config
from contrail.loader.warehouse import InstanceData, InstanceDataLastPointView, InstanceDataLastPointViewAllReserved, InstanceDataHourlyPriceView, InstanceDataDailyPriceView, InstanceDataMonthlyPriceView

db = Database(config['CLICKHOUSE']['db_name'], db_url=config['CLICKHOUSE']['db_url'], readonly=True)


LIST_QUERY_SIZE = 1000
"""Number of instances to list on a single page"""


DISCRIMINATORS = {
    'AmazonEC2': [
        'provider',
        'instanceType',
        'region',
        'operatingSystem'
    ],
    'Azure': [
        'provider',
        'instanceType',
        'region',
        'operatingSystem'
    ]
}
"""
A Dict that maps each provider to the set of fields needed to uniquely identify an instance of that provider. For
example, Amazon instances have dimensions of instance type, region, and operating system, so uniquely identifying a time
series requires that we filter by at least those fields.
"""


PRICE_HISTORY_PARAMS = ['crawlTime', 'priceType', 'pricePerHour', 'priceUpfront', 'leaseContractLength', 'purchaseOption']
"""
The set of fields that vary over an instance's time series, and therefore should be included in price history data and
excluded from instance details.
"""


def generate_detail_link_dict(instance: Dict) -> Dict:
    """
    Generate a dictionary that consists of this instance's provider discriminators, so that we can convert it to a link
    to the instance detail page.

    :param instance: A dict representing an instance, that contains `provider` keys and keys for all discriminators of
    that provider.

    :return: e.g.   {
                        'provider': 'AmazonEC2',
                        'instanceType': 'c4.xlarge',
                        'operatingSystem': 'Linux',
                        'region': 'apeast1'
                    }
    """
    provider = instance['provider']

    details = {discriminator: instance[discriminator] for discriminator in DISCRIMINATORS[provider]}

    return details


@cached(cache=TTLCache(maxsize=10, ttl=86400))
def list_regions(provider) -> List[str]:
    """
    List all regions found in the  `region` column of InstanceDataLastPointView.
    """
    if provider == 'aws':
        return list(map(lambda i: i.region, InstanceData.objects_in(db).filter(provider='AmazonEC2').distinct().only('region').order_by('region')))
    else:
        return list(map(lambda i: i.region, InstanceData.objects_in(db).filter(provider='Azure').distinct().only('region').order_by('region')))


def list_instances(page, **kwargs) -> List[Dict]:
    """
    List known instances satisfying the filter provided.

    :param kwargs: A set of filters to search for instances. These should follow Infi ORM query parameters:
                   https://github.com/Infinidat/infi.clickhouse_orm/blob/develop/docs/querysets.md#filtering

    :return: List of instance dicts
    """

    # Only query for the fields we need on an instance list
    fields = ['crawlTime', 'provider', 'instanceType', 'region', 'operatingSystem', 'vcpu', 'memory', 'priceType',
              'pricePerHour', 'priceUpfront', 'gpu', 'location']

    instances = InstanceDataLastPointView.objects_in(db).filter(productFamily='VM', **kwargs).only(*fields).paginate(page, LIST_QUERY_SIZE)[0]

    return [{k: v for k, v in instance.to_dict().items() if v} for instance in instances]


def get_instance_details(**kwargs) -> Dict:
    """
    Get details about a single instance described by `kwargs`.

    :param kwargs: A set of filters used to identify the desired instance. Must at least consist of the fields specified
                   by this provider's DISCRIMINATORS.

    :return: All known, most up-to-date details about the instance being queried.
    """

    query = InstanceDataLastPointView.objects_in(db).distinct().filter(**kwargs)

    instance_details = {}

    # Collect all details from all versions of this instance, because the "On Demand" record might know more details
    #   than the "Spot" record, for example.
    for record in query:
        for k, v in record.to_dict().items():
            # Filter out null fields and price-related fields from the instance dict
            if k not in PRICE_HISTORY_PARAMS and bool(v):
                instance_details[k] = v

    return instance_details


def get_instance_current_prices(**kwargs) -> Dict[str, Dict]:
    """
    Get a dict of current pricing modes for this instance.

    :param kwargs: A set of filters used to identify the desired instance. Must at least consist of the fields specified
                   by this provider's DISCRIMINATORS.

    :return: A dict mapping a pricing mode (i.e. 'onDemand' or 'reserved1yrFullUpfront') to a price dict that consists
    of crawlTime and pricePerHour, and priceUpfront if nonzero.
    """

    query = InstanceDataLastPointViewAllReserved.objects_in(db).filter(**kwargs)\
                .distinct().only(*PRICE_HISTORY_PARAMS).order_by('crawlTime')

    price_modes = {}

    for record in query:  # type: InstanceData
        price_dict = {'crawlTime': record.crawlTime, 'pricePerHour': record.pricePerHour}
        if record.priceType == 'On Demand':
            price_modes['onDemand'] = price_dict
        elif record.priceType == 'Spot':
            price_modes['spot'] = price_dict
        else:
            # Reserved price
            if record.purchaseOption == 'All Upfront':
                price_dict['priceUpfront'] = record.priceUpfront
                price_modes['reserved{}FullUpfront'.format(record.leaseContractLength)] = price_dict
            elif record.purchaseOption == 'Partial Upfront':
                price_dict['priceUpfront'] = record.priceUpfront
                price_modes['reserved{}PartialUpfront'.format(record.leaseContractLength)] = price_dict
            elif record.purchaseOption == 'No Upfront':
                price_dict['priceUpfront'] = record.priceUpfront
                price_modes['reserved{}NoUpfront'.format(record.leaseContractLength)] = price_dict

    return price_modes


def get_instance_price_history(record_count=100, **kwargs) -> Dict[str, List[Dict]]:
    """
    Get a set of time series, each containing price history points for a given instance and its pricing mode.

    :param record_count: Number of history points to retrieve per pricing mode.

    :param kwargs: A set of filters used to identify the desired instance. Must at least consist of the fields specified
                   by this provider's DISCRIMINATORS.

    :return: A dict mapping a pricing mode (i.e. 'onDemand' or 'reserved1yrFullUpfront') to a List of "history points",
             where each history point is a dictionary consisting of crawlTime, priceType, and optionally pricePerHour,
             priceUpfront, and leaseContractLength.
    """
    # hourly_base_query = InstanceDataHourlyPriceView.objects_in(db).filter(**kwargs).only(*PRICE_HISTORY_PARAMS).order_by('-crawlTime')
    daily_base_query = InstanceDataDailyPriceView.objects_in(db).filter(**kwargs).only(*PRICE_HISTORY_PARAMS).order_by('-crawlTime')
    monthly_base_query = InstanceDataMonthlyPriceView.objects_in(db).filter(**kwargs).only(*PRICE_HISTORY_PARAMS).order_by('-crawlTime')
    # base_query = InstanceData.objects_in(db).filter(**kwargs).distinct().only(*PRICE_HISTORY_PARAMS).order_by('-crawlTime')
    # Get a time series from the last several entries in the database that match this filter

    price_history = {
        # 'hourlyOnDemand': list(hourly_base_query.filter(priceType='On Demand')[:record_count]),
        # 'hourlySpot': list(hourly_base_query.filter(priceType='Spot')[:record_count]),
        # 'hourlyReserved1yrNoUpfront': list(hourly_base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='1yr', purchaseOption='No Upfront')[:record_count]),
        'dailyOnDemand': list(daily_base_query.filter(priceType='On Demand')[:record_count]),
        'dailySpot': list(daily_base_query.filter(priceType='Spot')[:record_count]),
        'dailyReserved1yrNoUpfront': list(daily_base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='1yr', purchaseOption='No Upfront')[:record_count]),
        'monthlyOnDemand': list(monthly_base_query.filter(priceType='On Demand')[:record_count]),
        'monthlySpot': list(monthly_base_query.filter(priceType='Spot')[:record_count]),
        'monthlyReserved1yrNoUpfront': list(monthly_base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='1yr', purchaseOption='No Upfront')[:record_count]),
    }
    # Build our own list of "price history point" dicts, since we don't want to include null or zero fields
    price_history_points = {k: [] for k, v in price_history.items() if v}
    for price_mode in price_history.keys():
        for inst in price_history[price_mode]:
            current_inst = {}
            for param in PRICE_HISTORY_PARAMS:
                if getattr(inst, param) is not None:
                    current_inst[param] = getattr(inst, param)
            price_history_points[price_mode].append(current_inst)

    return price_history_points


def check_instance_detail_filters(**kwargs):
    """
    Ensure that the filters used to query a single instance return **exactly one unique instance**, raising an exception
    otherwise.

    :param kwargs: Set of filters used to identify the desired instance.
    :except AttributeError: if a provided field does not exist in the instance data.
    :except AmbiguousTimeSeries: if the filters provided are not enough to distinctly identify one instance.
    :except InstanceNotFound: if there are no instances in the database that match the provided filters.
    """

    if 'provider' not in kwargs.keys():
        raise AmbiguousTimeSeries("provider must be specified")

    if kwargs['provider'] not in DISCRIMINATORS.keys():
        raise InstanceNotFound("Unknown provider: " + kwargs['provider'])

    # Queries must specify all discriminators, else returned price history will be ambiguous.
    for discriminator in DISCRIMINATORS[kwargs['provider']]:
        if discriminator not in kwargs.keys():
            raise AmbiguousTimeSeries("Missing discriminator: " + discriminator)

    try:
        InstanceDataLastPointView.objects_in(db).filter(**kwargs).order_by('-crawlTime')[0]
    except AttributeError:
        raise
    except StopIteration:
        raise InstanceNotFound("No instance found matching query.")


class AmbiguousTimeSeries(LookupError):
    """
    Error raised if attempting to query a single instance, but the filters provided may return two or more instances.
    """
    pass


class InstanceNotFound(LookupError):
    """
    Error raised if attempting to query a single instance, but no such instance exists.
    """
    pass


def list_storage():
    """
    List all current storage options and their prices.
    :return:
    """
    fields = ['crawlTime', 'provider', 'region', 'pricePerHour', 'maxThroughputVolume', 'storageMedia', 'volumeType']
    instances = InstanceDataLastPointView.objects_in(db).filter(productFamily='Storage').only(*fields).distinct()

    instance_dicts = []
    for instance in instances:
        instance_dict = {}
        for k, v in instance.to_dict().items():
            if k == 'pricePerHour':
                k = 'pricePerGbMonth'
            if v:
                instance_dict[k] = v
        instance_dicts.append(instance_dict)

    return instance_dicts
