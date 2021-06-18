#%%
# Import Libraries
import datadotworld as dw
import pandas as pd
import altair as alt 
import numpy as np 
import sklearn as sk    
import seaborn as sns

#%%
# the from imports
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics

from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier

#%%
# URL Links to Data Set
dwellings_denver_url = "https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_denver/dwellings_denver.csv"
dwellings_ml_url = "https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_ml/dwellings_ml.csv"
dwellings_neighborhoods_ml_url = "https://github.com/byuidatascience/data4dwellings/raw/master/data-raw/dwellings_neighborhoods_ml/dwellings_neighborhoods_ml.csv"

# Data Frames
dwellings_denver = pd.read_csv(dwellings_denver_url)
dwellings_ml = pd.read_csv(dwellings_ml_url) # THIS IS THE CLEANED UP DATA, USE THIS
dwellings_neighborhoods_ml = pd.read_csv(dwellings_neighborhoods_ml_url)

alt.data_transformers.enable('json')

# %%
# CODE FROM JUNE 10 2021
# DO NOT PUT THIS IN PROJECT
h_subset = dwellings_ml.filter(['livearea', 'finbsmnt', 
    'basement', 'yearbuilt', 'nocars', 'numbdrm', 'numbaths', 
    'stories', 'yrbuilt', 'before1980']).sample(500)

#sns.pairplot(h_subset, hue = 'before1980')

corr = h_subset.drop(columns = 'before1980').corr()
# %%
# CODE FROM JUNE 10 2021
sns.heatmap(corr)

#%%
# GRAND QUESTION 1
# Year Built & Number of Baths
chart1 = (alt.Chart(dwellings_ml)
    .encode(
        x = alt.X('yrbuilt', axis=alt.Axis(format='.0f'), scale=alt.Scale(zero=False)), 
        y = alt.Y('numbaths', scale=alt.Scale(zero=False)), 
        # The O changes the chart index to 0 and 1
        color = 'before1980:O' 
        ) 
    .mark_circle()
)

# Year Built and Number of baths line 
# USE THIS
chart2 = (alt.Chart(dwellings_ml)
    .encode(
        x = alt.X('yrbuilt', axis=alt.Axis(format='.0f'), scale=alt.Scale(zero=False)), 
        y = alt.Y('numbaths', scale=alt.Scale(zero=False)), 
        # The O changes the chart index to 0 and 1
        color = 'before1980:O' 
        ) 
    .transform_loess("yrbuilt", "numbaths")
    .mark_line()
    # ADD line at 1980
)

chart1
chart2
#%%
# Year Built and Stories
(alt.Chart(dwellings_ml)
    .encode(
        x = alt.X('yrbuilt', axis=alt.Axis(format='.0f'), scale=alt.Scale(zero=False)), 
        y = alt.Y('stories', scale=alt.Scale(zero=False)), 
        # The O changes the chart index to 0 and 1
        color = 'before1980:O' 
        ) 
    .mark_circle()
)


#%%
# Year Built and Live Area
(alt.Chart(dwellings_ml)
    .encode(
        x = alt.X('yrbuilt', axis=alt.Axis(format='.0f'), scale=alt.Scale(zero=False)), 
        y = alt.Y('livearea', scale=alt.Scale(zero=False)), 
        # The O changes the chart index to 0 and 1
        color = 'before1980:O' 
        ) 
    .mark_circle()
)

#%%
# Year Built and basement
(alt.Chart(dwellings_ml)
    .encode(
        x = alt.X('yrbuilt', axis=alt.Axis(format='.0f'), scale=alt.Scale(zero=False)), 
        y = alt.Y('basement', scale=alt.Scale(zero=False)), 
        # The O changes the chart index to 0 and 1
        color = 'before1980:O' 
        ) 
    .mark_circle()
)
#%%
# What is a classification model?

# GRAND QUESTION 3
# Read Feature
# https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html

# GRAND QUESTION 4
# Read ROC.curve
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html

















# %%
# Trying to get the count of the 
dat_count = (dwellings_ml
    .groupby(['yrbuilt', 'numbaths'])
    .agg(count = ('nocars', 'size'))
    .reset_index()
)
#%%















# %%
# not quite working yet
(alt.Chart(dat_count)
    .encode(
        alt.X('yrbuilt:O',
            scale = alt.Scale(zero=False),
            axis=alt.Axis(format='.0f')), 
        alt.Y('numbaths:O',scale = alt.Scale(zero=False)), 
        color = alt.Color('count', 
            scale=alt.Scale(type='log')))
    .mark_rect()
    .properties(width=400)
)
# %%
(alt.Chart(dat_count)
    .encode(
        alt.X('yrbuilt:O',
            scale = alt.Scale(zero=False),
            axis=alt.Axis(format='.0f')), 
        alt.Y('numbaths',scale = alt.Scale(zero=False)))
    .mark_boxplot(size = 3)
    .properties(width=650)
)
# %%
base = (alt.Chart(dwellings_ml)
    .encode(
    alt.X('yrbuilt', bin=alt.Bin(step = 1),
        axis=alt.Axis(format='.0f')),
    alt.Y('numbaths', bin=alt.Bin(step=1)),
        color=alt.Color('count()', 
            scale=alt.Scale(type='log')))
)
base.mark_rect() 
# %%
base = (alt.Chart(dwellings_ml)
    .encode(
    alt.X('yrbuilt', bin=alt.Bin(step = 5),
        axis=alt.Axis(format='.0f')),
    alt.Y('numbaths', bin=alt.Bin(step=1)),
        color=alt.Color('count()', 
            scale=alt.Scale(type='log')))
)
base.mark_rect() 

#%%






















# %%
# GRAND QUESTION 4
# CODE from JUNE 10 2021 "What does the train_test_split() function do?"
X_pred = dwellings_ml.drop(['yrbuilt', 'before1980'], axis = 1) # Capital is used for metrix, You want to run this and make sure there are no 'yrbuilt' and 'before1980'
y_pred = dwellings_ml.before1980 # Lower case is used for series. This is what we are trying to predict

X_train, X_test, y_train, y_test = train_test_split(
    X_pred, 
    y_pred, 
    test_size = .34, # These need to be smaller than the train size
    random_state = 76)  

    # USE these in terminal
    # X_train
    # y_train.size
    # y_test.size
    # y_pred.size
    # y_test.size / y_pred.size

#%%
# Decision Tree 
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
predict_p = clf.predict(X_test)
# %%
# This is a fusion matrix chart
print(metrics.confusion_matrix(y_test, predict_p)) # This puts the 0's and 1's in their quadrants (Boy who cried wolf -Google Example-)
metrics.plot_confusion_matrix(clf, X_test, y_test)
# Go to sklearn metrics
# %%
print(metrics.classification_report(y_test, predict_p))

# shows me the accuracy score
clf.score(X_test, y_test)

#%%








#%%
# Decision Tree Regression
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X_test, y_test)
clf.predict(X_test)

#%%
# Not very helpful
#tree.plot_tree(clf)

#%%











#%%
# GRADIENT TREE
clf = GradientBoostingClassifier()
clf = clf.fit(X_train, y_train)
predict_p = clf.predict(X_test)
# %%
# This is a fusion matrix chart
print(metrics.confusion_matrix(y_test, predict_p)) # This puts the 0's and 1's in their quadrants (Boy who cried wolf -Google Example-)
metrics.plot_confusion_matrix(clf, X_test, y_test)
# Go to sklearn metrics
# %%
print(metrics.classification_report(y_test, predict_p))

# shows me the accuracy score
clf.score(X_test, y_test)




# %%
# Enter into terminal clf.feature_importances_
df_features = pd.DataFrame(
    {'f_names': X_train.columns, 
    'f_values': clf.feature_importances_}).sort_values('f_values', ascending = False)


# %%
