import re


def capacityStatusNormalizer(key, value):
    if key == 'capacitystatus':
        return ('capacityStatus', value)
    else:
        pass

def clockSpeedNormalizer(key, value):
    if key == 'clockSpeed':
        clock_speed_is_up_to = False
        if re.findall("Up to", value):
            clock_speed_is_up_to = True
        try:
            clock_speed = float(re.findall("\d+\.\d+", value)[0])
        except(IndexError):
            clock_speed = float(re.findall("\d+", value)[0])
        return ('clockSpeedIsUpTo', clock_speed_is_up_to), ('clockSpeed', clock_speed)
    else:
        pass

def dedicatedEbsThroughputNormalizer(key, value):
    if key == 'dedicatedEbsThroughput' and value != 'N/A':
        dedicated_ebs_throughput_is_up_to = False
        if re.findall("Upto", value):
            dedicated_ebs_throughput_is_up_to = True
        dedicated_ebs_throughput = int(re.findall("\d+", value)[0])
        return ('dedicatedEbsThroughputIsUpTo', dedicated_ebs_throughput_is_up_to), ('dedicatedEbsThroughput', dedicated_ebs_throughput)
    else:
        pass

def ecuNormalizer(key, value):
    if key == 'ecu':
        if value == 'Variable':
            return ('ecuIsVariable', True)
        elif value == 'NA':
            return ('ecuIsVariable', False)
        else:
            return ('ecuIsVariable', False), ('ecu', float(value))

def instanceskuNormalizer(key, value):
    if key == 'instancesku':
        return None
    else:
        pass

def licenseModelNormalizer(key, value):
    if key == 'licenseModel':
        if value == 'Bring your own license':
            return None
        else:
            return (key, value)
    else:
        pass

def maxThroughputvolumeNormalizer(key, value):
    if key == 'maxThroughputvolume':
        return ('maxThroughputVolume', value)
    else:
        pass

def maxVolumeSizeNormalizer(key, value):
    if key == 'maxVolumeSize':
        max_volume_size = int(re.findall("\d+", value)[0])
        return ('maxVolumeSize', max_volume_size)
    else:
        pass

def memoryNormalizer(key, value):
    if key == 'memory':
        if value == 'NA':
            pass
        else:
            try:
                memory = float(re.findall("\d+\.\d+", value)[0])
            except(IndexError):
                try:
                    memory = float(re.findall("\d+\,\d+", value)[0].replace(",", ""))
                except(IndexError):
                    memory = float(re.findall("\d+", value)[0])
            return ('memory', memory)
    else:
        pass

def normalizationSizeFactorNormalizer(key, value):
    if key == 'normalizationSizeFactor':
        if value == 'NA':
            pass
        else:
            try:
                normalization_size_factor = float(re.findall("\d+\.\d+", value)[0])
            except(IndexError):
                normalization_size_factor = float(re.findall("\d+", value)[0])
            return ('normalizationSizeFactor', normalization_size_factor)
    else:
        pass

def servicenameNormalizer(key, value):
    if key == 'servicename':
        return('serviceName', value)
    else:
        pass

def storageNormalizer(key, value):
    if key == 'storage':
        if value == 'EBS only':
            return ('storageIsEbsOnly', True)
        elif value != 'NA':
            try:
                storage_info = re.findall(r"(\d+)", value)
                storage_type = re.findall("\d+\s([^x]+)", value)[0]
                return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', storage_type)
            except(IndexError):
                storage_info = re.findall(r"(\d+)", value)
                return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', "HDD")
        else:
            pass
    else:
        pass

def usagetypeNormalizer(key, value):
    if key == 'usagetype':
        return ('usageType', value)
    else:
        pass

def USDNormalizer(key, value):
    if key == 'uSD':
        return ('pricePerHour', value)
    else:
        pass

def unitNormalizer(key, value):
    if key == 'unit':
        return ('priceUnit', value)
    else:
        pass

def spotPriceNormalizer(key, value):
    if key == 'spotPrice':
        return ('pricePerHour', value)
    else:
        pass

def servicecodeNormalizer(key, value):
    if key == 'servicecode':
        return ('provider', value)
    else:
        pass 

def operatingSystemNormalizer(key, value):
    if key == 'operatingSystem':
        return (key, value)
    else:
        pass

def productFamilyNormalizer(key, value):
    if key == 'productFamily':
        if 'Compute' in value:
            return (key, 'VM')
        elif value == 'Storage':
            return (key, 'Storage')
        else:
            return None
    else:
        pass

def tenancyNormalizer(key, value):
    if key == 'tenancy':
        if value == 'Shared':
            return (key, value)
        else:
            return None
    else:
        pass

def preInstalledSwNormalizer(key, value):
    if key == 'preInstalledSw':
        if value == 'NA':
            return (key, value)
        else:
            return None
    else:
        pass

def ProductDescriptionNormalizer(key, value):
    if key == 'productDescription':
        if value == 'Linux/UNIX':
            value = 'Linux'
        return ('operatingSystem', value)
    else:
        pass

def regionNormalizer(key, value):
    if key == 'region':
        regions = {
            'us-gov-east-1': 'AWS GovCloud (US-East)',
            'us-gov-west-1': 'AWS GovCloud (US)',
            'ap-east-1': 'Asia Pacific (Hong Kong)',
            'ap-northeast-1': 'Asia Pacific (Tokyo)',
            'ap-northeast-2': 'Asia Pacific (Seoul)',
            'ap-northeast-3': 'Asia Pacific (Osaka-Local)',
            'ap-south-1': 'Asia Pacific (Mumbai)',
            'ap-southeast-1': 'Asia Pacific (Singapore)',
            'ap-southeast-2': 'Asia Pacific (Sydney)',
            'ca-central-1': 'Canada (Central)',
            'cn-north-1': 'China (Beijing)',
            'cn-northwest-1': 'China (Ningxia)',
            'eu-central-1': 'EU (Frankfurt)',
            'eu-west-1': 'EU (Ireland)',
            'eu-west-2': 'EU (London)',
            'eu-west-3': 'EU (Paris)',
            'eu-north-1': 'EU (Stockholm)',
            'sa-east-1': 'South America (Sao Paulo)',
            'us-east-1': 'US East (N. Virginia)',
            'us-east-2': 'US East (Ohio)',
            'us-west-1': 'US West (N. California)',
            'us-west-2': 'US West (Oregon)'
        }
        return ('region', regions.get(value, value))
    else:
        pass

def timestampNormalizer(key, value):
    if key == 'timestamp':
        return ('crawlTime', value)
    else:
        pass

def availabilityZoneNormalizer(key, value):
    if key == 'availabilityZone':
        return (key, value)
    else:
        pass

def normalizeData(key, value):
    switcher = {
        'capacitystatus': capacityStatusNormalizer(key, value),
        'clockSpeed': clockSpeedNormalizer(key, value),
        'dedicatedEbsThroughput': dedicatedEbsThroughputNormalizer(key, value),
        'ecu': ecuNormalizer(key, value),
        'instancesku': instanceskuNormalizer(key, value),
        'licenseModel': licenseModelNormalizer(key, value),
        'maxThroughputvolume': maxThroughputvolumeNormalizer(key, value),
        'maxVolumeSize': maxVolumeSizeNormalizer(key, value),
        'memory': memoryNormalizer(key, value),
        'normalizationSizeFactor': normalizationSizeFactorNormalizer(key, value),
        'servicecode': servicecodeNormalizer(key, value),
        'servicename': servicenameNormalizer(key, value),
        'storage': storageNormalizer(key, value),
        'usagetype': usagetypeNormalizer(key, value),
        'uSD': USDNormalizer(key, value),
        'unit': unitNormalizer(key, value),
        'spotPrice': spotPriceNormalizer(key, value),
        'region': regionNormalizer(key, value),
        'operatingSystem': operatingSystemNormalizer(key, value),
        'productFamily': productFamilyNormalizer(key, value),
        'tenancy': tenancyNormalizer(key, value),
        'preInstalledSw': preInstalledSwNormalizer(key, value),
        'productDescription': ProductDescriptionNormalizer(key, value),
        'timestamp': timestampNormalizer(key, value),  # Spot only
        'availabilityZone': availabilityZoneNormalizer(key, value)  # Spot only
    }
    func = switcher.get(key, lambda: (key, str(value)))
    try:
        r = func()
        if r == None:
            pass
        else:
            return r
    except(TypeError):
        if func == None:
            pass
        else:
            return func