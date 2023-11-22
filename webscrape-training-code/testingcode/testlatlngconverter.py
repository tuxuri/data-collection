import requests
from urllib.parse import urlparse

def get_latlng_from_google_maps_url(google_maps_url):
    expanded_url = requests.head(google_maps_url, allow_redirects=True).url
    print("1 ", expanded_url)

    parsed_url = urlparse(expanded_url)
    print("2 ", parsed_url)

    path_segments = parsed_url.path.split('/')
    print("3 ", path_segments)

    latlng_segment = path_segments[-2]
    print("4 ", latlng_segment)

    latlng_values = latlng_segment.split(',')

    latitude = float(latlng_values[0][1:])
    longitude = float(latlng_values[1])

    return latitude, longitude

# Example usage with the provided Google Maps link
google_maps_url = "https://goo.gl/maps/BwjmmM9N8FqHLGn28"
lat,lng = get_latlng_from_google_maps_url(google_maps_url)

print("Latitude and Longitude:", lat,",",lng)
