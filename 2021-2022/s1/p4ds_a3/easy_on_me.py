import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np


geolocator=Nominatim(user_agent="app")


def main():
    data_table = pd.read_csv("zomato.csv")
    print(data_table["address"])


def drop_address_data(df):
    new_df = df.drop(columns=["address"])
    return new_df


def drop_menu_related_data(df):
    new_df = df.drop(columns=['dish_liked', 'cuisines', 'menu_item'])
    return new_df


def drop_irrelevant_data(df):
    new_df = df.drop(columns=['url', 'phone', 'reviews_list'])
    return new_df


def drop_nan(df):
    df["rate"].replace("NEW", np.nan)
    df.dropna(how='any',inplace=True)
    return df


def transform_rate(df):
    rates = []
    for _, row in df.iterrows():
        rate_in_float = float(row["rate"].split("/")[0])
        rates.append(rate_in_float)
    df["rate"] = rates
    return df


def transform_price(df):
    prices = []
    for _, row in df.iterrows():
        price_s = row["price"]
        price = int(price_s.replace(",", ""))
        prices.append(price)
    df["price"] = prices
    return df



def transform_address(df):
    latitudes = []
    longitudes = []
    for _, row in df.iterrows():
        latitude, longitude = get_geo_info(row)
        latitudes.append(latitude)
        longitudes.append(longitude)
    df["lat"] = latitudes
    df["lon"] = longitudes
    return df


def get_geo_info(row):
    address = row["address"]
    location = geolocator.geocode(address)
    next_index = address.find(",")

    while not location and next_index != -1:
        address = address[(next_index+1):]
        location = geolocator.geocode(address)
        next_index = address.find(",")

    if not location:
        location = geolocator.geocode(row["location"])
    return location.latitude, location.longitude


def rename_features(df):
    df.rename(column={'approx_cost(for two people)': 'price', 'listed_in(city)': 'city_area',
                      'listed_in(type)': 'meal_type'})
    return df


def data_cleanint(df):
    df = drop_address_data(df)
    df = drop_irrelevant_data(df)
    df = drop_menu_related_data(df)
    df = drop_nan(df)

    df = rename_features(df)
    df = transform_price(df)
    df = transform_address(df)
    df = transform_rate(df)




def test():
    test_data = {"address": "942, 21st Main Road, 2nd Stage, Banashankari, Bangalore"}
    print(get_geo_info(test_data))


if __name__ == "__main__":
    # test()
    main()