#!/usr/bin/env python3

import csv
import json
import os
import re
import uuid

import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://www.giant.com.my/store_location/"
DOWNLOAD_DIR = "downloads"
STORES = "stores.csv"
HISTORY_CONFIG = "history.json"

extract_page = re.compile(r"\d+")
extract_coordinates = re.compile(r"\d+.\d+,\d+.\d+")

fieldnames = [
    "feature_name",
    "feature_tag",
    "Name",
    "Address",
    "Latitude",
    "Longitude",
]


def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    history = {}
    if os.path.exists(HISTORY_CONFIG):
        with open(HISTORY_CONFIG) as f:
            history = json.load(f)

    last_page = get_last_page(fetch(history, ENDPOINT))
    if not last_page:
        print("Failed to get last page")
        return

    with open(STORES, mode='w', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        print(last_page)

        for i in range(1, last_page + 1):
            url = f"{ENDPOINT}/page/{i}/"

            data = list(extract_data(fetch(history, url)))
            # print(f"Extracted data from {url}: {data}")
            writer.writerows(data)

    with open(HISTORY_CONFIG, "w") as f:
        json.dump(history, f, sort_keys=True, indent=4)


def fetch(history, url):
    if url in history:
        with open(os.path.join(DOWNLOAD_DIR, history[url]), "r") as f:
            return f.read()

    print(f"Fetching {url}...")
    resp = requests.get(url)
    resp.raise_for_status()

    history[url] = uuid.uuid4().hex

    data = resp.text
    with open(os.path.join(DOWNLOAD_DIR, history[url]), mode='w', newline='', encoding="utf-8") as f:
        f.write(data)

    return data


def extract_data(data):
    soup = BeautifulSoup(data, "html.parser")

    title_wrappers = soup.find_all("div", class_="title-wrapper")
    for title_wrapper in title_wrappers:
        name_element = title_wrapper.find("h4", class_="woodmart-title-container")
        address_element = title_wrapper.find("div", class_="title-after_title")

        if name_element and address_element:
            name = name_element.text.strip()
            address = name + ", "+address_element.text.strip()

            yield {
                "feature_name": "giant",
                "feature_tag": "convenience_store",
                "Name": name,
                "Address": address,
                "Latitude": None,  
                "Longitude": None,  
            }



def get_last_page(data):
    soup = BeautifulSoup(data, "html.parser")
    pagination_div = soup.find("div", class_="dce-pagination")

    if pagination_div:
        last_page_element = pagination_div.find_all("a", class_="inactive")[-1]
        last_page_url = last_page_element.get("href")
        
        if last_page_url:
            num = extract_page.findall(last_page_url)
            return int(num[0]) if num else None

    return None


if __name__ == "__main__":
    main()
