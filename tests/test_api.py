#!/usr/bin/env python
import json
import requests

url = 'http://127.0.0.1:5000/api/indicator'
headers = {'Content-Type': 'application/json'}

regional_indicator = {
    "id": 1,
    "nuts_region_id": "UKMW3",
    "nuts_region_level": "NUTS1",
    "indicator_type": "GVA",
    "indicator_value": 1
}

response = requests.post(url, json=json.dumps(regional_indicator), headers=headers)
assert response.status_code == 201
print(response.json())