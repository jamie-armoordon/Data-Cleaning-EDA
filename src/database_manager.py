import requests

base_url = "https://ghoapi.azureedge.net/api"

response = requests.get(f"{base_url}/Indicator")

if response.status_code == 200:
    data = response.json()
    for indicator in data['value']:
        if any(term in indicator['IndicatorName'].lower() for term in ['covid', 'coronavirus', 'sars-cov-2']):
            print(f"Indicator: {indicator['IndicatorName']}, Code: {indicator['IndicatorCode']}")
else:
    print(f"Error: {response.status_code}")