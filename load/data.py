import pymongo
from pymongo import MongoClient
import json
import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

#add credentials for mongodb atlas
USER = os.getenv("MONGO_USER")
PASSWORD = os.getenv("MONGO_PASS")
uri = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.yxwmo97.mongodb.net/?appName=Cluster0"

#create log file 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='mongo_push.log'
)
logger = logging.getLogger(__name__)

#read in created csvs for election results and census data
election = pd.read_csv("../data/county_results.csv")
census = pd.read_csv("../data/census_data.csv")
merged = election.merge(census, on="fips")
logger.info("Merged election and census data on fips code")

try: 
    documents = [] #create proper nesting structure in documents to add 
    for _, row in merged.iterrows():
        doc = {
            "fips": row["fips"],
            "election": {
                "win_2016": row["win_2016"],
                "win_2020": row["win_2020"],
                "flip": row["flip"],
                "per_point_diff_2016": row["per_point_diff_2016"],
                "per_point_diff_2020": row["per_point_diff_2020"],
                "2008_dif": row["2008_dif"],
                "2012_dif": row["2012_dif"]
            },
            "demographics": {
                "white_pop": row["White_pct_change"],
                "total_pop": row["Total_Population_pct_change"],
                "med_inc": row["Med_HH_Income_pct_change"],
                "med_rent": row["Med_Rent_pct_change"],
                "senior_pop": row["senior_pop_pct_change"],
                "hs_edu_pop": row["hs_pop_pct_change"],
                "low_inc": row["low_income_pct_change"],
                "high_inc": row["high_income_pct_change"],
                "homeowner": row["homeowner_pct_change"],
                "renter": row["renter_pct_change"]
            }
        }
        documents.append(doc)
    logger.info(f"Created {len(documents)} documents for MongoDB insertion")
except Exception as e:
    logger.error(f"Error creating documents for MongoDB: {e}")
    raise e

try: #error handling for mongodb connection 
    client = MongoClient(uri) #connect to mongodb 
    logger.info("Connected to MongoDB Atlas")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise e

#select database and collection 
db = client["election_prediction"] 
collection = db["counties"] 

try: #error handling for mongodb insertion 
    collection.insert_many(documents)
    logger.info("Successfully inserted documents into MongoDB")
except Exception as e:
    logger.error(f"Failed to insert documents into MongoDB: {e}")
    raise e