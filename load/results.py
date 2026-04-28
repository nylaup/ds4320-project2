import pandas as pd
import numpy as np
import logging

#create log file 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='results_data.log'
)
logger = logging.getLogger(__name__) 

#get county level election results from precinct level 
# data sourced frm csv from https://github.com/tonmcg/US_County_Level_Election_Results_08-24/tree/master

df_2020 = pd.read_csv("../data/2020_US_County_Level_Presidential_Results.csv")
df_2016 = pd.read_csv("../data/2016_US_County_Level_Presidential_Results.csv")
logger.info("Loaded 2020 and 2016 election results data")

try: 
    #calculate the winner for each county in 2020 and 2016
    df_2020["win_2020"] = np.where(df_2020["per_gop"] > df_2020["per_dem"], "gop", "dem")
    df_2016["win_2016"] = np.where(df_2016["per_gop"] > df_2016["per_dem"], "gop", "dem")
    logger.info("Calculated winners for 2020 and 2016 election results")

    #clean 2016 fips code to standardize 
    df_2016["fips"] = df_2016["combined_fips"].astype(str).str.zfill(5)
    df_2020["fips"] = df_2020["county_fips"].astype(str).str.zfill(5)
    logger.info("Standardized FIPS codes")
except Exception as e:  
    logger.error(f"Error processing election results data: {e}")
    raise

try:
    #combine 2020 and 2016 on fips code with year as suffix 
    df = df_2016[["fips", "win_2016", "per_point_diff"]].merge(
        df_2020[["fips", "win_2020", "per_point_diff"]],
        on="fips",
        how="inner",
        suffixes=("_2016", "_2020")
    )
    logger.info("Merged 2016 and 2020 data on FIPS codes")

    #calculate if flip 
    df["flip"] = (df["win_2016"] != df["win_2020"]).astype(int)

    #fix 2016 pct difference 
    df["per_point_diff_2016"] = (
        df["per_point_diff_2016"]
        .str.replace("%", "", regex=False)
        .astype(float) / 100
    )
    #2016 ppd is absolute value, add sign to align with 2020 ppd 
    df["per_point_diff_2016"] = np.where(
        df["win_2016"] == "dem",
        -df["per_point_diff_2016"],
        df["per_point_diff_2016"])

    df["fips"] = pd.to_numeric(df["fips"]) #convert fips for merging 
    logger.info("Cleaned 2016 ppd and flip variables")
except Exception as e:
    logger.error(f"Error merging and cleaning 2016 and 2020 data: {e}")
    raise

#Read in past election results 
df_past = pd.read_csv("../data/US_County_Level_Presidential_Results_08-16.csv")

try:
    #Calculate percentages for 2008 and 2012 elections
    df_past["2008_gop_pct"] = df_past["gop_2008"] / df_past["total_2008"]
    df_past["2008_dem_pct"] = df_past["dem_2008"] / df_past["total_2008"]
    df_past["2012_gop_pct"] = df_past["gop_2012"] / df_past["total_2012"]
    df_past["2012_dem_pct"] = df_past["dem_2012"] / df_past["total_2012"]
    logger.info("Read in past data and calculate voter share percents")

    df_past_pcts = df_past[["fips_code"]] #create new df for percent wins 
    #since per_point_diff is calculated as gop - dem in csv, calculate in that same way for 2008 and 2012 
    df_past_pcts["2008_dif"] = df_past["2008_gop_pct"] - df_past["2008_dem_pct"]
    df_past_pcts["2012_dif"] = df_past["2012_gop_pct"] - df_past["2012_dem_pct"] 

    df_past_pcts = df_past_pcts.rename(columns={"fips_code": "fips"}) #fix naming for merge 

    merged = df.merge(df_past_pcts, on="fips") #merge historic data with 2016 & 2020
    logger.info("Merged 2008 & 2012 election data with 2016 & 2020 data")
except Exception as e:
    logger.error(f"Error processing past election data: {e}")
    raise

#convert dataframe to csv 
merged.to_csv("../data/county_results.csv", index=False)
logger.info("Saved final dataset to county_results.csv")