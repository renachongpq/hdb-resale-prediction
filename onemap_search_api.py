import requests
from urllib.parse import urlencode
import pandas as pd
import re
from tqdm import tqdm
from fuzzywuzzy import fuzz

"""
use OneMap search API to get the location details of all MRT and LRT stations
"""

def read_stations(file):
    stations = []
    with open(file, "r") as f:
        result = [line.strip() for line in f.readlines()]
        stations.extend(result[1:]) # remove name header
    stations = set(stations)
    return stations

def search_stations(stations):
    base_url = "https://www.onemap.gov.sg/api/common/elastic/search?"
    results = []
    for s in stations:
        search_para = {"searchVal": s, "returnGeom": "Y", "getAddrDetails" : "Y"}
        url = base_url + urlencode(search_para)
        response = requests.request("GET", url)
        data = response.json()
        for d in data["results"]:
            if re.search(".*\(.*\)", d["SEARCHVAL"]):
                results.append(d)
                break
    return pd.DataFrame(results)

def get_station_details(mrt_dir, lrt_dir):
    mrt_stations = read_stations(mrt_dir)
    mrt_stations = [x.strip() + " MRT" for x in mrt_stations]
    lrt_stations = read_stations(lrt_dir)
    lrt_stations.remove("Teck Lee")
    lrt_stations = [x.strip() + " LRT" for x in lrt_stations]

    mrt_details = search_stations(mrt_stations)
    lrt_details = search_stations(lrt_stations)
    station_details = pd.concat([mrt_details, lrt_details], axis=0)
    station_details.to_csv("data/station_info.csv", index=False)

# -------------- main code to get mrt & lrt station details --------------
mrt_names = "data/mrt_stations.txt"
lrt_names = "data/lrt_stations.txt"
# get_station_details(mrt_names, lrt_names)
# ------------------------------------------------------------------------

def format_address(address):
    if re.search(" NTH ", address):
        address = re.sub(" NTH ", " NORTH ", address)
    elif re.search(" STH ", address):
        address = re.sub(" STH ", " SOUTH ", address)
    if re.search(" DR ", address):
        address = re.sub(" DR ", " DRIVE ", address)
    elif re.search(" DR", address):
        address = re.sub(" DR", " DRIVE", address)
    elif re.search(" PL ", address):
        address = re.sub(" PL ", " PLACE ", address)
    elif re.search(" ST ", address):
        address = re.sub(" ST ", " STREET ", address)
    elif re.search(" AVE", address):
        address = re.sub(" AVE", " AVENUE", address)
    elif re.search(" RD", address):
        address = re.sub(" RD", " ROAD", address)
    if re.search(" CTRL", address):
        address = re.sub(" CTRL", " CENTRAL", address)
    elif re.search(" CTR", address):
        address = re.sub(" CTR", " CENTER", address)
    if re.search(" C\'WEALTH ", address):
        address = re.sub(" C\'WEALTH ", " COMMONWEALTH ", address)
    elif re.search(" GDNS ", address):
        address = re.sub(" GDNS ", " GARDENS ", address)
    elif re.search(" BT ", address):
        address = re.sub(" BT ", " BUKIT ", address)
    elif re.search(" LOR ", address):
        address = re.sub(" LOR ", " LORONG ", address)
    elif re.search(" UPP ", address):
        address = re.sub(" UPP ", " UPPER ", address)
    return address

def search_hdb(address_list):
    base_url = "https://www.onemap.gov.sg/api/common/elastic/search?"
    results = {}
    error_list = []
    unique_address = set(address_list)
    for address in tqdm(unique_address):
        address = format_address(address)
        search_para = {"searchVal": address, "returnGeom": "N", "getAddrDetails" : "Y"}
        url = base_url + urlencode(search_para)
        response = requests.request("GET", url)
        data = response.json()
        if len(data["results"]) > 1:
            max_ratio = 0
            keep = {}
            for d in data["results"]:
                match_ratio = fuzz.ratio(address, d["SEARCHVAL"])
                if match_ratio > max_ratio:
                    max_ratio = match_ratio
                    keep = d
            results[address] = keep
        elif len(data["results"]) < 1:
            error_list.append(address)
            # print(address)
            # print(results)
            # raise
        else:
            results[address] = data["results"][0]
    return results, error_list

def match_hdb_lat_long(address_list, flat_details):
    results = []
    for address in tqdm(address_list):
        results.append(flat_details[address])
    return pd.DataFrame(results)

# -------------- main code to get hdb flat location details --------------
df = pd.read_csv("data/resale-flat-prices-2000-present.csv")
address_list = df["address"].values.tolist()
# print(set(address_list))
flat_details, error_address = search_hdb(address_list)
print(flat_details)
print(error_address)
# matched_details = match_hdb_lat_long(address_list, flat_details)
# hdb_data = pd.concat([df, matched_details["SEARCHVAL", "LATITUDE", "LONGITUDE"]], axis=1)
# hdb_data.to_csv("hdb-resale-price-with-lat-long-2000-present.csv", index=False)
# ------------------------------------------------------------------------