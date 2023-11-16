#!/bin/bash
wget https://www.mynews.com.my/data/store-locations.json
jq . store-locations.json > stores.json