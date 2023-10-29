from iso3166 import countries
import requests

def fetch_country(country: str) -> dict:
    try:
        if len(country) != 2:
            raise
        countries.get(country)
    except:
        raise "The country code is invalid"
    
    res = requests.get(f"https://stat.ripe.net/data/country-resource-list/data.json?resource={country}")
    if res.status_code != 200:
        raise
    
    payload = res.json()

    return payload['data']['resources']

def fetch_country_ip(country: str) -> list:
    resources = fetch_country(country)
    ip = resources['ipv4'] + resources['ipv6']
    return ip

def fetch_asn_holder(asn: int) -> str:
    res = requests.get(f"https://stat.ripe.net/data/as-overview/data.json?resource={asn}")
    if res.status_code != 200:
        raise

    payload = res.json()
    return payload['data']['holder']


def fetch_asn_neighbours(asn: int) -> list:
    res = requests.get(f"https://stat.ripe.net/data/asn-neighbours/data.json?resource={asn}")
    if res.status_code != 200:
        raise

    payload = res.json()

    return payload['data']['neighbours']