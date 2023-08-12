import requests
from urllib.parse import urlencode
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from tqdm import tqdm, trange
from onemap_access_token import access_token
      
def calculate_approx_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) # convert to radians

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371.0 * 1000 # approximate radius of earth in m
    return c * r

# def get_nearest_stations(transaction, mrt_info):
#     opened_stations = mrt_info[(transaction["month"] > mrt_info["opening_date"])] # opened stations before transaction
#     opened_stations.drop_duplicates(subset="station_name", inplace=True) # drop duplicate stations
#     lat1 = transaction["latitude"]
#     lon1 = transaction["longitude"]
#     opened_stations["walk_dist"] = opened_stations.apply(lambda row: calculate_approx_distance(lat1, lon1, row["latitude"], row["longitude"]), axis=1)
#     sorted_dist = opened_stations.sort_values(by="walk_dist", ascending=True)
#     return sorted_dist.iloc[:3]

def get_nearest_stations(hdb_data, mrt_info):
    address_df = hdb_data[["address", "latitude", "longitude"]].drop_duplicates()
    result = []
    for i in trange(address_df.shape[0]):
        address = address_df.iloc[i]
        lat1 = address["latitude"]
        lon1 = address["longitude"]
        temp = mrt_info
        temp["walk_dist"] = temp.apply(lambda row: calculate_approx_distance(lat1, lon1, row["latitude"], row["longitude"]), axis=1)
        sorted_dist = temp.sort_values(by="walk_dist", ascending=True)
        result.append(sorted_dist.to_dict("records"))
    return result

def get_walk_route(start_lat, start_long, end_lat, end_long, headers):
    base_url = "https://www.onemap.gov.sg/api/public/routingsvc/route?"
    search_para = {"start": start_lat + "," + start_long, "end": end_lat + "," + end_long , "routeType" : "walk"}
    url = base_url + urlencode(search_para)
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    data = response.json()
    print(data)
    return data["route_summary"]["total_time"], data["route_summary"]["total_distance"]

def get_shortest_mrt_walk_dist(hdb_dir, mrt_dir):
    hdb_data = pd.read_csv(hdb_dir)
    mrt_data = pd.read_csv(mrt_dir)
    mrt_data["opening_date"] = pd.to_datetime(mrt_data["opening_date"]).dt.to_period("M")
    hdb_data["month"] = pd.to_datetime(hdb_data["month"], format="%Y-%m").dt.to_period("M")

    # get the 3 neareast stations for routing
    for i in range(tqdm(hdb_data.shape[0])):
        row = hdb_data.iloc[i]
        nearest_stations = get_nearest_stations(row, mrt_data)
        nearest_stations[["walk_dist", "walk_time"]] = nearest_stations.apply(lambda mrt: get_walk_route(row["latitude"], row["longtitude"], mrt["latitude"], mrt["longtitude"]), axis=1, result_type="expand")
        nearest_stations.sort_values(by="walk_dist", ascending=True, inplace=True)



headers = {"Authorization": access_token}
hdb_dir = "data/hdb-resale-price-with-lat-long-2000-present.csv"
mrt_dir = "data/station_info.csv"
