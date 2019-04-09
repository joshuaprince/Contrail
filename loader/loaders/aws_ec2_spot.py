import collections
import itertools
import re
import logging

from crawler.providers.aws_ec2_spot import AmazonEC2Spot
from loader.warehouse import InstanceData, db
from loader.loaders import BaseLoader, register_loader
from loader.normalizers import normalizeData

logger = logging.getLogger('contrail.loader.aws_ec2')

def getSpotData(d, keys):
    attributes = []
    data = []
    for instance in d:
        attributes.append(instance.keys())
    attributes = sorted(set(list(itertools.chain(*attributes))))
    spot_attributes = sorted(set(attributes) - set(list(set(attributes) & set(keys))))
    qs = InstanceData.objects_in(db)
    qs = qs.filter(instanceType = instance['instanceType'])
    main = list(vars(qs[0]).items())[:70]
    # print(main)
    for i in qs:
        if list(vars(i).items())[:70] != main:
            print(set(list(vars(i).items())[:70]) - set(main))
            print(set(main) - set(list(vars(i).items())[:70]))
    for instance in d:
        values = []
        for i in attributes:
            try:
                try:
                    if normalizeData(i, instance[i]) == None:
                        pass
                    else:
                        key, value = normalizeData(i, instance[i])
                except(ValueError):
                    values.extend(normalizeData(i, instance[i]))
                    pass
                if isinstance(value, tuple):
                    values.extend((key, value))
                else:
                    values.append((key, value))
            except(KeyError, AttributeError):
                pass
        data.append(values)
    return data

@register_loader(provider=AmazonEC2Spot)
class AmazonEC2SpotLoader(BaseLoader):
    @classmethod
    def load(cls, filename: str, json: dict):
        logger.info("Loading {} into ClickHouse.".format(filename.split('/')[-1]))
        product_attributes = list(vars(InstanceData)['_fields'].keys())[:70]
        spot_data = getSpotData(json, product_attributes)
        # for k in spot_data:
        #     print(k)
        # print(spot_data)
        # data = {}
        # lst = []
        # for key, value in combineddata.items():
        #     for k, v in reserved_data.items():
        #         if k.startswith(key):
        #             lst.append(key)
        #             try:
        #                 data[k].append(value + v)
        #             except(KeyError):
        #                 data[k] = value + v
        #     if key not in set(lst):
        #         try:
        #             data[key].append(value)
        #         except(KeyError):
        #             data[key] = value

        # items = list(data.values())  # + spot_data
        # for item in items:
        #     instance = InstanceData()
        #     for i in item:
        #         setattr(instance, i[0], i[1])
        #     db.insert([instance])
