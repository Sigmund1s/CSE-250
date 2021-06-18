#%%
# Import libraries
import pandas as pd 
import altair as alt 
import numpy as np 

#%%
#-----NOTES 5/11/2021-----#
# internal packages
import urllib3 
import json

url = "https://github.com/byuidatascience/data4missing/raw/master/data-raw/mtcars_missing/mtcars_missing.json"

# %%
http = urllib3.PoolManager()
response = http.request('GET', url)
cars_json = json.loads(response.data.decode('utf-8'))

# %%
cars = pd.json_normalize(cars_json) # handles nested jsons.

#%%
# Example
data = [{'id': 1,
         'name': "Cole Volk",
         'fitness': {'height': 130, 'weight': 60}},
        {'name': "Mose Reg",
         'fitness': {'height': 130, 'weight': 60}},
        {'id': 2, 'name': 'Faye Raker',
         'fitness': {'height': 130, 'weight': 60}}]
pd.json_normalize(data, max_level=0)
# %%
# Missing data examples
df = (pd.DataFrame(
    np.random.randn(5, 3), 
    index=['a', 'c', 'e', 'f', 'h'],
    columns=['one', 'two', 'three'])
  .assign(
    four = 'bar', 
    five = lambda x: x.one > 0,
    six = [np.nan, np.nan, 2, 2, 1],
    seven = [4, 5, 5, np.nan, np.nan])
  )

#%%
# What happens when you add two pandas objects with missing values?
df.seven + df.six

df.seven.fillna(0) + df.six.fillna(0)
# %%
# What happens when you sum within a column
df.seven.sum()

# %%
#-----NOTES 5/13/2021-----#
pd.crosstab(flights)



# %%
#-----NOTES 5/20/2021-----#

