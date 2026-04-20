# DS 4320 Project 1:
This repository contains materials for a project for DS4320 Data by Design on predicting county flips in presidential elections. The repository contains files for getting data from 
loading the data into a document database, a pipeline using a model to predict ____, and a press release summarizing the project.     
Name: Nyla Upal           
NetID: mge9dn      
DOI:    
Press Release: [Press Release File](https://github.com/nylaup/ds4320-project2/blob/main/PressRelease.md)     
Pipeline: [Solution Pipeline](https://github.com/nylaup/ds4320-project2/blob/main/pipeline/SolutionPipeline.ipynb)      
License: [MIT License](https://github.com/nylaup/ds4320-project2/blob/main/LICENSE)      

## Problem Definition     
#### Initial Problem     
The general problem is predicting election results. The specific problem is predicting if a county will flip its vote in the 2024 presidential election based on demographic changes and counties that flipped their votes in the 2020 election.       

#### Motivation        
During election seasons, swing voters and areas that have a critical amount of votes that could change the outcome of the election are integral to elections. Typically candiates focus a lot of energy on swing states so they can win those uncertain ballots. It would be useful to know which areas are expected to flip their votes based on changes in demographic information so candidates can take these expected flips into account.      

#### Refinement Rationale       
I refined this specific issue to the county level as looking at it at the state level was too general and wouldn't give the refined information that exact counties would provide to best see the trends. As you generalize you lose the unique trends and specific patterns that may shed insight onto changes that cause votes flipping. With the next presidental election being in two years, I thought it would be interesting to try and predict which counties may flip their votes in that election, based on any changes in their demographics. Based on the availability of election results data, I decided to go with the 2020 election and compare that to the previous election in 2016. I decided that demographic changes would be helpful, as we are assessing changes in votes, so changes in people would give some information on their voting.  

#### Press Release       
[Will it flip? Predicting county vote flips in the next presidential election](https://github.com/nylaup/ds4320-project2/blob/main/pipeline/SolutionPipeline.ipynb)

## Domain Exposition 
#### Terminology
| Flipping | A political party winning a seat previously held by the opposition |
| FIPS Code | A unique numeric identifier used to identify US counties and county <br> equivalents |
| Incumbents | The current holder of an office or position |
| Rural-Urban <br> Continuum | Codes given to distinguish US  counties by their degree of urbanization <br> and adjacency to a metro area, according to the USDA |
| Median <br>Income | The middle cutoff where half of the households in an area are earning <br>more and half are earning less |
| Logistic <br> Regression | A machine learning algorithm used for binary classification, predicting <br> one of two outcomes |        
               

#### Project Domain 
This project is in the domain of political science, specifically in electoral modeling. This seeks to understand why voters make the political choices that they do and how these change over time, often in response to changing social and economic conditions. Political science often dives deep into political systems and their operations and behavior in response to different forms of governance. This project applies data science to this domain by trying to predict county vote flipping in an algorithmic way, drawing on demographic and electoral theory of what changes affect voting to create an effective model.         

#### Background Readings
[Folder Link](https://myuva-my.sharepoint.com/:f:/g/personal/mge9dn_virginia_edu/IgCynM8Og8HISp_4b6DqVAsuAVko1N2w9oCttap5TbbRz5Q?e=bBF7a5)         

| Title | Description | Link |
| :--- | :--- | :--- |
| The Politics of the 2018 <br> Midterm Elections | Overview of the 2018 midterm election, from <br> changes expected beforehand to voter <br> outcomes and results | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQCTG-VrYR24ToQUB7pxd5wCAdN65Qv1HzM0Sh8BnzqYmf0?e=XzvnWk) |
| Election Recap 2018:<br> Demographics and <br> Education Levels in <br> Flipped Districts | Article detailing changes seen in districts that <br> flipped in 2018, proposing that a large driver of <br> these changes was immigration and education | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQAnPYv7R5urTIM8AuYrLoeOAev64e1zYCa18iQdJVZSdBs?e=ZoeMIT) |
| Behind the 2018 U.S. <br> Midterm Election <br> Turnout | Highlighting increased voter turnout rates in <br> comparison to the 2014 midterm elections, in <br> part due to the increase in alternative voting | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQBmbkwflW65RLNI7YJtLYk6AUDBoYoCS_vCE7eeViwxRh8?e=esdxiX) |
| Pitfalls of Demographic <br> Forecasts of US <br> Elections | Critique of demographic forecasters for US <br> electoral trends through experiments on <br>elections since 1952 | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQA7bZlFEUS3QKwfnUFORUvkAR3cyF56LQ8ixT2Y_A-rYPU?e=CQchLL) |
| A Bayesian Model for <br> the Prediction of <br>United States <br>Presidential Elections | A study using polling data and election results<br> to explore applications of Bayesian analysis in <br> prediction of election results | [Link](https://myuva-my.sharepoint.com/:b:/g/personal/mge9dn_virginia_edu/IQC7dhg3a4rNTKyhsNQvYnswAc3FRJJert5VSHQsvITthc0?e=5uYFTV) 
                  
                    

## Data Creation 
#### Data Acquisition     
For the election results, I was looking for a dataset that would have the counties for every state with their election results. For this I found a dataset from a github project working to make county-level election results more accessible that scraped election result information from various news sources. In order to get the data I was looking for I used both the 2020 and 2016 election results files and calculated who won the election based on the party percentages and then if the 2020 election result was a county flip or not. In order to get the demographic information I called from the US Census API to get select categories from the American Community Survey. For this I had to sign up with an API key, but the data was returned through these calls.    

#### Creation Code
| File | Description | Link |
| :--- | :--- | :--- |
| Election <br> Results | Results of 2016 and 2020 elections with <br> information on if they flipped | [Link](https://github.com/nylaup/ds4320-project2/blob/main/load/results.py) |
| Demographic <br>Change | Demographic changes from 2016 to 2020 | [Link](https://github.com/nylaup/ds4320-project2/blob/main/load/census.py) |

#### Rationale     
Initially I wanted to run a model on a dataset I had found for demographic details providing the context for the 2018 midterms, however this dataset did not actually have the results of the midterm elections. I realized it was incredibly difficult to access data for the outcome of the midterm election in each county, ensuring it also had FIPS codes. I then decided to look at 2020 and compare it to the prior 2016 election, since it was much easier to find information on these larger election years. I had to decide which demographic columns from the census that I thought changes in might affect the overall election result. I presumed changes in race, income, employment, population, education, and immigration may affect voting, so I pulled these from the census.     

#### Bias Identification      
The bias in the demographic information could emerge from sampling methods. Any data from the census may be biased from nonresponse, as the survey is voluntary, but there may be specific marginalized groups that are less likely to fill it out, and will thus not accurately be represented by any of the information. If we use change in population, this may also be biased towards assuming places with larger populations already are having more significant changes.      

#### Bias Mitigation     
Since the biases with the ACS are inherent to the data, we cannot fix them through any data transformations. However we can be cautious when drawing conclusions from the data and accept that conclusions from minority groups may not be accurately representing all invested parties. We can accept numeric conclusions with a certain margin of error to quantify this bias. We could also weight the results differently for underrepresented groups. For the issue with population changes, instead of using raw population change we can use percent change, so the impact of changes is proportional to the context. With the final model, we can acknowledge the uncertainty these biases may introduce into the outcomes.       

## Metadata 
#### Soft-Schema     
While since it is a NoSQL database there is no enforced schema, each document represents a single county uniquely identified by FIPS code, which is numeric. Each county document will have two nested objects, Elections and Demographics. The election result fields of 2020 and 2016 wins will be categorical strings that have allowed values of "dem" and "gop". The value of Flip will be a boolean indicating whether a county's vote flipped (1) from 2016 to 2020 or not (0). Demographic variables are all numeric values that represent percent change from 2016 to 2020.     

#### Data Summary     
The data will be stored in documents, and each document will represent one county with the identifier being the unique FIPS code. Inside of this county there will be Election, which will have keys of win_2016, win_2020, and flip, and Demographics, which will have various demographic percent changes; white population, median income, poverty, employed population, working age, college education, homeowners, renters, and immigrants.         
{ fips      
  election: { win_2016, win_2020, flip }       
  demographics: { white_pop, med_inc, poverty, employed, working_age, college_pop, homeowner, renter, imm }    
}

#### Data Dictionary 
Elections
| Name | Data Type | Description | Example |      
| :--- | :--- | :--- | :--- |
| FIPS Score | Int | Unique identifier for each county (or equivalent) | 1007 |
| win_2016 | Cat | Party who won 2016 presidential election | dem |
| win_2020 | Cat | Party who won 2020 presidential election | gop |
| Flip | Bool | If county vote flipped from 2016 to 2020 | 0 |        
               
Demographics       
| Name | Data Type | Description | Example |      
| :--- | :--- | :--- | :--- |
| White Population | Float | Percent difference of population identifying<br> as white | -2.44 |
| Med Inc | Float | Percent difference in median household income | 13.1 |
| Poverty | Float | Percent difference in population in poverty | -18.70 |
| Employed | Float | Percent difference in employment | -1.12 |
| Working Age | Float | Percent difference in population that is working age | 6.3 |
| College Population | Float | Percent difference in college educated pop | 18.00 |
| Homeownership | Float | Percent difference in homeownering pop | 4.66 |
| Renters | Float | Percent difference in renting pop | -28.8 |
| Imm Total | Float | Percent difference in immigrant population | -1.21 |       
           

#### Uncertainty 
| Column | Mean | Median | Std Dev | Variance | Min | Max | Range | IQR | Skew | Null % |    
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FIPS Score | 30647 | 29207 | 14984 | 0.0 | 1001 | 56045 | 55044 | 26966 | -0.07 | 0 |
| White Population | -2.14 | -1.91 | 7.24 | 52.46 | 86.79 | 100 | 186.79 | 4.95 | -1.35 | 0 |
| Median Income | -397.90 | 14.93 | 23421.09 | 548547500 | -1328809 | 95 | 1328905 | 10.3 | -56.74 | 0 |
| Poverty | -9.01 | -11.56 | 29.08 | 845.82 | 100 | 1022.22 | 1122.22 | 17.33 | 16.39 | 0 |
| Employed | 2.53 | 2.08 | 11.66 | 135.88 | -40.85 | 490.28 | 531.13 | 8.16 | 23.02 | 0
| Working Age | -0.26 | -0.46 | 11.73 | 137.61 | -71.43 | 266.67 | 338.1 | 7.54 | 7.4 | 0 |
| College Education | 11.87 | 11.23 | 18.94 | 358.65 | -1.00 | 584 | 684 | 15.35 | 9.02 | 0
| Homeownership | 2.97 | 2.89 | 7.56 | 57.16 | -100 | 72.64 | 172.64 | 7.68 | -0.63 | 0 |
| Renters | 0.08 | -0.28 | 17.79 | 316.31 | -88.19 | 477.36 | 565.55 | 14.41 | 7.4 | 0 |
| Immigration | 0.29 | -0.35 | 8.17 | 66.77 | -2.99 | 379.12 | 409.05 | 4.6 | 31.19 | 0 |    



