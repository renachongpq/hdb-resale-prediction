import requests
from urllib.parse import urlencode
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
from fuzzywuzzy import fuzz

"""
use OneMap search API to get the location details of all MRT and LRT stations
"""

def search_stations(stations):
    base_url = "https://www.onemap.gov.sg/api/common/elastic/search?"
    results = []
    for s in stations:
        search_para = {"searchVal": s, "returnGeom": "Y", "getAddrDetails" : "Y"}
        url = base_url + urlencode(search_para)
        response = requests.request("GET", url)
        data = response.json()
        keep = ""
        max_ratio = 0
        for d in data["results"]:
            if re.search(".*\(.*\)", d["SEARCHVAL"]):
                match_ratio = fuzz.ratio(s, d["SEARCHVAL"])
                if match_ratio > max_ratio:
                    max_ratio = match_ratio
                    keep = d
        results.append(keep)
    return pd.DataFrame(results)

def get_station_details(mrt_dir):
    df = pd.read_csv(mrt_dir)
    mrt_stations = df["Station name"].values.tolist()
    mrt_stations = [x.strip() + " MRT Station" for x in mrt_stations]

    mrt_details = search_stations(mrt_stations)
    mrt_details = mrt_details[["SEARCHVAL", "LATITUDE", "LONGITUDE"]]
    station_details = pd.concat([df, mrt_details], axis=1)
    station_details.rename(columns={"SEARCHVAL": "search_val", "LATITUDE": "latitude", "LONGITUDE": "longitude", 
                                    "Alpha-numeric code(s)": "code" , "Station name": "station_name", "Opening": "opening_date"}, inplace=True)
    station_details.to_csv("data/station_info.csv", index=False)

# -------------- main code to get mrt & lrt station details --------------
mrt_names = "data/mrt_station_opening.csv"
# get_station_details(mrt_names)
# ------------------------------------------------------------------------


"""
use OneMap search API to get the location details of HDB Resale Flats
"""

def format_address(address):
    if re.search(" NTH ", address):
        address = re.sub(" NTH ", " NORTH ", address)
    elif re.search(" STH ", address):
        address = re.sub(" STH ", " SOUTH ", address)
    if re.search(" DR ", address):
        address = re.sub(" DR ", " DRIVE ", address)
    # elif re.search(" DR", address):
    #     address = re.sub(" DR", " DRIVE", address)
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
    elif re.search(" JLN ", address):
        address = re.sub(" JLN ", " JALAN ", address)
    elif re.search(" KG ", address):
        address = re.sub(" KG ", " KAMPONG ", address)
    elif re.search(" CL$", address):
        address = re.sub(" CL$", " CLOSE", address)
    return address

# check if hdb address exist, if does not likely to be en-bloc flat
def search_hdb(address_list):
    base_url = "https://www.onemap.gov.sg/api/common/elastic/search?"
    results = {}
    error_list = []
    unique_address = set(address_list)
    for address in tqdm(unique_address):
        clean_address = format_address(address)
        search_para = {"searchVal": clean_address, "returnGeom": "Y", "getAddrDetails" : "Y"}
        url = base_url + urlencode(search_para)
        response = requests.request("GET", url)
        data = response.json()
        if len(data["results"]) > 1:
            max_ratio = 0
            keep = {}
            for d in data["results"]:
                match_ratio = fuzz.ratio(clean_address, d["SEARCHVAL"])
                if match_ratio > max_ratio:
                    max_ratio = match_ratio
                    keep = d
            results[address] = keep
        elif len(data["results"]) < 1:
            error_list.append(address)
        else:
            results[address] = data["results"][0]
    return results, error_list

def match_hdb_lat_long(address_list, flat_details, error_address, df):
    results = []
    for address in tqdm(address_list):
        if address in error_address:
            results.append({})
        else:
            results.append(flat_details[address])
    matched_results = pd.DataFrame(results)
    matched_results = matched_results[["LATITUDE", "LONGITUDE"]]
    matched_results.rename(columns={"LATITUDE": "latitude", "LONGITUDE": "longitude"}, inplace=True)
    hdb_matched = pd.concat([df, matched_results], axis=1)
    return hdb_matched

def check_accuracy(flat_details):
    count = 0
    for k, v in flat_details.items():
        if v["BLK_NO"] in k:
            count += 1
    return count

def get_valid_hdb_details(hdb_dir):
    df = pd.read_csv(hdb_dir)
    address_list = df["address"].values.tolist()
    flat_details, error_address = search_hdb(address_list)
    # print(len(flat_details))
    # print(check_accuracy(flat_details))
    hdb_new = match_hdb_lat_long(address_list, flat_details, error_address, df)
    hdb_new.dropna(axis=0, inplace=True)
    hdb_new.to_csv("data/hdb-resale-price-with-lat-long-2000-present.csv", index=False)

# -------------- main code to get hdb flat location details --------------
hdb_data = "data/resale-flat-prices-2000-present.csv"
get_valid_hdb_details(hdb_data)
# match_error = {'1 JLN PASAR BARU', '1 SELETAR WEST FARMWAY 6', '10 GHIM MOH RD', '10 TEBAN GDNS RD', '10 UPP BOON KENG RD', '10 YUNG KUANG RD', '11 REDHILL CL', 
#                '110 BT MERAH VIEW', '111 BT MERAH VIEW', '113 BT MERAH VIEW', '114 BT MERAH VIEW', '12 REDHILL CL', '167 BOON LAY DR', '168 BOON LAY DR', '169 BOON LAY DR', 
#                '170 BOON LAY DR', '171 BOON LAY DR', '172 BOON LAY DR', '172 STIRLING RD', '173 STIRLING RD', '18 KG BAHRU HILL', '19 KG BAHRU HILL', '1A WOODLANDS CTR RD', 
#                '2 SELETAR WEST FARMWAY 6', '20 UPP BOON KENG RD', '22 KG BAHRU HILL', '220 BOON LAY AVE', '23 KG BAHRU HILL', '24 KG BAHRU HILL', '247 ANG MO KIO AVE 3', 
#                '248 ANG MO KIO AVE 2', '252 ANG MO KIO AVE 4', "27A C'WEALTH AVE", '29 HAVELOCK RD', '2A WOODLANDS CTR RD', '3 ROCHOR RD', '3 TEBAN GDNS RD', '30 LOR 5 TOA PAYOH', 
#                '31 DOVER RD', '31 TAMAN HO SWEE', '313 CLEMENTI AVE 4', '314 CLEMENTI AVE 4', '33 TAMAN HO SWEE', '35 DOVER RD', '36 DOVER RD', '38 DOVER RD', "39A C'WEALTH AVE", 
#                '4 ROCHOR RD', '401 CLEMENTI AVE 1', '402 CLEMENTI AVE 1', '403 CLEMENTI AVE 1', '407 CLEMENTI AVE 1', '409 CLEMENTI AVE 1', '5 SELETAR WEST FARMWAY 6', 
#                '5 TEBAN GDNS RD', '5 YUNG PING RD', '51 TANGLIN HALT RD', '52 TANGLIN HALT RD', '53 TANGLIN HALT RD', '54 SIMS DR', '54 TANGLIN HALT RD', '59 SIMS DR', 
#                '6 SELETAR WEST FARMWAY 6', '6 TEBAN GDNS RD', '6 UPP BOON KENG RD', '6 YUNG PING RD', '62 SIMS DR', '7 SELETAR WEST FARMWAY 6', '7 TEBAN GDNS RD', '7 YUNG KUANG RD', 
#                "74 C'WEALTH DR", "75 C'WEALTH DR", "76 C'WEALTH DR", "77 C'WEALTH DR", "78 C'WEALTH DR", "79 C'WEALTH DR", '8 YUNG KUANG RD', "80 C'WEALTH DR", '83 BEDOK NTH RD', 
#                '88 ZION RD', '89 ZION RD', '90 ZION RD', '91 ZION RD', '96 MARGARET DR'}
# ------------------------------------------------------------------------