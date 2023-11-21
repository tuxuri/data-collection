import csv
import requests
import re
from bs4 import BeautifulSoup


def get_nearest_facilities(latitude, longitude, access_token, types, limit=3):
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    coordinates = f"{longitude},{latitude}.json"
    endpoint = f"{base_url}{coordinates}"
    params = {
        "access_token": access_token,
        "types": types,  # specify the types you are interested in (e.g., hospital, restaurant, poi, school)
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
            
            if '99' not in place_name.lower():
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
    match_format_1 = re.search(r'q=([-+]?\d*\.\d+),\s*([-+]?\d*\.\d+)', url)
    match_format_2 = re.search(r'q=([NEWS\d.,]+),\s*([NEWS\d.,]+)', url)
    # match_format_3 = re.search(r'@(\d+)°(\d+)\'([\d.]+)\"([NS]+)\+(\d+)°(\d+)\'([\d.]+)\"([EW]+)', url)
    # match_format_4 = re.search(r'place/([-+]?\d*\.\d+)°(\d+\.\d+)\'(\d+\.\d+)\"([NS])\+([-+]?\d*\.\d+)°(\d+\.\d+)\'(\d+\.\d+)\"([EW])', url)
    match_format_5 = re.search(r'@([-+]?\d+\.\d+),([-+]?\d+\.\d+),(\d+)z', url)

    # Debuging
    # print("url location : ", url)
    # print("regex result 1: ", match_format_1)
    # print("regex result 2: ", match_format_2)
    # print("regex result 3: ", match_format_3)
    # print("regex result 4: ", match_format_4)
    # print("regex result 5: ", match_format_5) 

    if match_format_1:
        latitude, longitude = match_format_1.groups()
        # print("p1")
    elif match_format_2:
        # print("p2")
        coordinates = match_format_2.groups()
        latitude, longitude = coordinates[0].replace('N', '').replace('E', ''), coordinates[1].replace('N', '').replace('E', '')
    # elif match_format_3:
    #     print("p3")
    #     # Extract latitude and longitude from the query parameters
    #     parsed_url = urlparse(url)
    #     query_params = parse_qs(parsed_url.query)

    #     latitude = float(query_params['q'][0].split(',')[0])
    #     longitude = float(query_params['q'][0].split(',')[1])
    # elif match_format_4:
    #     print("p4")
    #     lat_deg, lat_min, lat_sec, lat_dir, lon_deg, lon_min, lon_sec, lon_dir = match_format_4.groups()

    #     # Convert to decimal degrees
    #     latitude = float(lat_deg) + float(lat_min)/60 + float(lat_sec)/3600
    #     longitude = float(lon_deg) + float(lon_min)/60 + float(lon_sec)/3600

    #     # Adjust for direction (N/S/E/W)
    #     if lat_dir == 'S':
    #         latitude *= -1
    #     if lon_dir == 'W':
    #         longitude *= -1
    elif match_format_5:
        # print("p5")
        lat, lon, _ = match_format_5.groups()

        # Convert the  match_format_5 to this format "3°04'36.3"N 101°28'40.0"E"
        latitude, longitude = convert_to_dms(lat, lon)

    else:
        latitude, longitude = None, None

    return latitude, longitude


def convert_to_dms(latitude, longitude):
    def dd_to_dms(degrees):
        d = int(degrees)
        m = int((degrees - d) * 60)
        s = (degrees - d - m / 60) * 3600
        return d, m, s

    lat_deg, lat_min, lat_sec = dd_to_dms(float(latitude))
    lon_deg, lon_min, lon_sec = dd_to_dms(float(longitude))

    return f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"N", f"{lon_deg}°{lon_min}'{lon_sec:.1f}\"E"



# Store data to cvs file
csv_file_path = 'data_99speedmart.csv'

# Open csv file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row to the CSV file
    csv_writer.writerow(['feature_name','feature_tag', 'name', 'Address', 'Latitude', 'Longitude', 'Location','Nearest(poi)'])

    base_url = "https://www.99speedmart.com.my/Store"
    current_page = 1
    x=0
    while True:
        url = f"{base_url}?page={current_page}&Statename=1"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table
            table = soup.find('table', class_='table sp-logo')

            # Get all data from each row
            rows = table.find_all('tr')[1:]

            for row in rows:
                columns = row.find_all('td')

                store_name_original = columns[0].text.strip()
                store_name = re.sub(r'^\d+ - ', '', store_name_original)

                full_address = columns[1].text.strip()
                map_url_tag = columns[2].find('a')

                if map_url_tag and 'href' in map_url_tag.attrs:
                    # Get the url
                    map_url = map_url_tag['href']

                    latitude, longitude = extract_coordinates_from_url(map_url)

                    if latitude and longitude != "None":
                        if "03." in latitude or "02." in latitude:
                            latitude = latitude.replace('03.', '3.').replace('02.','2.')

                        if "selangor" in full_address.lower() and "E" not in latitude and "N" not in latitude:
                            # print("Store Name: 99SpeedMart@", store_name)
                            # print("Full Address:", full_address)
                            # print("Latitude:", latitude)
                            # print("Longitude:", longitude)
                            # print("-----")
                            location = store_name
                            x+=1

                            mapbox_access_token = "pk.eyJ1IjoicnllaSIsImEiOiJjbG52aHo5aWgwcGs3MnBucDBwd2Jud2VkIn0.yFjj-Nk5rVdbkGtIaBF84Q"
                            facility_types = "poi,poi.landmark"  

                            nearestPoi = get_nearest_facilities(latitude, longitude, mapbox_access_token, facility_types)


                            csv_writer.writerow(["99speedmart","convenience_store","99SpeedMart @"+store_name, full_address, latitude, longitude, location,nearestPoi]) 
                            print("Total Data : ",x)
            # Find the next page link
            next_page_link = soup.find('li', class_='PagedList-skipToNext')
            if next_page_link:
                current_page += 1
            else:
                break

        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            break

print(f"Data has been successfully saved to {csv_file_path}.")
# print(f"Total Data : ",x)
