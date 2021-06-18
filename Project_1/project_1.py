#%%
# Load the libraries
import pandas as pd 
import numpy as np 
import altair as alt 

# %%
# Load the Data
names_year_url = "https://github.com/byuidatascience/data4names/raw/master/data-raw/names_year/names_year.csv"
df = pd.read_csv(names_year_url)

# %%
# See the what columns and objects are available
##### What I see is only "name", "year", "state names" and "Total"
df.columns

#%%
# How many unique names in our data
pd.unique(df.name).size

#%%
# Shows unique years assisgned to John
oliver = df.query('name == "Oliver"').year.size


#%%
# Which names have been given the most and the least?
names_year_1 = (df.groupby(["name"])
    .agg(Total_all = ("Total", np.sum),
        Average_all = ("Total", np.mean))
    .reset_index()
    )

names_year_1.sort_values("Total_all").head(1).name
names_year_1.sort_values("Total_all").tail(1).name
#%%
names_state_1 = (df.groupby(["name"])
    .agg(Total_all = ("UT", np.sum),
        Average_all = ("UT", np.mean))
    .reset_index()
    .query("Total_all > 0")
    .sort_values("Total_all")
)

print(names_state_1.head(1).name)
names_state_1.tail(1).name

#%%
(alt.Chart(names_state_1.tail(25))
    .encode(
        x = alt.X("name", sort = "-y"),
        y = "Total_all"
    )
    .mark_bar()
)
# %%
#----------------------------------------------------------------------------------------
#### GRAND QUESTION 1
# Another creation of the data set to narrow results

# My question is how do I select specific multiple items in a column?
birth_year = df[["name", "year", "Total"]]

#%%
df_spencer = birth_year.loc[birth_year["name"] == "Spencer"]

df_spencer

#%%
df_spencer = birth_year.query('name == "Felisha"').nsmallest
df_spencer
#%%
chart_line = (alt.Chart(df_spencer)
    .encode(
        x = alt.X("year", axis=alt.Axis(format='.0f')),
        y = alt.Y("Total", scale=alt.Scale(domain=[0, 5000])),
        color = "name"
        )
    .mark_line()
)
chart_line
# %%
#----------------------------------------------------------------------------------------
#### GRAND QUESTION 2

# Data set for brittany
df_brittany = birth_year.loc[birth_year["name"] == "Brittany"]
df_brittany_2 = df.loc[birth_year["name"] == "Brittany"]

#df_brittany
#df_brittany_2

# %%
# Chart for Brittany
chart_line_brit = (alt.Chart(df_brittany)
    .encode(
        x = alt.X("year", axis=alt.Axis(format='.0f')),
        y = alt.Y("Total", scale=alt.Scale(domain=[0, 35000])),
        color = "name"
        )
    .mark_line()
)
chart_line_brit
chart_line_brit.save("chart_brit.png")
#----------------------------------------------------------------------------------------
#%%
#----------------------------------------------------------------------------------------
#### GRAND QUESTION 3
# Data set for Mary, Martha, Peter, and Paul
# I get error "Too many indexers"
# Data Set for only Mary
df_mary = df.query('name == "Mary"')
df_mary

df_more_names = birth_year.query('name == "Mary" | name == "Martha" | name == "Peter" | name== "Paul"')
df_more_names

# %%
chart_line_names = (alt.Chart(df_more_names)
    .encode(
        x = alt.X("year", axis=alt.Axis(format='.0f')),
        y = alt.Y("Total", scale=alt.Scale(domain=[0, 60000])),
        color = "name"
        )
    .mark_line()
)
chart_line_names
chart_line_names.save("chart_names.png")
#----------------------------------------------------------------------------------------
# %%
#----------------------------------------------------------------------------------------
#### GRAND QUESTION 4
# Would I use filter, loc, or query?
df_max_2000 = birth_year.query('year >= 2000')
#df_max_2000 = birth_year.loc[birth_year["year"] >= 2000]

df_max_1990 = birth_year.query('year >= 1990 and year <= 2005')

# %%
# Finding the largest total value in the year 2000 and above
# I want to get rid of duplicates also
df_max_2000.nlargest(100, "Total").drop_duplicates("name")
# %%
# Look for a specific name from the years 2000 and above. 
df_max_2000.query('name == "Marshall"').nlargest(16, "Total")
# %%
# Avengers (2012) Cast
avengers = (df_max_2000.query('name == "Scarlett"')
    .nlargest(5000, "Total")
)

# Avengers chart
chart_line_avengers = (alt.Chart(avengers)
    .encode(
        x = alt.X("year", axis=alt.Axis(format='.0f')),
        y = alt.Y("Total", scale=alt.Scale(domain=[0, 10000])),
        color = "name"
        )
    .mark_line()
)
chart_line_avengers
chart_line_avengers.save("avengers.png")
# %%
# Backstreet Boys

# Filter out the specific members of the group
backstreet = (df_max_1990.query('name == "Howard" | name == "Nickolas" | name == "Howie" | name == "Brian" | name == "Alex" | name == "Kevin"')
    .nlargest(1000, "Total")
)

# Backstreet Boys chart
chart_line_bb = (alt.Chart(backstreet)
    .encode(
        x = alt.X("year", axis=alt.Axis(format='.0f')),
        y = alt.Y("Total", scale=alt.Scale(domain=[0, 22000])),
        color = "name"
        )
    .mark_line()
)
chart_line_bb
chart_line_bb.save("backstreet_boys.png")