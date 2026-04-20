import pymongo
from pymongo import MongoClient
import json
import pandas as pd
import matplotlib.pyplot as plt

#add credentials for mongodb atlas
USER = " "
PASSWORD = " "
uri = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.yxwmo97.mongodb.net/?appName=Cluster0"

#read in created csvs for election results and census data
election = pd.read_csv("../data/county_results.csv")
census = pd.read_csv("../data/census_data.csv")
merged = election.merge(census, on="fips")

documents = [] #create proper nesting structure in documents to add 
for _, row in merged.iterrows():
    doc = {
        "fips": row["fips"],
        "election": {
            "win_2016": row["win_2016"],
            "win_2020": row["win_2020"],
            "flip": row["flip"]
        },
        "demographics": {
            "white_pop": row["White_pct_change"],
            "med_inc": row["Med_HH_Income_pct_change"],
            "poverty": row["Poverty_pct_change"],
            "employed": row["Employed_pct_change"],
            "working_age": row["working_age_pop_pct_change"],
            "college_pop": row["college_pop_pct_change"],
            "homeowner": row["homeowner_pct_change"],
            "renter": row["renter_pct_change"],
            "imm": row["imm_total_pct_change"]
        }
    }
    documents.append(doc)

client = MongoClient(uri) #connect to mongodb 

db = client["election_prediction"]
collection = db["counties"]

collection.insert_many(documents)