# How big of a margin? Predicting county vote margins in future presidential elections

## Past election results found more significant in predicting county vote margins than demographic percent changes when used to predict for the 2020 election 

## Problem Statement        
Currently, there are many different methods used to predict election outcomes, many centering around forecasters who draw on their own experiences and trends they have been observing in order to state what they think the outcome will be, which have varying levels of success. Many election predictions focus on party wins, although voter margins are also integral to studying political patterns. Party wins only provides a narrow view of who won, which will group clear Republican wins in the same category of counties that had a very slim Republican win, while voter margins provides a much more nuanced study, for the more complex issue of elections. Not many predictions focus solely on changes, which often are what create unexpected results, so this model uses demographic changes to aid in its prediction. 


## Solution Description      
In order to generate a useful tool for predicting elections, I decided to use a Regression machine learning model to predict the voter margins of a county. This model uses presidential election results, as well as other information on demographic and economic changes, to learn how to be able to predict the voter share margin for counties in the 2020 election. It will then apply this learned relationship to given information about counties leading up to the 2024 election to then predict party margins from the way they voted in the last presidential election and demographic changes since then. This project aims to create an analytical and predictive model that uses objective historical demographics and doesn't rely on the opinions of a political analyst. The specific goal is predicting election margins, which do not only focus on which party won but by how much and the percent difference in voters for the two parties. 

## Chart 

![Feature Importances](images/feature_importances.png)

The model shows which features are the most important, revealing that historical voting patterns vastly trump any demographic changes, and these models do not really weigh these demographic changes very significantly. Out of these demographic changes, it seems that the most impactful were percent changes in total population and senior population. 

![Massachusetts Prediction](images/mass_predictions.png)

This chart shows a map created using this database and random forest model, predicting election margins for counties in Massachusetts. We can see that based on historical election results and recent demographic changes, there are different predicted margins. Election forecasters can use this when creating their predictions for upcoming elections, in addition to candidates can also see which counties are predicted to have slim margins and may require more campaigning efforts. 
