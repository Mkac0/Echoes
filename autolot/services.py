import requests
from django.conf import settings

AUTO_DEV_API_KEY = settings.AUTO_DEV_API_KEY
BASE_API = "https://api.auto.dev"

def fetch_vehicle_by_vin(vin):
    """Fetch basic vehicle info (make, model, year, etc.)"""
    headers = {"Authorization": f"Bearer {settings.AUTO_DEV_API_KEY}"}
    response = requests.get(f"{BASE_API}/vin/{vin}", headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_retail_photo_urls_by_vin(vin):
    """Fetch retail photo URLs for a VIN"""
    headers = {"Authorization": f"Bearer {settings.AUTO_DEV_API_KEY}"}
    response = requests.get(f"{BASE_API}/photos/{vin}", headers=headers)
    response.raise_for_status()
    data = response.json()
    return (data.get('data') or {}).get('retail', [])
