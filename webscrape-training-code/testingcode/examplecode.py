import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com'
response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')

    for i in range(len(quotes)):
        print(f"Quote: {quotes[i].text}")
        print(f"Author: {authors[i].text}\n")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
