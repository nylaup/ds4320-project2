## Imports & Setup

## Data Preparation




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fips</th>
      <th>election.win_2016</th>
      <th>election.win_2020</th>
      <th>election.flip</th>
      <th>election.per_point_diff_2016</th>
      <th>election.per_point_diff_2020</th>
      <th>election.2008_dif</th>
      <th>election.2012_dif</th>
      <th>demographics.white_pop</th>
      <th>demographics.total_pop</th>
      <th>demographics.med_inc</th>
      <th>demographics.med_rent</th>
      <th>demographics.senior_pop</th>
      <th>demographics.hs_edu_pop</th>
      <th>demographics.low_inc</th>
      <th>demographics.high_inc</th>
      <th>demographics.homeowner</th>
      <th>demographics.renter</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1001</td>
      <td>gop</td>
      <td>gop</td>
      <td>0</td>
      <td>0.4948</td>
      <td>0.444184</td>
      <td>0.478406</td>
      <td>0.460580</td>
      <td>-0.003805</td>
      <td>0.010718</td>
      <td>0.091960</td>
      <td>0.128348</td>
      <td>0.103314</td>
      <td>-0.004528</td>
      <td>-0.011802</td>
      <td>0.262367</td>
      <td>0.057169</td>
      <td>-0.019885</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1003</td>
      <td>gop</td>
      <td>gop</td>
      <td>0</td>
      <td>0.5779</td>
      <td>0.537623</td>
      <td>0.514476</td>
      <td>0.558232</td>
      <td>0.081553</td>
      <td>0.094126</td>
      <td>0.202297</td>
      <td>0.160855</td>
      <td>0.197600</td>
      <td>0.076371</td>
      <td>-0.041240</td>
      <td>0.488574</td>
      <td>0.200557</td>
      <td>-0.090049</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1005</td>
      <td>gop</td>
      <td>gop</td>
      <td>0</td>
      <td>0.0561</td>
      <td>0.076631</td>
      <td>0.014531</td>
      <td>-0.029147</td>
      <td>-0.067820</td>
      <td>-0.059668</td>
      <td>0.030451</td>
      <td>-0.001701</td>
      <td>0.085929</td>
      <td>0.003215</td>
      <td>-0.032242</td>
      <td>0.422613</td>
      <td>-0.009264</td>
      <td>0.077133</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1007</td>
      <td>gop</td>
      <td>gop</td>
      <td>0</td>
      <td>0.5554</td>
      <td>0.577280</td>
      <td>0.458468</td>
      <td>0.468478</td>
      <td>-0.013356</td>
      <td>-0.008772</td>
      <td>0.300307</td>
      <td>0.059633</td>
      <td>0.094048</td>
      <td>0.027449</td>
      <td>-0.163880</td>
      <td>0.572386</td>
      <td>0.060363</td>
      <td>-0.050804</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1009</td>
      <td>gop</td>
      <td>gop</td>
      <td>0</td>
      <td>0.8138</td>
      <td>0.800022</td>
      <td>0.695059</td>
      <td>0.741451</td>
      <td>-0.014562</td>
      <td>0.000884</td>
      <td>0.058643</td>
      <td>0.055468</td>
      <td>0.046467</td>
      <td>0.047695</td>
      <td>-0.018570</td>
      <td>0.543636</td>
      <td>-0.007506</td>
      <td>0.162199</td>
    </tr>
  </tbody>
</table>
</div>



## Solution Analysis 

    Linear Regression | MAE: 0.087, RMSE: 0.116, R^2: 0.865


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


R^2 value is quite high from Linear Regression, but could be better. Linear Regression may not be the best for modeling complex relationships, try again with Random Forest 

    Random Forest | MAE: 0.071, RMSE: 0.093, R^2: 0.913


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


    Random Forest Demographics | MAE: 0.187, RMSE: 0.239, R^2: 0.432


## Analysis Rationale 

I initially wanted to create a logistic regression model that predicted if a county would flip or not, as a binary prediction. I got a very high accuracy, however when looking at the confusion matrix it showed that there was a very high amount of false negatives and the model was actually predicting every county to not flip. This was due to the very large class imbalance inherent to the dataset, where there were very few county flips to sample from. Even after doing a y stratified train test split and balanced class weights in the regression for the underrepresented class, the model still had a very small true positive and was not picking up on the signals used to predict county flipping, even when the decision threshold was modified. Since the logistic model was not performing well, I decided to then try a random forest model, as the logistic regression may have been too simple and linear to properly reflect the relationship, although this still was having issues. I realized county flips may not have been the best way to approach the problem, as there could be counties that had great changes in their voter margins due to demographic changes, but did not exactly flip.              
I reformatted my question to focus on margins between the two parties, as the data already had a column for the percent point difference in parties. Since this was no longer a classification problem, I had to create a regression, and started by creating a linear regression, which had good accuracy, but the random forest regression created was much better at capturing the complexities. I then created models and used feature importance to see which variables were given larger weights by the model. I then only chose variables that were significant to the model's final decisions.       
The model's final feature importance was greatly reliant on the 2012 election margins This shows that election outcomes are incredibly difficult predict and election forecasting remains a difficult task, even if we look at various demographic changes and historical results. Demographic change is less significant in predicting election margins than past history in elections, and these alone could not be used as predictors. 

## Visualization 


    
![png](SolutionPipeline_files/SolutionPipeline_17_0.png)
    


    /home/nylup/DS4320/ds4320-project2/env/lib/python3.10/site-packages/geopandas/geodataframe.py:1969: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      super().__setitem__(key, value)



    
![png](SolutionPipeline_files/SolutionPipeline_20_0.png)
    


## Visualization Rationale 

Since one of our topics of interest was feature importance and asking which features were significant in predicting election margins, I decided to create a graph of the feature importances created by our best performing model, the Random Forest on electoral history and demographic changes. I created this graph as a bar plot, to show the size of each feature so they could be compared, and made it horizontal as some of the feature names were long and would be better displayed horizontally. The graph showed the absolute weights, and interestingly enough the top two features were 2012 and 2008 margins, and these were significantly more important than any demographic changes, which was unexpected. The most important demographic features appeared to be      
This model is meant to be used as a tool to be used to predict future election margins, so I thought an impactful visual would show this model in action and use it to predict margins for a future election. However, the most recent census information that would be guaranteed to be fully accessible was 2022, which was not a presidential election year, but the demographic changes could still be compared to 2020 to get some assessment of demographic changes and predict for margins of a hypothetical election. I chose a random state to predict all the counties in, which happened to be Massachusetts. I had to pull the relevant demographics from the census API, calculate percent changes, merge these with election history, and then use our previous random forest model to predict election margins. I then merged this predicted value and fips codes with county shapefiles to be able to create a graph of Massachusetts counties, color coded by the predicted election margin. Since the percent point difference was not an absolute value, there were two extremes of the election margin, which showed party lean, so I made the legend have a diverging color map so the 0 in the middle would be white and the two diverging sides would be the colors. The colors also were the colors of the political parties, making this graph more relevant.   
