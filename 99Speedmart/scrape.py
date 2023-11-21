#!/usr/bin/env python3

import csv
import json
import os
import re
import uuid

import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://www.99speedmart.com.my/Store"
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

    with open("stores.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(last_page):
            url = f"{ENDPOINT}?page={i+1}"

            data = extract_data(fetch(history, url))
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
    with open(os.path.join(DOWNLOAD_DIR, history[url]), "w") as f:
        f.write(data)

    return data


def extract_data(data):
    soup = BeautifulSoup(data, "html.parser")
    rows = soup.select("tr")

    for row in rows[1:]:
        name, address, link_holder = row.select("td")

        lat = None
        lng = None

        link = link_holder.select_one("a")
        if link and "href" in link.attrs:
            extracted = extract_coordinates.findall(link.attrs["href"])
            if extracted and len(extracted) > 0:
                lat, lng = extracted[0].split(",")
                lat = float(lat)
                lng = float(lng)

        yield {
            "feature_name": "99 Speedmart",
            "feature_tag": "convenience_store",
            "Name": name.text.strip(),
            "Address": address.text.strip(),
            "Latitude": lat,
            "Longitude": lng,
        }


def get_last_page(data):
    soup = BeautifulSoup(data, "html.parser")
    target = soup.select_one("li.PagedList-skipToLast > a")

    if target is None:
        return None

    num = extract_page.findall(target.attrs["href"])[0]
    return int(num)


if __name__ == "__main__":
    main()
