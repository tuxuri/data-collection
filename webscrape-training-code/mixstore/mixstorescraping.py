import csv
import re
import requests
from bs4 import BeautifulSoup

# a,b,c,d,e=0

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



def extract_coordinates_from_url(url):
    # global a, b, c, d, e 
    # print("url : ",url)
    match_format_1 = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+),\d+z', url)
    match_format_2 = re.search(r'place/[^@]+@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    # match_format_3 = re.search(r'goo\.gl/maps/[^/]+/(-?\d+\.\d+),(-?\d+\.\d+)', url)
    match_format_4 = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    # match_format_5 = re.search(r'/maps/[^/]+/(-?\d+\.\d+),(-?\d+\.\d+)', url)

    if match_format_1:
        latitude, longitude = match_format_1.groups()
        # a+=1
    elif match_format_2:
        latitude, longitude = match_format_2.groups()
        # b+=1
    # elif match_format_3:
    #     latitude, longitude = match_format_3.groups()
    #     c+=1
    elif match_format_4:
        latitude, longitude = match_format_4.groups()
        # d+=1
    # elif match_format_5:
    #     latitude, longitude = match_format_5.groups()
    #     e+=1
    else:
        latitude, longitude = None, None
        # latitude, longitude = "none"

    # print("position : ",latitude,longitude)
    return latitude, longitude

def storeDataToExcel(name, address, lat, lng, location, state, nearestpoi):
    # Store the data in a CSV file (open in append mode 'a')
    csv_file_path = "data_mixstore.csv"
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # If the file is empty, write the header
        if csv_file.tell() == 0:
            csv_writer.writerow(['feature_name', 'feature_tag', 'Name', 'Address', 'Latitude', 'Longitude', 'Location (CS)', 'State', 'Nearest(poi)'])

        # Write data
        csv_writer.writerow(["mixstore", "convenience_store", name, address, f"{lat}", f"{lng}", location, state, nearestpoi])

    print(f"Data has been successfully written to {csv_file_path}")

url = "https://mix.com.my/storelocation/"
response = requests.get(url)

if response.status_code == 200:
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    stores = []

    x=0

    # for h3 in soup.find_all('h3', class_='wp-block-heading'):
    #     city = h3.text.strip()
    store_info = {'Country': 'Malaysian'}
    
    for ul in soup.find_all('ul'):
        name, address, location, state,stateCopy,lat,lng = '', '', '', '','', '', '',
        for li in ul.find_all('li'):
            if(li.find('strong') ):
                # print("store tag : ",li)
                
                strong_tags = li.find_all('strong')
                
                # print("strong_tags :",strong_tags[0].text.strip())
                # print("address :",li.br.next_sibling.strip())

                name = strong_tags[0].text.strip()
                address = li.br.next_sibling.strip()
                # store_info['feature_name'] = "mixstore"
                # store_info['feature_tag'] = "convenience_store"
                location_store =  re.search(r'@ (.+)',name)
                if location_store:
                    location = location_store.group(1)
                x+=1
                # print(store_info['Location (CS)'])

                malaysian_states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
                "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu","Kuala Lumpur","Petaling Jaya"]

                for state in malaysian_states:
                    if state in address:
                        stateCopy= state
                        break

                print("Data ",x," : ","Name : ",strong_tags[0].text.strip())

            # Extract latitude and longitude from Google Maps link
            elif 'href' in li.find('a').attrs:
                # print("map tag : ",li)
                map_url_tag=li.find('a')
                if map_url_tag and 'href' in map_url_tag.attrs:
                    map_url = map_url_tag['href']
                    # print("map_url : ",map_url)
                    latitude, longitude = extract_coordinates_from_url(map_url)
                    if latitude and longitude and name:
                        lat = latitude
                        lng = longitude
                        # print("location : ", latitude,",",longitude)

                        # get nearest poi on fixed latlng
                        mapbox_access_token = "pk.eyJ1IjoicnllaSIsImEiOiJjbG52aHo5aWgwcGs3MnBucDBwd2Jud2VkIn0.yFjj-Nk5rVdbkGtIaBF84Q"
                        facility_types = "poi,poi.landmark"  

                        nearestpoi = get_nearest_facilities(latitude, longitude, mapbox_access_token, facility_types)

                        storeDataToExcel(name, address, lat, lng, location, stateCopy, nearestpoi)

                    elif name:
                        storeDataToExcel(name, address, "none", "none", location, stateCopy, "none")

                        # lat = "none"
                        # lng = "none"

        # storeDataToExcel(store_info['Name'], store_info['Address'], store_info['Latitude'], store_info['Longitude'],store_info['Location (CS)'], store_info['State'], store_info['Nearest(poi)'])
    # print(a,b,c,d,e)
    print("Total Data : ",x)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
