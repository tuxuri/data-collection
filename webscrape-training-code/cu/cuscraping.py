import requests
import csv

url = "https://nicetocu.com.my/wp-admin/admin-ajax.php?action=asl_load_stores&lang=&nonce=3c71404c7d&load_all=1&layout=1"

# Bypass: add headers to mimic a legitimate user
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    json_data = response.json()
    
    # Open a CSV file for writing
    with open('data_cu.csv', mode='w', newline='') as csv_file:
        fieldnames = ['feature_name','Name', 'Address', 'Latitude', 'Longitude']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        x = 0
        for location in json_data:
            title = location['title']
            street = location['street']
            city = location['city']
            state = location['state']
            postal_code = location['postal_code']
            lat = location['lat']
            lng = location['lng']

            title=title.replace('CU ','CU@')

            full_address = f"{street}, {postal_code} {city}, {state}"
            # if state.lower() == "selangor":
            writer.writerow({'feature_name': "CU",'Name': title,'Address': full_address, 'Latitude': lat, 'Longitude': lng})
            x += 1

        print("Total: ", x)
        print("Data has been written to data_cu.csv")

else:
    print("Failed to retrieve data. Status code:", response.status_code)
