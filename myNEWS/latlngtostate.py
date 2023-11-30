import csv

import requests

def get_nearest_facilities(latitude, longitude, access_token, types, limit=1):
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
            
            # if '99' not in place_name.lower():
            malaysian_states = ["Johor", "Kedah", "Kelantan", "Melaka", "Negeri Sembilan",
                    "Pahang", "Perak", "Perlis", "Pulau Pinang", "Sabah", "Sarawak", "Selangor", "Terengganu","Labuan","Putrajaya","Kuala Lumpur", "Pen"]

            for state in malaysian_states:
                if state.lower() in place_name.lower():
                    print(f"The state '{state}' is present in the given address.")
                    results.append(state)
                    break
            if not results :
                results.append("none")
            
            count+=1
            print("placename ",count ," : " , place_name )

            output_file_path = r'myNews/dataStates.csv'
            # Append data to the existing CSV file
            with open(output_file_path, 'a', newline='') as output_file:
                # Create a CSV writer object
                csv_writer = csv.writer(output_file)

                # Write the data to the CSV file
                csv_writer.writerow([latitude, longitude, ','.join(results)])

        return results

    else:
        print(f"Error: {response.status_code}, {data.get('message', 'Unknown error')}")

def read_csv(file_path):

    coordinates = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it contains column names

        for row in reader:
            try:
                # Try to convert the values to float
                lat, lon = map(float, row)
                coordinates.append((lat, lon))
            except ValueError:
                coordinates.append(("none", "none"))
    return coordinates

# Example usage
file_path = r'myNews/datalatlng.csv'

coordinates = read_csv(file_path)

for lat, lon in coordinates:

    mapbox_access_token = "pk.eyJ1IjoicnllaSIsImEiOiJjbG52aHo5aWgwcGs3MnBucDBwd2Jud2VkIn0.yFjj-Nk5rVdbkGtIaBF84Q"
    facility_types = "poi,poi.landmark"  
    nearestPoi = get_nearest_facilities(lat, lon, mapbox_access_token, facility_types)
    
    print(f'Latitude: {lat}, Longitude: {lon}')

