#%%
import datadotworld as dw
import pandas as pd
import altair as alt 
import numpy as np 
#%%
results_s = dw.query('byuidss/cse-250-baseball-database', 
    'SELECT * FROM Salaries')

results_cp = dw.query('byuidss/cse-250-baseball-database', 
    'SELECT * FROM CollegePlaying')

salaries = results_s.dataframe
college_playing = results_cp.dataframe
#%%
#----------GRAND QUESTION 1----------#

### USE CollegePlaying and Salaries
q = '''
SELECT 
    s.yearid,
    s.teamid, 
    s.playerid, 
    cp.schoolid, 
    s.salary
FROM Salaries as s
    JOIN CollegePlaying as cp
    ON s.playerid = cp.playerid 
WHERE
    cp.schoolid = 'idbyuid'
GROUP BY
    s.salary
ORDER BY 
    s.salary DESC
'''

# Is byui labeled as idbyuid? 
# How do I get rid of the duplicates?

results_cp_s = dw.query('byuidss/cse-250-baseball-database', q).dataframe
results_cp_s

#%%
# Print for markdown
print(results_cp_s.to_markdown())
# %%
#----------GRAND QUESTION 2----------#
### PART 1
w = '''
SELECT
    yearid,
    playerid,
    h as hits,
    ab as at_bats,
    ROUND(h / ab, 3) as at_bats_average
FROM Batting 
WHERE
    h >= 1
ORDER BY
    at_bats_average DESC
LIMIT 5
'''
results_at_bats_avg = dw.query('byuidss/cse-250-baseball-database', w).dataframe
results_at_bats_avg

#%%
# Print for markdown
print(results_at_bats_avg.to_markdown())
# %%
### PART 2
e = '''
SELECT
    yearid,
    playerid,
    h as hits,
    ab as at_bats,
    ROUND(h / ab, 3) as at_bats_average
FROM Batting 
WHERE
    ab >= 10
ORDER BY
    at_bats_average DESC
LIMIT 5
'''
results_at_bats_avg_1 = dw.query('byuidss/cse-250-baseball-database', e).dataframe
results_at_bats_avg_1

#%%
# Print for markdown
print(results_at_bats_avg_1.to_markdown())
# %%
### PART 3
# WHERE
#   at_bats > 100
r = '''
SELECT
    COUNT(yearid) as years_played,
    playerid,
    SUM(h) as hits,
    SUM(ab) as at_bats,
    ROUND(h / ab, 3) as at_bats_average
FROM Batting  
GROUP BY 
    playerid
HAVING
    at_bats > 100
ORDER BY
    at_bats_average DESC
LIMIT 5
'''
results_at_bats_avg_2 = dw.query('byuidss/cse-250-baseball-database', r).dataframe
results_at_bats_avg_2

#%%
# Print for markdown
print(results_at_bats_avg_2.to_markdown())

# %%
### PART 3.1
# I want to see people who played in the 2000s and above.
#   
r = '''
SELECT
    COUNT(yearid) as years_played,
    playerid,
    SUM(h) as hits,
    SUM(ab) as at_bats,
    ROUND(h / ab, 3) as at_bats_average
FROM Batting 
WHERE
    h >= 100 AND
    yearid >= 2000 AND
    yearid >= 5
GROUP BY playerid
ORDER BY
    at_bats_average DESC
LIMIT 5
'''
results_at_bats_avg_2 = dw.query('byuidss/cse-250-baseball-database', r).dataframe
results_at_bats_avg_2
# %%
#----------GRAND QUESTION 3----------#
# PITCHING POST CUBS vs CLE
t = '''
SELECT
    yearid,
    round as world_series,
    teamid,
    playerid,
    G as games_played,
    SO as strikeouts,
    BAOpp as opp_batting_avg,
    HBP as batters_hit,
    R as runs_allowed
FROM PitchingPost
WHERE 
    round = "WS" AND
    yearid = 2016
ORDER BY
    teamid ASC
'''
results_pitching_post = dw.query('byuidss/cse-250-baseball-database', t).dataframe
results_pitching_post

#%%
# Batting regular season
# 1.) Sort them through NL and AL
# I want to understand how I can get the team total batting average.
u = '''
SELECT
    yearID,
    teamID,
    lgID as division,
    playerID,
    R as runs,
    H as hits,
    AB as at_bats,
    ROUND(h / ab, 3) as batting_average,
    RBI,
    SO as strikeouts
FROM Batting
WHERE 
    (AB >= 250 AND
    yearid = 2016) AND
    (teamID = "CHN" OR teamID = "CLE")
ORDER BY
    teamid ASC,
    batting_average DESC
'''

# FOR chart use mark_circle (for the other teams) + mark_line (for the Chicago Cubs that will be a horizontal line.)
results_batting_reg = dw.query('byuidss/cse-250-baseball-database', u).dataframe
results_batting_reg

#%%
round(results_batting_reg.query("teamID == 'CHN'")["batting_average"].mean(), 3)

round(results_batting_reg.query("teamID == 'CLE'")["batting_average"].mean(), 3)

#%%
# Filtering down the data to make a box plot
results_chn = (results_batting_reg.query("teamID == 'CHN'"))
results_cle = (results_batting_reg.query("teamID == 'CLE'"))
#%%
# Chart CLE batting average
chart_batting_cle_chn = (alt.Chart(results_batting_reg
)
    .encode(
        x = alt.X("teamID", title = "Team"),
        y = alt.Y("batting_average", title = "Batting Average"),
        )
    .mark_boxplot()
    .properties(title = "Batting (Regular Season)",
    width = 250
    )
)
chart_batting_cle_chn.save("chartbattingclechn.png")
chart_batting_cle_chn

# %%
# Batting POST CUBS vs CLE
y = '''
SELECT
    yearid,
    round as world_series,
    teamid,
    playerid,
    h as hits,
    ab as at_bats,
    ROUND(h / ab, 3) as batting_average,
    RBI,
    SO as strikeouts
FROM BattingPost
WHERE 
    (round = "WS" AND
    yearid = 2016) AND
    ab >= 5
ORDER BY
    teamid ASC,
    batting_average DESC
'''
results_batting_post = dw.query('byuidss/cse-250-baseball-database', y).dataframe
results_batting_post

#%%
# Chart CLE batting average
chart_batting_cle_chn_post = (alt.Chart(results_batting_post)
    .encode(
        x = alt.X("teamid", title = "Team"),
        y = alt.Y("batting_average", title = "Batting Average"),
        )
    .mark_boxplot()
    .properties(title = "Batting (World Series)",
    width = 250
    )
)
chart_batting_cle_chn_post.save("chartbattingclechnpost.png")
chart_batting_cle_chn_post
#%%


















#%%
# Chart BattingPost
chart_batting_post = (alt.Chart(results_batting_post)
    .encode(
        #x = alt.X("year", scale=alt.Scale(domain=[2004, 2016]), axis=alt.Axis(format='.0f')),
        x = "teamid",
        y = alt.Y("strikeouts_total"),
        color = "teamid"
        )
    .mark_bar()
    .properties(title = "World Series Strikeouts")
)
chart_batting_post.save("chartbattingpost.png")
chart_batting_post

#%%
# SORT the values, and replace NaN values with 0
results_batting_post = results_batting_post.sort_values("batting_average", ascending=False)

results_batting_post.batting_average = results_batting_post.batting_average.replace("NaN").fillna(method = "ffill")
#%%
# Total Strikeouts per team
results_batting_post_1 = results_batting_post.groupby("teamid").agg(
    strikeouts_total = ("strikeouts", "sum") #would I use mean?
).reset_index()