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

google_maps_url = "https://www.google.com/maps/place/5%C2%B036'37.4%22N+100%C2%B030'52.4%22E/@5.6103953,100.5119797,17z/data=!3m1!4b1!4m4!3m3!8m2!3d5.61039!4d100.51456?entry=ttu"
lat,lng = get_latlng_from_google_maps_url(google_maps_url)

print("Latitude and Longitude:", lat,",",lng)
