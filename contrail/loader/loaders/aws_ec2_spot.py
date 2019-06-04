import collections
import logging

from infi.clickhouse_orm.database import Database

from contrail.crawler.providers.aws_ec2_spot import AmazonEC2Spot
from contrail.loader.warehouse import InstanceData
from contrail.loader.loaders import BaseLoader, register_loader
from contrail.loader.normalizers import normalizeData

logger = logging.getLogger('contrail.loader.aws_ec2')

def nested_dict_iter(nested):
    lower = lambda s: s[:1].lower() + s[1:] if s else ''
    for key, value in nested.items():
        if isinstance(value, collections.abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield lower(key), value

def getSpotData(d, last_modified, region):
    attributes = []
    data = []
    for instance in d:
        values = []
        for key, value in dict(nested_dict_iter(instance)).items():
            try:
                try:
                    if normalizeData(key, value) == None:
                        pass
                    else:
                        key, value = normalizeData(key, value)
                except(ValueError):
                    values.extend(normalizeData(key, value))
                    pass
                if isinstance(value, tuple):
                    values.extend((key, value))
                else:
                    values.append((key, value))
            except(KeyError, AttributeError):
                pass
        k, v = normalizeData('region', region)
        values += [('priceType', 'Spot'), (k, v), ['provider', 'AmazonEC2']]

        instanceType = [val for val in values if val[0] == 'instanceType'][0][1]

        data.append(values)
    return data


@register_loader(provider=AmazonEC2Spot)
class AmazonEC2SpotLoader(BaseLoader):
    @classmethod
    def load(cls, filename: str, json: dict, last_modified: str, db: Database):
        logger.info("Loading {} into ClickHouse.".format(filename.split('/')[-1]))
        region = "{}".format(filename.split('/')[1])
        spot_data = getSpotData(json, last_modified, region)

        instances = []
        for item in spot_data:
            instance = InstanceData()
            for i in item:
                setattr(instance, i[0], i[1])
            instances.append(instance)
        insertables = [instances[i * 1000:(i + 1) * 1000] for i in range((len(instances) + 1000 - 1) // 1000 )] 
        for inst in insertables:
            db.insert(inst)
