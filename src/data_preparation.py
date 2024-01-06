import pandas as pd
from constants import *


def map_config(style):
    map_config = {
        "api_keys": {'mapbox': access_api_token},
        "map_provider": 'mapbox',
        "map_style": style
    }
    return map_config


df = pd.read_csv("data/europe_acled.csv")
df["event_date"] = pd.to_datetime(df["event_date"])
df_ue = df[~df.country.isin(["Ukraine", "Russia"])]



# for col in ["longitude", "latitude"]:
#     df[col] = pd.to_numeric(df[col], errors="coerce")

# df["event_date"] = pd.to_datetime(df["event_date"])
# df["fatalities"] = df["fatalities"].astype(int)

# df["year"] = df["event_date"].dt.year
# df["month"] = df["event_date"].dt.month_name()
# df["day"] = df["event_date"].dt.day
# df["day_name"] = df["event_date"].dt.day_name()

# df["dayofyear"] = df["event_date"].dt.dayofyear
# df["dayofyear"] = df["dayofyear"].where(
#     ~((df["event_date"].dt.month > 2) &
#       (df["event_date"].dt.is_leap_year)),
#     df["dayofyear"] - 1,
# )


# Summary of key figures

d1 = df.groupby(["country"], as_index=False).size().rename(columns={"size": "events"})
d2 = df.groupby(["country"], as_index=False)["fatalities"].sum()
data = pd.merge(d1, d2, on=["country"])

d3 = df.groupby(["country", "event_type"], as_index=False).size()
d3 = d3.pivot_table(index="country", columns="event_type").reset_index().fillna(0)
d3 = d3["size"]

d4 = df.groupby(["country", "disorder_type"], as_index=False).size()
d4 = d4.pivot_table(index="country", columns="disorder_type").reset_index().fillna(0)
d4 = d4["size"]

d5 = df.groupby(["country", "location"], as_index=False).size().sort_values(by="size",ascending=False)
d5 = d5.drop_duplicates("country", keep="first").sort_values(by="country")

data = pd.concat([data, d3, d4], axis=1)
data = pd.merge(data, d5, on="country")
data = data.rename(columns={"size": "Events"})
data = data.sort_values(by="Events", ascending=False)
