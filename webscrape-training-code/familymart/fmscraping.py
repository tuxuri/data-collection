import csv
import re

import requests
from data import data  

def get_nearest_facilities(latitude, longitude, access_token, types, limit=3):
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    coordinates = f"{longitude},{latitude}.json"
    endpoint = f"{base_url}{coordinates}"
    params = {
        "access_token": access_token,
        "types": types,  
        "limit": limit
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if response.status_code == 200:
        features = data.get("features", [])
        results = []
        count = 0   
        for feature in features:
            place_name = feature.get("place_name", "")
            
            if 'mix' not in place_name.lower():
                first_part = place_name.split(',')[0]
                results.append(first_part)
                count+=1
                print("placename ",count ," : " , place_name )
        if count < 2  :
            results.append("newplace")
        return results

    else:
        print(f"Error: {response.status_code}, {data.get('message', 'Unknown error')}")



with open('data_familymart.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    csv_writer.writerow(['feature_name','feature_tag','Name','Address', 'Latitude','Longitude','Location','Nearest(poi)'])
    x=0
    for item in data:
        content = item['content']

        name_start = content.find('<h5>') + 4
        name_end = content.find('<', name_start)
        name = content[name_start:name_end].strip()

        address_start = content.find('<p class="font10">') + 18
        address_end = content.find('</p>', address_start)
        full_address = content[address_start:address_end].replace('<br>', ' ').strip()

        # getlocation name


        # Check if the address contains "Selangor"
        if full_address:
        # if 'Selangor' in full_address:
            pattern = r'(?:.*?,){3}\s*([^,]+)$'
            match = re.search(pattern, full_address)

            if match:
                result = match.group()
                city = [part.strip() for part in result.split(',')]
                x = len(city) - 2

                # print(city[x-1])
            lat = item['position']['lat']
            lng = item['position']['lng']

            mapbox_access_token = "pk.eyJ1IjoicnllaSIsImEiOiJjbG52aHo5aWgwcGs3MnBucDBwd2Jud2VkIn0.yFjj-Nk5rVdbkGtIaBF84Q"
            facility_types = "poi,poi.landmark"  
            
            nearestpoi = get_nearest_facilities(lat, lng, mapbox_access_token, facility_types)

            state = city[len(city)-1]
            if ' ' in state :
                # print(state)
                newState = state.split()[-2]
                print(newState)
            

            csv_writer.writerow(["familymart","convenience_store",f"{name} @{city[x-1]}", full_address, f"{lat}",f"{lng}",city[x-1],nearestpoi])
            x=x+1
    print("Total: ",x)
