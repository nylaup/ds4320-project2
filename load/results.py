import pandas as pd
import numpy as np

#get county level election results from precinct level 
# data sourced frm csv from https://github.com/tonmcg/US_County_Level_Election_Results_08-24/blob/master/2020_US_County_Level_Presidential_Results.csv

df_2020 = pd.read_csv("../data/2020_US_County_Level_Presidential_Results.csv")
df_2016 = pd.read_csv("../data/2016_US_County_Level_Presidential_Results.csv")

#calculate the winner for each county in 2020 and 2016
df_2020["win_2020"] = np.where(df_2020["per_gop"] > df_2020["per_dem"], "gop", "dem")
df_2016["win_2016"] = np.where(df_2016["per_gop"] > df_2016["per_dem"], "gop", "dem")

#clean 2016 fips code to standardize 
df_2016["combined_fips"] = df_2016["combined_fips"].astype(str).str.zfill(5)
df_2016["combined_fips"] = pd.to_numeric(df_2016["combined_fips"])

#combine 2020 and 2016 on fips code
df = df_2016[["combined_fips", "win_2016"]].merge(
    df_2020[["county_fips", "win_2020"]],
    left_on="combined_fips", right_on="county_fips", how="inner")

#calculae if flip 
df["flip"] = np.where(df["win_2016"] != df["win_2020"], 1, 0)