import pandas as pd
from geopy.geocoders import Nominatim
import numpy as np
import folium
from folium.plugins import HeatMap, FastMarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import ExtraTreesRegressor


def read_data():
    df = pd.read_csv("zomato.csv")
    return df
​

def drop_unnecessary_columns(df):
    df.drop(columns=['dish_liked', 'cuisines', 'menu_item'], inplace=True)
    df.drop(columns=['name', 'url', 'phone', 'reviews_list', "address"], inplace=True)
    return df

​
df = drop_unnecessary_columns(df)
df.columns

def remove_nan(df):
    df["rate"] = df["rate"].replace("NEW", np.nan)
    df["rate"] = df["rate"].replace("-", np.nan)
    df.dropna(how='any', inplace=True)
    return df

def rename_features(df):
    df.rename(columns={'approx_cost(for two people)': 'price', 'listed_in(city)': 'city_area',
                       'listed_in(type)': 'meal_type'}, inplace=True)
    return df

​
​
df = rename_features(df)
df.columns

def transform_rate(df):
    rates = []
    for _, row in df.iterrows():
        rate_in_float = float(row["rate"].split("/")[0])
        rates.append(rate_in_float)
    df["rate"] = rates
    return df

​
​

def transform_price(df):
    prices = []
    for _, row in df.iterrows():
        price_s = row["price"]
        price_s = price_s.replace(",", "")
        price = int(price_s)
        prices.append(price)
    df["price"] = prices
    return df

​
df = transform_rate(df)
df = transform_price(df)


def get_geo_info_location(location):
    geo_info = geolocator.geocode(location)
    if geo_info is None:
        return np.nan, np.nan
    return geo_info.latitude, geo_info.longitude

​
​

def get_location_coordinate(df):
    all_location = df["location"].unique()
    coordinate = dict()
    for location in all_location:
        coordinate[location] = get_geo_info_location(location + ", Bangalore")
    return coordinate

​
​
geolocator = Nominatim(user_agent="app")
lat_lon_location = get_location_coordinate(df)
lat_lon_location


def Encode(df):
    for column in df.columns[~df.columns.isin(['rate', 'price', 'votes'])]:
        df[column] = df[column].factorize()[0]
    return df

​
df_float = Encode(df.copy())
df_float.head()

def get_train_test_data(df_float):
    x = df_float.iloc[:, [0, 1, 4, 5, 6, 7]]
    y = df_float.iloc[:, [2, 3]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.1, random_state=353)
    return x_train, x_test, y_train, y_test


x_train, x_test, y_train, y_test = get_train_test_data(df_float)
x_train.head()

def train_random_forest(x_train, y_train):
    random_forest = RandomForestRegressor(n_estimators=500, random_state=329, min_samples_leaf=.0001)
    random_forest.fit(x_train, y_train)
    return random_forest

​
​
RF_model = train_random_forest(x_train, y_train)
Model
training - -- decision
tree
regression
The
following
code
uses
decision
tree
regression
to
predict
the
outcome.
In[20]:


def train_decision_tree(x_train, y_train):
    decision_tree = DecisionTreeRegressor()
    decision_tree.fit(x_train, y_train)
    return decision_tree

​
​
DT_model = train_decision_tree(x_train, y_train)
Model
training - -- linear
regression
The
following
code
uses
linear
regression
to
predict
the
outcome.
In[21]:


def train_linear_regression(x_train, y_train):
    linear_regression = LinearRegression()
    linear_regression.fit(x_train, y_train)
    return linear_regression


def train_extra_tree(x_train, y_train):
    extra_tree = ExtraTreesRegressor(n_estimators=100)
    extra_tree.fit(x_train, y_train)
    return extra_tree

​
​
ET_model = train_extra_tree(x_train, y_train)


def test_model(model, x_test, y_test):
    y_predict = model.predict(x_test)
    score = r2_score(y_test, y_predict)
    return score

RF_score = test_model(RF_model, x_test, y_test)
DT_score = test_model(DT_model, x_test, y_test)
LR_score = test_model(LR_model, x_test, y_test)
ET_score = test_model(ET_model, x_test, y_test)
​
​
evaluation = pd.DataFrame({"Model": ["Random Forest", "Decision Tree", "Linear Regression", "Extra Trees"],
                           "R^2 Score": [RF_score, DT_score, LR_score, ET_score]})
​
evaluation.sort_values(by='R^2 Score', ascending=False, ignore_index=True)



def heatmap_generate(lat_lon_location, location_info, need_clustering=False):
    map_info = []
    for location in location_info:
        if not np.isnan(lat_lon_location[location][0]):
            map_info.append(list(lat_lon_location[location]) + [float(location_info[location])])
    base_map = folium.Map(location=[12.9716, 77.5946], zoom_start=11)
    HeatMap(map_info, zoom=20, radius=15).add_to(base_map)
    if need_clustering:
        FastMarkerCluster(map_info).add_to(base_map)
    return base_map


def generate_count_heatmap():
    location_count = dict(df['location'].value_counts())
    heatmap_count = heatmap_generate(lat_lon_location, location_count)
    return heatmap_count


def generate_avg_heatmap():
    avg_price = dict(df.groupby(['location'])['price'].mean())
    heatmap_avg = heatmap_generate(lat_lon_location, avg_price, need_clustering=True)
    return heatmap_avg


def generate_med_heatmap():
    med_price = dict(df.groupby(['location'])['price'].median())
    heatmap_med = heatmap_generate(lat_lon_location, med_price, need_clustering=True)
    return heatmap_med

def plot_price_dist():
    fig, ax = plt.subplots(figsize=[10, 4])
    sns.distplot(df["price"], ax=ax)


def plot_rate_dist():
    fig, ax = plt.subplots(figsize=[10, 4])
    sns.distplot(df["rate"], ax=ax)


def plot_rate_votes():
    plt.plot(df["rate"], df["votes"], "ob")
    plt.show()


plot_rate_votes()