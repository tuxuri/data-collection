import requests

def get_nearest_facilities(latitude, longitude, access_token, types, limit=9999):
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    coordinates = f"{longitude},{latitude}.json"
    endpoint = f"{base_url}{coordinates}"
    params = {
        "access_token": access_token,
        "types": types,
        "limit": limit,
    }

    response = requests.get(endpoint, params=params)
    data = response.json()
    if response.status_code == 200:
        features = data.get("features", [])
        count = 0
        for index, feature in enumerate(features):
            place_name = feature.get("place_name", "")
            properties = feature.get("properties", "")
            category = properties.get("category", "")
            print(place_name)
            
            if ("shop" in category.lower() or
                "facility" in category.lower() or
                "track" in category.lower() or
                "hospital" in category.lower() or
                "restaurant" in category.lower() or
                "entertainment" in category.lower() or
                "pharmacy" in category.lower() or
                "clinic" in category.lower()) and count != 3:

                
                print(f"{index + 1}. {place_name}")
                count += 1

            if count == 3:
                break

    else:
        print(f"Error: {response.status_code}, {data.get('message', 'Unknown error')}")

# Example usage
latitude = 2.815001
longitude = 101.503224
mapbox_access_token = "pk.eyJ1IjoicnllaSIsImEiOiJjbG52aHo5aWgwcGs3MnBucDBwd2Jud2VkIn0.yFjj-Nk5rVdbkGtIaBF84Q"
facility_types = "poi" 

get_nearest_facilities(latitude, longitude, mapbox_access_token, facility_types)
