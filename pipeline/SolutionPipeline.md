```
#imports
import pandas as pd 
import numpy as np
from pymongo import MongoClient 
import matplotlib.pyplot as plt
import logging
import os 

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import geopandas as gpd
```

```
#create log file 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pipeline.log'
)
logger = logging.getLogger(__name__) 
```

## Data Preparation

```
USER = os.getenv("MONGO_USER")
PASSWORD = os.getenv("MONGO_PASS")

uri = f"mongodb+srv://{USER}:{PASSWORD}@cluster0.yxwmo97.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri) #connect to mongodb 
    db = client["election_prediction"]
    collection = db["counties"]
    logger.info("Successfully connected to MongoDB and collection")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    raise

#find all from collection except id 
cursor = collection.find({}, {"_id": 0})  
docs = list(cursor)

#normalize json to format in dataframe 
df = pd.json_normalize(docs)

logger.info(f"Successfully loaded data into DataFrame with shape {df.shape}")
```

## Solution Analysis 

```
#create X and y to train logistic regression model
y = df["election.per_point_diff_2020"]

#drop election win history as predictors as they aren't relevant to predicting 
X = df.drop(columns=["election.flip", "election.win_2016", "election.win_2020", "election.per_point_diff_2016", "election.per_point_diff_2020"])

#train test split split with 20% test size 
#add stratify to ensure class balance in train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=29)
logger.info(f"Completed train-test split")
```
```
#Linear Regression on per point difference 
pipeline_lr = Pipeline([
    ("scaler", StandardScaler()), #scale all features 
    ("model", LinearRegression())
])

pipeline_lr.fit(X_train, y_train) #fit to training data 
y_pred_lr = pipeline_lr.predict(X_test) #predict on test data

#evaluate mae, rmse, and r2 for model
mae_lr = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
r2_lr = r2_score(y_test, y_pred_lr)

print(f"Linear Regression | MAE: {mae_lr:.3f}, RMSE: {rmse_lr:.3f}, R^2: {r2_lr:.3f}")
logger.info(f"Linear Regression | MAE: {mae_lr:.3f}, RMSE: {rmse_lr:.3f}, R^2: {r2_lr:.3f}")
```
Linear Regression - MAE: 0.087, RMSE: 0.116, R^2: 0.865

```
#get trained random forest model 
lr_model = pipeline_lr.named_steps["model"]

#get feature importances from random forest 
coefficients = lr_model.coef_

#print feature importances 
feature_importance_df = pd.DataFrame({
    "feature": X_train.columns,
    "weight": coefficients
})

#make features absolute values
feature_importance_df["weight"] = np.abs(feature_importance_df["weight"])

feature_importance_df = feature_importance_df.sort_values( #sort 
    by="weight", ascending=False)
logger.info("Feature Importances Calculated from LR")

print("Feature Importances from Linear Regression:")
print(feature_importance_df)
logger.info(f"Top 3 feature importances: {feature_importance_df.head(3).to_string(index=False)}")
```
Feature Importances from Linear Regression:      
                    feature    weight      
2         election.2012_dif  0.323233      
4    demographics.total_pop  0.066066      
1         election.2008_dif  0.036836      
7   demographics.senior_pop  0.035068      
3    demographics.white_pop  0.033967      
8   demographics.hs_edu_pop  0.018202      
11   demographics.homeowner  0.013673      
12      demographics.renter  0.013042      
10    demographics.high_inc  0.010268      
0                      fips  0.004440      
6     demographics.med_rent  0.002491      
9      demographics.low_inc  0.001792      
5      demographics.med_inc  0.001133      

```
#Random Forest Regressor on per point difference 
pipeline_rf = Pipeline([
    ("scaler", StandardScaler()), #scale features 
    ("model", RandomForestRegressor(n_estimators=100, random_state=42))
])

pipeline_rf.fit(X_train, y_train) #fit to training 
y_pred_rf = pipeline_rf.predict(X_test) #predict on test 

#evaluate performance metrics on test and predicted 
mae_rf = mean_absolute_error(y_test, y_pred_rf) 
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest | MAE: {mae_rf:.3f}, RMSE: {rmse_rf:.3f}, R^2: {r2_rf:.3f}")
logger.info(f"Random Forest | MAE: {mae_rf:.3f}, RMSE: {rmse_rf:.3f}, R^2: {r2_rf:.3f}")
```
Random Forest - MAE: 0.071, RMSE: 0.093, R^2: 0.913

```
#get trained random forest model 
rf_model = pipeline_rf.named_steps["model"]

#get feature importances from random forest 
importances = rf_model.feature_importances_

#make features absolute values
feature_importance_df["weight"] = np.abs(feature_importance_df["weight"])

feature_importance_df = feature_importance_df.sort_values( #sort 
    by="weight", ascending=False)
logger.info("Feature Importances Calculated from LR")

#print feature importances 
feature_importance_df = pd.DataFrame({
    "feature": X_train.columns,
    "importance": importances})

feature_importance_df["importance"] = np.abs(feature_importance_df["importance"]) #absolute val of weights
feature_importance_df = feature_importance_df.sort_values(by="importance", ascending=False) #sort 
logger.info("Feature Importances Calculated from RF")

print("Feature Importances from Random Forest:")
print(feature_importance_df)
logger.info(f"Top 3 feature importances: {feature_importance_df.head(3).to_string(index=False)}")
```
Feature Importances from Random Forest:      
                    feature  importance      
2         election.2012_dif    0.807685      
1         election.2008_dif    0.070170      
4    demographics.total_pop    0.029157      
7   demographics.senior_pop    0.027027      
0                      fips    0.010075      
12      demographics.renter    0.008682      
3    demographics.white_pop    0.007921      
6     demographics.med_rent    0.007665      
10    demographics.high_inc    0.007081      
8   demographics.hs_edu_pop    0.006963      
5      demographics.med_inc    0.006299      
11   demographics.homeowner    0.006111      
9      demographics.low_inc    0.005166      

```
#try model without any election history to assess just demographic features
X_train = X_train.drop(columns=["election.2012_dif", "election.2008_dif"])
X_test = X_test.drop(columns=["election.2012_dif", "election.2008_dif"])

#Random Forest Regressor on per point difference change
pipeline_rf = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor(n_estimators=100, random_state=42))
])

pipeline_rf.fit(X_train, y_train)
y_pred_rf = pipeline_rf.predict(X_test)

mae_rf = mean_absolute_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
r2_rf = r2_score(y_test, y_pred_rf)

print(f"Random Forest Demographics - MAE: {mae_rf:.3f}, RMSE: {rmse_rf:.3f}, R^2: {r2_rf:.3f}")
logger.info(f"Random Forest Demographics - MAE: {mae_rf:.3f}, RMSE: {rmse_rf:.3f}, R^2: {r2_rf:.3f}")
```
Random Forest Demographics - MAE: 0.187, RMSE: 0.239, R^2: 0.432

## Analysis Rationale    

I initially wanted to create a logistic regression model that predicted if a county would flip or not, as a binary prediction. I got a very high accuracy, however when looking at the confusion matrix it showed that there was a very high amount of false negatives and the model was actually predicting every county to not flip. This was due to the very large class imbalance inherent to the dataset, where there were very few county flips to sample from. Even after doing a y stratified train test split and balanced class weights in the regression for the underrepresented class, the model still had a very small true positive and was not picking up on the signals used to predict county flipping, even when the decision threshold was modified. Since the logistic model was not performing well, I decided to then try a random forest model, as the logistic regression may have been too simple and linear to properly reflect the relationship, although this still was having issues.        
I realized county flips may not have been the best way to approach the problem, as there could be counties that had great changes in their voter margins due to demographic changes, but did not exactly flip. I reformatted my question to focus on margins between the two parties, as the data already had a column for the percent point difference in parties. Since this was no longer a classification problem, I had to create a regression, and decided to use a random forest regression, as a linear may have been too simplistic for the problem. Still, the R^2 of this model was still quite low. I decided to test out different polynomial features and interactions between the demographic changes and historic election data and adding feature engineering. I then created models and used permutation importance to see which variables were given larger weights by the model. After running various models and testing the optimal setup, I chose interactions pertaining to features that were significant to the model's final decisions.        
Even after this model testing, the best R^2 value was still under 70%. This shows that election outcomes are incredibly difficult predict and election forecasting remains a difficult task, even if we look at various demographic changes and historical results. Still, the model did improve over other models and had some predictive accuracy. Most of the significant features from the permutation importance were based on historic performance and various interactions with past election margins, which shows that demographic change is less significant in predicting election margins than past history in elections, and these alone could not be used as predictors. Interestingly, the most important features involving demographics were based on the median household income, senior population, the white population, and median rent. This shows that financial details, age, and some racial information are significant changes, but demographic changes that I thought would be important, like higher education, immigrant population, or specific minority populations were not as important. 

## Visualization 

```
#bar plot of feature importances from random forest 
feature_importance_df.plot(
    kind="barh",
    x="feature",
    y="importance",
    legend=False
)
plt.title("Feature Importances from Random Forest")

#save plot as png 
plt.savefig("../images/feature_importances.png", dpi=300, bbox_inches="tight")
plt.show()
logger.info("Created and saved feature importance plot from RF")
```
![Feature Importances](../images/feature_importances.png)

```
#get demographic changes for massachusetts 
mass_dem = pd.read_csv("../data/mass.csv")
mass_elect = df[["fips", "election.2008_dif", "election.2012_dif"]] #get election history

#merge demographics with election history to keep only massachusetts counties 
merged = pd.merge(mass_elect, mass_dem, on="fips", how="right")

#reorder columns to align with desired order for model 
col_order = ['fips', 'election.2008_dif', 'election.2012_dif',
       'demographics.white_pop', 'demographics.total_pop',
       'demographics.med_inc', 'demographics.med_rent',
       'demographics.senior_pop', 'demographics.hs_edu_pop',
       'demographics.low_inc', 'demographics.high_inc',
       'demographics.homeowner', 'demographics.renter']
merged = merged[col_order]

#predict on massachusetts counties using random forest model 
merged['y_pred_rf'] = pipeline_rf.predict(merged)

#new dataframe storing fips and predicted margins, for graphing 
data = merged[["fips", "y_pred_rf"]] 

logger.log("Predicted margins for Massachusetts counties using Random Forest model")
```

```
#get county shapefile 
url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_county_500k.zip"
counties = gpd.read_file(url)
#merge shapefiles with data to get geometry, only containing massachusetts counties
ma_counties = counties[counties["STATEFP"] == "25"]
ma_counties["fips"] = ma_counties["STATEFP"] + ma_counties["COUNTYFP"]
ma_counties["fips"] = pd.to_numeric(ma_counties["fips"])
ma_merged = pd.merge(data, ma_counties, on="fips")

logger.info("Get county shapefiles for MA and merge with data")
```

```
#convert dataframe to geodataframe for graphing 
ma_merged = gpd.GeoDataFrame(
    ma_merged,
    geometry="geometry"
)

fig, ax = plt.subplots(1, 1, figsize=(8, 8))

ma_merged.plot(
    column="y_pred_rf", #plot predicted margins
    cmap="coolwarm", #improved color map 
    linewidth=0.8,
    edgecolor="black",
    legend=True,
    legend_kwds={"label": "Margin (gop-dem)"},
    ax=ax
)

ax.set_title("Massachusetts Counties Predicted Margins for Future Election")
ax.axis("off") #no axis on map 

#save as png
plt.savefig("../images/mass_predictions.png", dpi=300, bbox_inches="tight")
logger.info("Created and saved map of Massachusetts county predictions")

plt.show()
```
![Massachusetts Prediction](../images/mass_predictions.png)

## Visualization Rationale 

Since one of our topics of interest was feature importance and asking which features were significant in predicting election margins, I decided to create a graph of the feature importances created by our best performing model, the Random Forest on electoral history and demographic changes. I created this graph as a bar plot, to show the size of each feature so they could be compared, and made it horizontal as some of the feature names were long and would be better displayed horizontally. The graph showed the absolute weights, and interestingly enough the top two features were 2012 and 2008 margins, and these were significantly more important than any demographic changes, which was unexpected. The most important demographic features appeared to be      
This model is meant to be used as a tool to be used to predict future election margins, so I thought an impactful visual would show this model in action and use it to predict margins for a future election. However, the most recent census information that would be guaranteed to be fully accessible was 2022, which was not a presidential election year, but the demographic changes could still be compared to 2020 to get some assessment of demographic changes and predict for margins of a hypothetical election. I chose a random state to predict all the counties in, which happened to be Massachusetts. I had to pull the relevant demographics from the census API, calculate percent changes, merge these with election history, and then use our previous random forest model to predict election margins. I then merged this predicted value and fips codes with county shapefiles to be able to create a graph of Massachusetts counties, color coded by the predicted election margin. Since the percent point difference was not an absolute value, there were two extremes of the election margin, which showed party lean, so I made the legend have a diverging color map so the 0 in the middle would be white and the two diverging sides would be the colors. The colors also were the colors of the political parties, making this graph more relevant.   
