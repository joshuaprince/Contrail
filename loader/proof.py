import json

fil = open('../tmp.json')
d = json.load(fil)

output = {}

for sku, product in d['products'].items():
    instanceType = product['attributes'].get('instanceType')

    prod_out = {'sku': sku}
    try:
        a = d['terms']['OnDemand'].get(sku)
        b = next(iter(a.values()))['priceDimensions']
        c = next(iter(b.values()))['description']
        prod_out['onDem'] = c
    except (KeyError, AttributeError):
        prod_out['onDem'] = None

    try:
        output[instanceType].append(prod_out)
    except KeyError:
        output[instanceType] = [prod_out]

for size, lst in output.items():
    print((size or "None") + "--------------------------------------------------------")

    for price in lst:
        print(price['onDem'] or "(none price)")
