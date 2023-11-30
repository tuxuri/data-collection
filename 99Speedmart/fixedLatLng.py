import requests

def find_nearest_store(target_store, fixed_lat, fixed_lng):
    base_url = "https://nominatim.openstreetmap.org/search"
    query = target_store
    format_ = "json"
    address_details = 0  # Set to 1 if you want detailed address information

    # Construct the request URL
    url = f"{base_url}?q={query}&format={format_}&addressdetails={address_details}&limit=1"
    url += f"&lat={fixed_lat}&lon={fixed_lng}"  # Optionally provide the fixed coordinates

    print(url)
    # Make the API request
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if response.status_code == 200 and data:
        # Extract information about the first result (assuming it's the nearest)
        first_result = data[0]
        store_name = first_result['display_name']
        store_location = [float(first_result['lat']), float(first_result['lon'])]

        return store_name, store_location
    else:
        # If the request was not successful, print the error message
        print(f"Error: Unable to find {target_store}")

# Fixed latitude and longitude coordinates
fixed_latitude = 3.19774  # Example latitude (e.g., Kuala Lumpur)
fixed_longitude = 101.59918  # Example longitude (e.g., Kuala Lumpur)

# Target store name
target_store = "99 speedmart"

# Find the nearest store using OpenStreetMap
result = find_nearest_store(target_store, fixed_latitude, fixed_longitude)

# Print the result
if result:
    store_name, store_location = result
    print(f"Nearest {target_store} store: {store_name}")
    print(f"Location: {store_location}")
