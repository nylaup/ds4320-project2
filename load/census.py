import requests
import pandas as pd

API_KEY = " " #fill in with api key 

#function to get all variables for a given table prefix
def get_table_vars(year, table_prefix):
    meta_url = f"https://api.census.gov/data/{year}/acs/acs5/variables.json"
    res = requests.get(meta_url).json()
    
    vars_list = [
        var for var in res["variables"].keys()
        if var.startswith(table_prefix) and var.endswith("E")
    ]
    
    return vars_list

#list of variables to get from census api 
def build_variable_list(year):
    base_vars = [
        "B02001_002E",  #white
        "B02001_003E",  #black
        "B19013_001E",  #med hh income
        "B17001_002E",  #poverty
        "B23025_004E",   #employed
        "B01001_001E" #total population
    ]
    
    #tables that have multiple 
    sex_age = get_table_vars(year, "B01001")
    education = get_table_vars(year, "B15003")
    homeownership = get_table_vars(year, "B25003")
    immigration = get_table_vars(year, "B05002")
    
    all_vars = base_vars + sex_age + education + homeownership + immigration
    
    return ",".join(all_vars)

#chunks to not hit api limit 
def chunk_list(lst, size=45): 
    for i in range(0, len(lst), size):
        yield lst[i:i+size]

#function to get census data for given year and return as dataframe 
def get_data(year):
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    
    vars_list = build_variable_list(year).split(",")
    
    dfs = []

    for i, chunk in enumerate(chunk_list(vars_list)):
        #get data in chunks, include name for merging 
        if i == 0:
            get_vars = ["NAME"] + chunk
        else:
            get_vars = chunk

        params = {
            "get": ",".join(get_vars),
            "for": "county:*",
            "in": "state:*",
            "key": API_KEY
        }
        
        r = requests.get(url, params=params) #request from url 
        data = r.json()
        df_chunk = pd.DataFrame(data[1:], columns=data[0])
        
        dfs.append(df_chunk)
    
    #merge chunks on fips code with state & county 
    df = dfs[0]
    for d in dfs[1:]:
        df = df.merge(d, on=["state", "county"])
    
    df["fips"] = df["state"] + df["county"] #create fips from state and county 
    df["year"] = year #create year column for finding difference 

    working_cols = [ #group all ages
    "B01001_007E","B01001_008E","B01001_009E",  
    "B01001_010E","B01001_011E","B01001_012E",
    "B01001_031E","B01001_032E","B01001_033E",  
    "B01001_034E","B01001_035E","B01001_036E"
    ]
    df["working_age_pop"] = df[working_cols].astype(float).sum(axis=1)

    #group all columns for college education 
    college_cols = ["B15003_022E","B15003_023E","B15003_024E","B15003_025E"]
    df["college_pop"] = df[college_cols].astype(float).sum(axis=1)

    #create columns for census api collected variables 
    df["home_total"] = df["B25003_001E"].astype(float)
    df["homeowner"] = df["B25003_002E"].astype(float) 
    df["renter"] = df["B25003_003E"].astype(float)
    df["imm_total"] = df["B05002_001E"].astype(float)
    df["foreign_born"] = df["B05002_013E"].astype(float)

    #rename columns from to readable names 
    df = df.rename(columns={"B02001_002E": "White", "B02001_003E": "Black", "B19013_001E": "Med_HH_Income", "B17001_002E": "Poverty", "B23025_004E": "Employed"})
    df = df.rename(columns={"B01001_001E": "Total_Population"})
    
    #drop extra columns 
    df.drop(columns=[col for col in df.columns if col.startswith("B")], inplace=True)
    df.drop(columns=['NAME'], inplace=True)

    return df

#get data from both years 
df20 = get_data(2020)
df16 = get_data(2016)

#merge both years on fips code, adding year suffix for clarity with data 
df = df16.merge(df20, on="fips", suffixes=("_2016", "_2020"))

#create dataframe for percent changes 
pct_change_df = pd.DataFrame() 
pct_change_df["fips"] = df["fips"]

for col in df.columns:
    if col.endswith("_2016"): #for demographic columns ending in 2016
        base_col = col.replace("_2016", "")
        col_2020 = base_col + "_2020"
        
        if col_2020 in df.columns:
            #calculate percent changes 
            pct_change_df[base_col + "_pct_change"] = (
                (df[col_2020].astype(float) - df[col].astype(float)) 
                / df[col].astype(float)
            )

#drop extra columns not needed for analysis 
pct_change_df.drop(columns=['state_pct_change', 'county_pct_change', 'year_pct_change'], inplace=True)

#convert dataframe to csv
pct_change_df.to_csv("../data/census_data.csv", index=False)