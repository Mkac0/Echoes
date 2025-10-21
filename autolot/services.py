import requests
from django.conf import settings

AUTO_DEV_API_KEY = settings.AUTO_DEV_API_KEY
BASE_URL = "https://api.auto.dev"

def fetch_vehicle_by_vin(vin):
    headers = {"Authorization": f"Bearer {settings.AUTO_DEV_API_KEY}"}
    params = {"vin": vin}
    response = requests.get(f"{BASE_URL}/vin-decode", headers=headers, params=params)
    response.raise_for_status()
    return response.json()
