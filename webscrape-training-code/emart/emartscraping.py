import requests
from bs4 import BeautifulSoup

url = "https://emart24.com.my/locations/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    
    store_elements = soup.select('your_selector')

    for store_element in store_elements:
        store_name = store_element.find('h2').text.strip()
        store_address = store_element.find('p', class_='address').text.strip()
        store_city = store_element.find('p', class_='city').text.strip()

        print(f"Store Name: {store_name}")
        print(f"Address: {store_address}")
        print(f"City: {store_city}")
        print("\n")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
