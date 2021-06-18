states = list(df_mary.drop(["name", "year", "Total"], axis = 1).columns)


#%%
# Add total row
df_mary = df_mary.append(df_mary.sum(numeric_only=True), ignore_index=True).fillna(0)

#%%
# Pivot
df_mary1 = df_mary.pivot(index = "name", columns = states, values = "year").reset_index()
df_mary1

insert = dat_mary1.iloc[[0]]
#%%
df_mary1 = insert.append(df_mary1)
df_mary1.iloc[0] = df_mary1.columns

#%%
def duplicate_header(table):


# %%