import requests
import json
import sys

# data = ["Namet Fıstıklı Macar Salam 100 gr", "Türkiye Tarım Kredi Koop.Yeşil Mercimek 1 kg",
#  'Carrefour Badem İçi 150 gr', "Dr.Oetker Hamur Kabartma Tozu 15'li 150 gr"]
data =['HBV00000NE0QI', "HBV00000JUHBA", 'HBV00000NFGQQ', 'ZYHPDROETYRD010']

json_string = json.dumps(data)
res = requests.get('http://localhost:5000/recommendations', json=json_string)
if res.ok:
    print (res.json())