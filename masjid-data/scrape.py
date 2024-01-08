#!/usr/bin/env python3

import csv
import json
import os
import re
import uuid

import requests
from bs4 import BeautifulSoup

ENDPOINT = "https://masjid.islam.gov.my/maklumatMasjidSurau?carian=&jenis=&negeri=&daerah=&masjidSurau=&page="
DOWNLOAD_DIR = r"masjid-data\downloads"
STORES = r"masjid-data\list_of_masjid_in_malaysia.csv"
HISTORY_CONFIG = r"masjid-data\history.json"

extract_page = re.compile(r"\d+")
extract_coordinates = re.compile(r"\d+.\d+,\d+.\d+")

fieldnames = [
"no","code","kategori","nama","alamat","negeri","daerah","no_tel","no_fax","tarikh_dibina","lat","long","sejarah","binaan","kemudahan","gambar",
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

    with open(STORES, mode='w', newline='',encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(last_page):
            if i<674:
                continue
            if i + 1 in [10, 38, 51, 59, 190, 197, 334, 445, 469, 483, 516, 517, 608, 613, 614, 615, 616, 640]:
                        print(f"Skipping page {i + 1}")
                        continue
            url = f"{ENDPOINT}{i+1}"
            data = extract_data(fetch(history, url),history)
            writer.writerows(data)
            # if data:
            #     break

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
    with open(os.path.join(DOWNLOAD_DIR, history[url]), mode='w', newline='',encoding="utf-8") as f:
        f.write(data)

    return data

def extract_additional_data(data):
    soup = BeautifulSoup(data, "html.parser")
    sejarah_heading = soup.find("h2", string="SEJARAH")
    binaan_heading = soup.find("h2", string="BINAAN")
    tarikh_dibina_label = soup.find("label", string="Tarikh Dibina")

    def extract_text_within_h6(element):
        if element:
            text = ""
            for h6_sibling in element.find_next_siblings(["h6", None], limit=5): 
                if h6_sibling.name == "h6" and h6_sibling.find_previous_sibling() == element:
                    text += str(h6_sibling.text).strip() + " "

            return text.strip()
    def extract_text_after_label(label_element):
        if label_element:
            h6_sibling = label_element.find_next("h6")
            return h6_sibling.text.strip() if h6_sibling else ""
        
    tarikh_dibina_text = extract_text_after_label(tarikh_dibina_label)

    sejarah_text = extract_text_within_h6(sejarah_heading)
    binaan_text = extract_text_within_h6(binaan_heading)
    
    return {
        "sejarah": sejarah_text,
        "binaan": binaan_text,
        "tarikh": tarikh_dibina_text,
    }
def extract_data(data,history):
    soup = BeautifulSoup(data, "html.parser")

    info_divs = soup.find_all("div", class_="pb-2")

    for info_div in info_divs:
        image_src = info_div.select_one("div.row.col-12 div.col-md-3 img")["src"] if info_div.select_one("div.row.col-12 div.col-md-3 img") else None
        name = info_div.select_one("div.row.col-12 div.btn h4")
        address = info_div.select_one("div.row.col-12 div.col-md-9 h6:nth-of-type(1)")
        state = info_div.select_one("div.row.col-12 div.col-md-9 h6:nth-of-type(3)")
        state_code_phone_fax = info_div.select("div.row.col-12 div.col-md-9 h6")[1:6]
        next_scraping_link = info_div.select_one("div.row.col-12 div.col-md-5 a")["href"] if info_div.select_one("div.row.col-12 div.col-md-5 a") else None


        if next_scraping_link:
            code = state_code_phone_fax[1].text.strip() if state_code_phone_fax[1] else "TIADA"
            next_link = f"https://masjid.islam.gov.my/maklumatDetailMS/1/{code}"
            if not code :
                continue
            else :
                next_data = fetch(history, next_scraping_link)
                additional_info = extract_additional_data(next_data)
                # print("latlng : ",additional_info )
                
                address = address.text.strip() if address else "TIADA"
                name = name.text.strip() if name else "TIADA"
                state = state_code_phone_fax[0].text.strip() if state_code_phone_fax[0] else "TIADA"
                phone = state_code_phone_fax[2].text.strip() if state_code_phone_fax[2] else "TIADA"
                fax = state_code_phone_fax[3].text.strip() if state_code_phone_fax[3] else "TIADA"
                

                yield {
                    "no":"",
                    "code":code,
                    "kategori":"",
                    "nama":name,
                    "alamat":address,
                    "negeri":state,
                    "daerah":"",
                    "no_tel":phone,
                    "no_fax":fax,
                    "tarikh_dibina":additional_info.get("tarikh", ""),
                    "lat":"",
                    "long":"",
                    "sejarah":additional_info.get("sejarah", ""),
                    "binaan":additional_info.get("binaan", ""),
                    "kemudahan":"",
                    "gambar":image_src,
            }
        else:
            print("Some information not found for this set.")


def get_last_page(data):
    # soup = BeautifulSoup(data:, "html.parser")
    # target = soup.select_one("li.PagedList-skipToLast > a")

    # if target is None:
    #     return None

    # num = extract_page.findall(target.attrs["href"])[0]
    num = 681
    return int(num)


if __name__ == "__main__":
    main()
