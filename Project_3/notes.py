#%%
import datadotworld as dw

import pandas as pd
import altair as alt 
import numpy as np 
#%%
results = dw.query('byuidss/cse-250-baseball-database', 
    'SELECT * FROM batting LIMIT 5')

batting5 = results.dataframe
# %%
q = '''
SELECT *
FROM batting
LIMIT 5
'''

dw.query('byuidss/cse-250-baseball-database', q).dataframe
#%%
q = '''
SELECT playerid, teamid, ab, r
FROM batting
LIMIT 5
'''

dw.query('byuidss/cse-250-baseball-database', q).dataframe
#%%
q = '''
SELECT playerid, teamid, ab, r, ab/r 
FROM batting
LIMIT 5
'''

batting_calc = dw.query('byuidss/cse-250-baseball-database', q).dataframe
#%%
q = '''
SELECT playerid, teamid, ab, r, ab/r as runs_atbat
FROM batting
LIMIT 5
'''

batting_calc = dw.query('byuidss/cse-250-baseball-database', q).dataframe
# %%
# Use the batting table to show the player and his team with his at batts and runs 
#   together with a calculated value of ab / r that is called runs_atbat.
con = 'byuidss/cse-250-baseball-database'

qt = """
SELECT playerid, yearid, r, ab, r / ab as runs_atbat
FROM batting
LIMIT 5
"""

dw.query(con, qt).dataframe
# %%
# For seasons after 1999, which year had the most players 
#   selected as All Stars but didn’t play in the All Star game?

# Provide a summary of how many games, hits, and at bats occurred by those 
#   players had in that years post season.

all_star = """
SELECT yearid, COUNT(*)
FROM AllstarFull 
WHERE gp != 1 
    AND yearid > 1999
GROUP BY yearid 
ORDER BY yearid
"""
dw.query(con, all_star).dataframe
# %%
dw.query(con, 
    'SELECT * FROM battingpost LIMIT 5').dataframe

# %%

all_star = """
-- Not sure if correct -- 
SELECT 
    bp.yearid,
    bp.playerid, 
    SUM(bp.g) as games,
    SUM(bp.h) as hits,
    SUM(bp.ab) as atbats
FROM battingpost as bp 
    JOIN AllstarFull as asf
    ON bp.playerid = asf.playerid
        AND bp.yearid = asf.yearid
WHERE asf.gp != 1 
    AND asf.yearid > 1999
GROUP BY asf.yearid 
ORDER BY asf.yearid
"""
dw.query(con, all_star).dataframe
# %%
#----NOTES 6/3/21----#
import pandas as pd 
import altair as alt
import numpy as np
import sqlite3

# %%
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)
# %%
# See the tables in the database
table = pd.read_sql_query(
    "SELECT * FROM sqlite_master WHERE type='table'",
    con)
print(table.filter(['name']))
print('\n\n')
# 8 is collegeplaying
print(table.sql[8])
# %%
### DONT USE BAR CHARTS