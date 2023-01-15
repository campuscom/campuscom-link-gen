import sys
from urllib.parse import urlparse
import requests
import json
import time


def impact(product_url, config, retry_interval):
    params = {
        'DeepLink': product_url,
        'Type': 'Regular'
    }

    headers = {
        'Accept': 'application/json'
    }

    response = requests.post(
        f"https://api.impact.com/Mediapartners/{config['account_sid']}/Programs/{config['program_id']}/TrackingLinks",
        params=params,
        headers=headers,
        auth=(config['account_sid'], config['auth_token'])
    )

    if response.status_code == 200:
        return response.json()['TrackingURL']

    return ''


def awin(product_url, config, retry_interval):
    data = {
        "advertiserId": config['advertiser_id'],
        "destinationUrl": product_url,
        "parameters": {}
    }

    headers = {
        "Authorization": f"Bearer {config['token']}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://api.awin.com/publishers/{config['publisher_id']}/linkbuilder/generate",
        data=json.dumps(data),
        headers=headers
    )

    if response.status_code == 200:
        return response.json()['url']
    elif response.status_code == 429:
        if retry_interval:
            time.sleep(retry_interval)
            awin(product_url, config, retry_interval)

    return ''


def rakuten(product_url, config, retry_interval):
    data = {
        "url": product_url,
        "advertiser_id": config['advertiser_id']
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['token']}"
    }

    response = requests.post(
        'https://api.linksynergy.com/v1/links/deep_links',
        data=json.dumps(data),
        headers=headers
    )

    if response.status_code == 200:
        return response.json()['advertiser']['deep_link']['deep_link_url']
    else:
        print(response.text)
        sys.exit()
    return ''


def skimlinks(product_url, config, retry_interval):
    url = f"https://go.skimresources.com/?id={config['publisher_id']}&url={product_url}&sref={config['sref']}"
    return url


def get_provider(config, hostname):
    try:
        providers = config['tracking_url_providers']
        provider = providers[hostname]
    except KeyError:
        print('no providers configered')

    return provider


def get_link(config, product, retry_interval):
    o = urlparse(product[1])
    provider = get_provider(config, o.hostname)
    generator = eval(provider['provider_name'])
    return generator(product[1], provider, retry_interval)
