from typing import Dict, List

from infi.clickhouse_orm.database import Database

from config import CLICKHOUSE_DB_NAME, CLICKHOUSE_DB_URL
from contrail.loader.warehouse import InstanceData, InstanceDataLastPointView

db = Database(CLICKHOUSE_DB_NAME, db_url=CLICKHOUSE_DB_URL, readonly=True)


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


PRICE_HISTORY_PARAMS = ['crawlTime', 'priceType', 'pricePerHour', 'priceUpfront', 'leaseContractLength']
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


def list_instances(page, **kwargs) -> List[Dict]:
    """
    List known instances satisfying the filter provided.

    :param kwargs: A set of filters to search for instances. These should follow Infi ORM query parameters:
                   https://github.com/Infinidat/infi.clickhouse_orm/blob/develop/docs/querysets.md#filtering

    :return: List of instance dicts
    """

    instances = InstanceDataLastPointView.objects_in(db).filter(**kwargs).paginate(page, LIST_QUERY_SIZE)[0]

    return [instance.to_dict() for instance in instances]


def get_instance_details(**kwargs) -> Dict:
    """
    Get details about a single instance described by `kwargs`.

    :param kwargs: A set of filters used to identify the desired instance. Must at least consist of the fields specified
                   by this provider's DISCRIMINATORS.

    :return: All known, most up-to-date details about the instance being queried.
    """

    latest_instance = InstanceData.objects_in(db).filter(**kwargs).order_by('-crawlTime')[0]

    # Filter out null fields and price-related fields from the instance dict
    latest_instance = {k: v for k, v in latest_instance.to_dict().items()
                       if k not in PRICE_HISTORY_PARAMS and v is not None}

    return latest_instance


def get_instance_price_history(**kwargs) -> Dict[str, List[Dict]]:
    """
    Get a set of time series, each containing price history points for a given instance and its pricing mode.

    :param kwargs: A set of filters used to identify the desired instance. Must at least consist of the fields specified
                   by this provider's DISCRIMINATORS.

    :return: A dict mapping a pricing mode (i.e. 'onDemand' or 'reserved1yrFullUpfront') to a List of "history points",
             where each history point is a dictionary consisting of crawlTime, priceType, and optionally pricePerHour,
             priceUpfront, and leaseContractLength.
    """

    base_query = InstanceData.objects_in(db).filter(**kwargs).distinct().only(*PRICE_HISTORY_PARAMS).order_by('-crawlTime')

    # Get a time series from the last several entries in the database that match this filter
    price_history = {
        'onDemand': base_query.filter(priceType='On Demand')[:100],
        'spot': base_query.filter(priceType='Spot')[:100],
        'reserved1yrFullUpfront': base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='1yr', purchaseOption='All Upfront')[:100],
        'reserved1yrPartialUpfront': base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='1yr', purchaseOption='Partial Upfront')[:100],
        'reserved1yrNoUpfront': base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='1yr', purchaseOption='No Upfront')[:100],
        'reserved3yrFullUpfront': base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='3yr', purchaseOption='All Upfront')[:100],
        'reserved3yrPartialUpfront': base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='3yr', purchaseOption='Partial Upfront')[:100],
        'reserved3yrNoUpfront': base_query.filter(priceType='Reserved', offeringClass='standard', leaseContractLength='3yr', purchaseOption='No Upfront')[:100],
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
        InstanceData.objects_in(db).filter(**kwargs).order_by('-crawlTime')[0]
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
