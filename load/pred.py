import requests
import pandas as pd
import logging
import numpy as np
import os

#get api key
API_KEY = os.getenv("CENSUS_API_KEY")

#create log file 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='predict.log'
)
logger = logging.getLogger(__name__)

#builds list of variables to get from census api 
def build_enhanced_variable_list():
    base_vars = [
        "B02001_002E", #White Only 
        "B19013_001E", #Med Inc 
        "B01001_001E" #Total Pop
    ]

    senior_cols = ( #grouping all senior population columns
        [f"B01001_{i:03d}E" for i in range(20, 26)] +
        [f"B01001_{i:03d}E" for i in range(44, 50)]
    )

    education_cols = [f"B15003_{i:03d}E" for i in range(1, 26)] #all education levels
    income_cols = [f"B19001_{i:03d}E" for i in range(1, 18)] #all income brackets
 
    housing_cols = [ #grouping all housing variables
        "B25064_001E", #Median Rent 
        "B25003_002E", "B25003_003E" #homeowner and renter
    ]

    all_vars = ( #collect all variables to pull 
        base_vars +
        senior_cols +
        education_cols +
        income_cols +
        housing_cols 
    )

    return sorted(set(all_vars))

#chunks to not hit api limit 
def chunk_list(lst, size=45):
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

#ensures that all columns exist, otherwise filled with 0
def safe_sum(df, cols): 
    cols = [c for c in cols if c in df.columns]
    if not cols:
        return 0
    return (
        df[cols]
        .apply(pd.to_numeric, errors="coerce") #converts to numeric or NaN 
        .sum(axis=1)
    )

#function to get census data for given year and return as dataframe 
def get_data(year):
    url = f"https://api.census.gov/data/{year}/acs/acs5"

    # FIX: ensure NAME is included + list type is correct
    vars_list = ["NAME"] + build_enhanced_variable_list()

    dfs = []

    for chunk in chunk_list(vars_list):
    #get data in chunks, include name for merging 
        params = {
            "get": ",".join(chunk),
            "for": "county:*",
            "in": "state:25", #for only massachusetts
            "key": API_KEY
        }

        r = requests.get(url, params=params) #request from url
        data = r.json()

        df_chunk = pd.DataFrame(data[1:], columns=data[0])
        dfs.append(df_chunk)

    df = pd.concat(dfs, axis=1)
    df = df.loc[:, ~df.columns.duplicated()]

    df["fips"] = df["state"] + df["county"] #create fips code from state and county
    df["year"] = year

    senior_cols = ( #senior population 
        [f"B01001_{i:03d}E" for i in range(20, 26)] +
        [f"B01001_{i:03d}E" for i in range(44, 50)]
    )
    df["senior_pop"] = safe_sum(df, senior_cols)

    #education
    hs_cols = ["B15003_017E","B15003_018E","B15003_019E","B15003_020E","B15003_021E"] #KEEP
    df["hs_pop"] = safe_sum(df, hs_cols)

    #income
    df["low_income"] = safe_sum(df, [f"B19001_{i:03d}E" for i in range(2, 11)])
    df["high_income"] = safe_sum(df, [f"B19001_{i:03d}E" for i in range(14, 18)])

    #housing
    df["homeowner"] = pd.to_numeric(df.get("B25003_002E"), errors="coerce") #KEEP
    df["renter"] = pd.to_numeric(df.get("B25003_003E"), errors="coerce") #KEEP

    rename_map = { #rename columns to readable names
    "B02001_002E": "White",
    "B19013_001E": "Med_HH_Income",
    "B01001_001E": "Total_Population",
    "B25064_001E": "Med_Rent"
    }
    df = df.rename(columns=rename_map)

    #drop extra columns if any remain after renaming 
    df.drop(columns=[c for c in df.columns if c.startswith("B")], inplace=True)
    df.drop(columns=["NAME"], inplace=True, errors="ignore")

    return df

try: 
    #get data for 2020 and 2022
    df20 = get_data(2020)
    logger.info("Successfully retrieved 2020 data")
    df16 = get_data(2022)
    logger.info("Successfully retrieved 2022 data")
except Exception as e:
    logger.error(f"Failed retrieve 2020 and 2022 data: {e}")
    raise e

#merge 2022 and 2020 data on fips code, creating suffix for clarity 
df = df16.merge(df20, on="fips", suffixes=("_2022", "_2020"))
logger.info("Successfully merged 2022 and 2020 data")

#create dataframe for percent changes 
change_df = pd.DataFrame() 
change_df["fips"] = df["fips"]

try: 
    for col in df.columns:
        if col.endswith("_2022"): #demographic columns ending in 2022
            base_col = col.replace("_2022", "")
            col_2020 = base_col + "_2020"
            
            if col_2020 in df.columns: #demographic columns ending in 2020
                old = df[col].astype(float)
                new = df[col_2020].astype(float)

                change = np.where( #handle divide by zero error 
                    old == 0, 0,
                    (new-old) / old) #calculate percent changes 
                change_df[base_col + "_pct_change"] = change
    logger.info("Successfully calculated percent changes")
except Exception as e:
    logger.error(f"Error calculating percent changes: {e}")
    raise e

#drop extra columns not needed for analysis 
change_df.drop(columns=['state_pct_change', 'county_pct_change', 'year_pct_change'], inplace=True)

rename_map = { #rename columns to match with prior for model application
    "White_pct_change": "demographics.white_pop",
    "Total_Population_pct_change": "demographics.total_pop",
    "Med_HH_Income_pct_change": "demographics.med_inc",
    "Med_Rent_pct_change": "demographics.med_rent",
    "senior_pop_pct_change": "demographics.senior_pop",
    "hs_pop_pct_change": "demographics.hs_edu_pop",
    "low_income_pct_change": "demographics.low_inc",
    "high_income_pct_change": "demographics.high_inc",
    "homeowner_pct_change": "demographics.homeowner",
    "renter_pct_change": "demographics.renter"
    }
change_df = change_df.rename(columns=rename_map)

#convert dataframe to csv
change_df.to_csv("../data/mass.csv", index=False)
logger.info("Successfully saved massachusetts data to CSV")