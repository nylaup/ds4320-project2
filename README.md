# DS 4320 Project 1:
This repository contains materials for a project for DS4320 Data by Design on predicting county vote margins in presidential elections. The repository contains files for getting data from election results data and the US Census, loading the data into a document database, a pipeline using a model to predict election margins, and a press release summarizing the project.     
Name: Nyla Upal           
NetID: mge9dn      
DOI: [![DOI](https://zenodo.org/badge/1203167035.svg)](https://doi.org/10.5281/zenodo.19843167)    
Press Release: [Press Release File](https://github.com/nylaup/ds4320-project2/blob/main/PressRelease.md)     
Pipeline: [Solution Pipeline](https://github.com/nylaup/ds4320-project2/blob/main/pipeline/SolutionPipeline.ipynb)      
License: [MIT License](https://github.com/nylaup/ds4320-project2/blob/main/LICENSE)      

## Problem Definition     
#### Initial Problem     
The general problem is predicting election results. The specific problem is predicting county level vote margins in elections, using past election results and demographic changes from 2016 to 2020. The model looks at the Democratic-Republican margin and how it is influenced on other changes, and analyzes which features are most important in this prediction.    


#### Motivation        
During election seasons, swing voters and areas that have a critical amount of votes that could change the outcome of the election are integral to elections. Typically candiates focus a lot of energy on swing states so they can win those uncertain ballots. It would be useful to know what the voter share margin in an area ix expected to be based on changes in demographic information so candidates can take these expected changes into account, and election forecasters can focus on which areas are changing to factor these into their predictions.      

#### Refinement Rationale       
I refined this specific issue to the county level as looking at it at the state level was too general and wouldn't give the refined information that exact counties would provide to best see the trends. As you generalize you lose the unique trends and specific patterns that may shed insight onto changes that cause votes changing. With the next presidental election being in two years, I thought it would be interesting to try and predict which counties may change their votes in that election, based on any changes in their demographics. While I could have just used county demographics to make this prediction, I thought it might be more interesting to only focus on the percent changes of these demographics, as I wanted to see how strongly voting behavior would be tied to shifts in the composition of who lives in an area. For example, one may think that if a county has a large decrease in the population of elderly voters, it may then have a large negative margin, favoring democrats. Based on the availability of election results data, I decided to go with the 2020 election and compare that to the previous election in 2016. I decided that demographic changes would be helpful, as we are assessing changes in votes, so changes in people would give some information on their voting.  

#### Press Release       
[How big of a margin? Predicting county vote margins in future presidential elections](https://github.com/nylaup/ds4320-project2/blob/main/PressRelease.md)

## Domain Exposition 
#### Terminology
| Terms | Definition |     
| :--- | :--- |     
| Flipping | A political party winning a seat previously held by the opposition |
| Margins | Difference between share of votes cast between top two parties (gop - dem in this database) | 
| FIPS Code | A unique numeric identifier used to identify US counties and county equivalents |
| Incumbents | The current holder of an office or position |
| Homeownership | Holding legal title to the property one resides in, contrasting to renters who pay rent to live in a property owned by someone else |
| ACS | American Community Survey administered yearly by the US Census Bureau asking social, economic, housing, and demographic topics |
| Median Income | The middle cutoff where half of the households in an area are earning more and half are earning less |
| R^2 | A measure representing the proportion of the output explained by the model |
| Linear Regression | Machine Learning algorithm modeling continuous variable (y) and various features (x) | 
| Random Forest Regression | Machine Learning model combining multiple decision trees to predict continuous numeric outcomes |             
               

#### Project Domain 
This project is in the domain of political science, specifically in electoral modeling. This seeks to understand why voters make the political choices that they do and how these change over time, often in response to changing social and economic conditions. Political science often dives deep into political systems and their operations and behavior in response to different forms of governance. This project applies data science to this domain by trying to predict county vote changes in an algorithmic way, drawing on demographic and electoral theory of what changes affect voting to create an effective model.         

#### Background Readings
[Folder Link](https://myuva-my.sharepoint.com/:f:/g/personal/mge9dn_virginia_edu/IgCynM8Og8HISp_4b6DqVAsuAVko1N2w9oCttap5TbbRz5Q?e=bBF7a5)         

| Title | Description | Link |
| :--- | :--- | :--- |
| Behind Biden’s 2020 Victory | Background insight of 2020 election and graphing results by different groups of interest | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQB23W7NlTELToItOzcKchoEAeFwk4ZYm9yWW-xwpQ7DuWU?e=grdmDQ) | 
| Demographic indicators of voter shift between 2016 and 2020 presidential elections | Study determining demographic indicators shifting voters from 2016 to 2020 election using Machine Learning algorithms | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQBu35TNoiX1TKvpA8-Ogr5HAVAO8as5H-z9MZPUo_vMQWs?e=XNH2hh) |
| Exit polls show both familiar and new voting blocs sealed Biden’s win | Finding demographic changes related to results of 2020 election compared to 2016 | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQC7-NhceZRPQJshGW6bAY1LAX2k3tf_6-CL4RYNavXtgIw?e=Z3bRxp) |
| Pitfalls of Demographic Forecasts of US Elections | Critique of demographic forecasters for US electoral trends through experiments on elections since 1952 | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQA7bZlFEUS3QKwfnUFORUvkAR3cyF56LQ8ixT2Y_A-rYPU?e=CQchLL) |
| A Bayesian Model for the Prediction of United States Presidential Elections | A study using polling data and election results to explore applications of Bayesian analysis in prediction of election results | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQC7dhg3a4rNTKyhsNQvYnswAc3FRJJert5VSHQsvITthc0?e=5uYFTV) |
                  
                    

## Data Creation 
#### Data Acquisition     
For the election results, I was looking for a dataset that would have the counties for every state with their election results. For this I found a dataset from a github project working to make county-level election results more accessible that scraped election result information from various news sources. In order to get the data I was looking for I used both the 2020 and 2016 election results files and calculated who won the election based on the party percentages and then if the 2020 election result was a county flip or not. I also decided that past election history might also be relevant, so I used the Past Results file to get 2008 and 2016 election results to then calculate the voter share for each party, then find the party margins. 
In order to get the demographic information I called from the US Census API to get select categories from the American Community Survey. For this I had to sign up with an API key, but the data was returned through these calls. Some of the columns used were provided directly by the survey, whereas some had to be aggregated from various other columns and combined.    

#### Creation Code
| File | Description | Link |
| :--- | :--- | :--- |
| Election Results | Results of 2016, 2020, and past elections with information on results | [Link](https://github.com/nylaup/ds4320-project2/blob/main/load/results.py) |
| Demographic Change | Get data for demographic percent changes from 2016 to 2020 from census API | [Link](https://github.com/nylaup/ds4320-project2/blob/main/load/census.py) |
| Mongo Data | Loading data of election results and demographic changes into documents to mongo database | [Link](https://github.com/nylaup/ds4320-project2/blob/main/load/data.py) |
| Prediction Data | Get data from census API to predict margins for Massachusetts in 2022 | [Link](https://github.com/nylaup/ds4320-project2/blob/main/load/pred.py) |

#### Rationale     
Initially I wanted to run a model on a dataset I had found for demographic details providing the context for the 2018 midterms, however this dataset did not actually have the results of the midterm elections. I realized it was incredibly difficult to access data for the outcome of the midterm election in each county, ensuring it also had FIPS codes. I then decided to look at 2020 and compare it to the prior 2016 election, since it was much easier to find information on these larger presidential election years. Initially, I wanted the problem to focus on predicting election flips, however it proved difficult to train a model on this binary classification task as there were very few counties that had flipped from 2016 to 2020, and county flips may not have been the best way to approach the problem, as there could be counties that had great changes in their voter margins due to demographic changes, but did not cross the threshold to flip. I reformatted my question to focus on margins between the two parties, so it would then be a continuous prediction problem, not having to select a specific cutoff for flipping. Using demographic percent changes from 2016 to 2020, I first thought it would be interesting to predict changes in the election margin from 2016 to 2020, however this variable was incredibly difficult to predict from the data I had and all the models created had incredibly low predictive accuracy, so I reiterated the focus of the question to predict only election margins for the past year.         
I had to decide which demographic columns from the census that I thought changes in might affect the election result. I presumed changes in race, income, employment, population, education, age, and immigration may affect voting, so I pulled these from the census. I initially ran a model on all of the variables, then I used permutation importance to see which features and relationships were actually contributing to the model and then only kept the top 15 features, which ended up focusing heavier on income, age, race, education, and homeownership, so I kept only select variables that were significant.       

#### Bias Identification      
The bias in the demographic information could emerge from sampling methods. Any data from the census may be biased from nonresponse, as the survey is voluntary, but there may be specific marginalized groups that are less likely to fill it out, and will thus not accurately be represented by any of the information. If we use change in population, this may also be biased towards assuming places with larger populations already are having more significant changes. Predicting election results from demographic changes is also difficult, as changes in people may not necessary relate to changes in voting patterns.        
Given that the election results information was sourced from different news sources for the different election years, it is possible that this inconsistency could create some bias. Since results are sourced from different news organizations across years, differences in reporting standards or rounding could introduce inconsistencies that are not related to actual voting behavior.
Our project is only focused on a certain amount of demographic variables, and could be ignoring other factors that have large influence, and excluding these may lead to the model over-attributing the features that it does have. We are also only looking at the county level, which may generalize patterns to a broad level that will not necessarily reflect in individual voting preferences.         

#### Bias Mitigation     
Since the biases with the ACS are inherent to the data, we cannot fix them through any data transformations. However we can be cautious when drawing conclusions from the data and accept that conclusions from minority groups may not be accurately representing all invested parties. We can accept numeric conclusions with a certain margin of error to quantify this bias. We could also weight the results differently for underrepresented groups. For the issue with population changes, instead of using raw population change we can use percent change, so the impact of changes is proportional to the context. With the final model, we can acknowledge the uncertainty these biases may introduce into the outcomes.       

## Metadata 
#### Soft-Schema     
While since it is a NoSQL database there is no enforced schema, each document represents a single county uniquely identified by FIPS code, which is numeric. Each county document will have two nested objects, Elections and Demographics. The election result fields of 2020 and 2016 wins will be categorical strings that have allowed values of "dem" and "gop". The value of Flip will be a boolean indicating whether a county's vote flipped (1) from 2016 to 2020 or not (0), and the election margins (dif) will be numeric floats. Demographic variables are all numeric values (float) that represent percent change from 2016 to 2020.     

#### Data Summary     
The data will be stored in documents, and each document will represent one county with the identifier being the unique FIPS code. Inside of this county there will be Election, which will have keys of win_2016, win_2020, per_point_diff_2016, per_point_diff_2020, 2008_dif, 2012_dif and flip, and Demographics, which will have various demographic percent changes; white population, total population, median income, median rent, senior population, highschol & batchelor's educated population, low income population, high income population, homwowners, and renters.      
Example Structure: 
``` json     
{ 
  "fips" : 1001,      
  "election": [
    { 
      "win_2016": "gop",
      "win_2020": "dem",
      "flip": 1,
      "per_point_diff_2016": 0.27965,
      "per_point_diff_2020": 0.10767,
      "2008_dif": 0.42567,
      "2012_dif": 0.38972
    }
  ]     
  "demographics": [
    {
      "white_pop": -0.0038051570513578,
      "total_pop": 0.0107177242093407,
      "med_inc": 0.0919603005706322, 
      "med_rent": 0.1283482142857142, 
      "senior_pop": 0.1033138401559454, 
      "hs_edu_pop": -0.0045276447540269,
      "low_inc": -0.0118024640231908,
      "high_inc": 0.2623670827554322,
      "homeowner": 0.0571691418057563, 
      "renter": -0.0198853457542099
    }
  ]     
}
```

#### Data Dictionary 
Elections
| Name | Data Type | Description | Example |      
| :--- | :--- | :--- | :--- |
| FIPS_Code | Int | Unique identifier for each county (or equivalent) | 1007 |
| win_2016 | Cat | Party who won 2016 presidential election | dem |
| per_point_diff_2016 | Float | Percentage point difference in election result by party in 2016 | 0.4948 |
| win_2020 | Cat | Party who won 2020 presidential election | gop |
| per_point_diff_2020 | Float | Percentage point difference in election result by party in 2020 | 0.5772 |
| Flip | Bool | If county vote flipped from 2016 to 2020 | 0 |  
| 2008_dif | Float | Differences in vote percentage by party for 2008 election result | 0.45846 |
| 2012_dif | Float | Differences in vote percentage by party for 2012 election result | 0.4684 |    


Demographics       
| Name | Data Type | Description | Example |      
| :--- | :--- | :--- | :--- |
| white_pop | Float | Percent difference of population identifying as white | -0.0244 |
| total_pop | Float | Percent difference in total population | 0.0572 |
| median_inc | Float | Percent change in median household income | 0.1310 |
| med_rent | Float | Percent change in median rent | 0.0016 |
| senior_pop | Float | Percent change in senior population | 0.1746 |
| hs_edu_pop | Float | Percent change in population with high school or batchelor's education | 0.0506 |
| low_inc | Float | Percent change in households earning under 50k a year (low income) | 0.1406 | 
| high_inc | Float | Percent change in households earning over 100k a year | -0.1891 |
| homeowner | Float | Percent change in houses occupied by owners | 0.0529 |
| renter | Float | Percent change in houses occupied by renters | 0.0988 |
                


#### Uncertainty 
| Column | Mean | Median | Std Dev | Variance | Min | Max | Range | IQR | Skew | Null % |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FIPS Score | 30647 | 29207 | 14984 | 0.0 | 1001 | 56045 | 55044 | 26966 | -0.07 | 0 |
| per_point_diff_2016 | 0.319406 | 0.382200 | 0.308256 | 0.095022 | -0.887200 | 0.916400 | 1.803600 | 0.397900 | -0.896334 | 0.0 |
| per_point_diff_2020 | 0.317357 | 0.384750 | 0.320430 | 0.102676 | -0.867524 | 0.930909 | 1.798433 | 0.431242 | -0.816190 | 0.0 |
| 2008_dif | 0.153689 | 0.160797 | 0.280941 | 0.078928 | -0.859245 | 2.794960 | 3.654206 | 0.381938 | -0.076316 | 0.0 |
| 2012_dif | 0.213239 | 0.238217 | 0.294904 | 0.086968 | -0.842394 | 0.924138 | 1.766532 | 0.393178 | -0.479841 | 0.0 |
| white_pop | -0.016657 | -0.018293 | 0.053439 | 0.002856 | -0.434615 | 0.746269 | 1.180884 | 0.047900 | 0.967589 | 0.0 |
| total_pop | 0.003536 | -0.002776 | 0.045474 | 0.002068 | -0.299283 | 0.539474 | 0.838757 | 0.045117 | 1.276013 | 0.0 |
| med_inc | -4.117550 | 0.150432 | 238.24170 | 56759 | -13288 | 1.169849 | 13289 | 0.107434 | -55.776315 | 0.0 |
| med_rent | -3230.329529 | 0.104000 | 58517.44822 | 3424292000 | -1415429 | 1.834320 | 1415431 | 0.107449 | -19.078350 | 0.0 |
| senior_pop | 0.102281 | 0.097448 | 0.091152 | 0.008309 | -0.559211 | 1.789474 | 2.348684 | 0.083877 | 2.369519 | 0.0 |
| hs_edu_pop | 0.016364 | 0.011400 | 0.066537 | 0.004427 | -0.658385 | 0.770833 | 1.429218 | 0.069088 | 0.643166 | 0.0 |
| low_inc | -0.096223 | -0.100907 | 0.152900 | 0.023379 | -0.999303 | 1.823529 | 2.822832 | 0.088532 | 1.238606 | 0.0 |
| high_inc | 1.297370 | 0.347368 | 18.520929 | 343.024800 | -1.000000 | 746.410714 | 747.410714 | 0.275068 | 29.652214 | 0.0 |
| homeowner | 0.402297 | 0.030226 | 7.830910 | 61.323150 | -0.999492 | 314.138614 | 315.138614 | 0.081404 | 32.741822 | 0.0 |
| renter | 0.969565 | -0.004453 | 29.058751 | 844.411000 | -0.999591 | 1435.466667 | 1436.466667 | 0.154930 | 43.237558 | 0.0 |

