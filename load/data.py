import pymongo
from pymongo import MongoClient
import json
import pandas as pd
import matplotlib.pyplot as plt

uri = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.yxwmo97.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["election_prediction"]
collection = db["counties"]