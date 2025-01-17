#imports
import pandas as pd
import matplotlib.pyplot as plt

#function to merge rows for players who played for multiple teams in one season
def single_row(df):
    #list of possible team names depending on # of teams played for
    non_teams = ["2TM", "3TM", "4TM", "5TM"]

    #do nothing if only one team
    if df.shape[0] == 1:
        return df
    else:  
        #gets the rows where team name is in list above and sets it to the last team player played for in that season
        row = df[df["Team"].isin(non_teams)]
        row["Team"] = df.iloc[-1,:]["Team"]
        return row


#reads the mvp csv file and only looks at the listed columns
mvps = pd.read_csv("csv\individual_awards\MVP.csv")

mvps = mvps[["Player", "Year", "Pts Won", "Pts Max", "Share"]]


#reads the players csv file and cleans it up
players = pd.read_csv("csv\data\Players.csv")
del players["Unnamed: 0"]
del players["Rk"]
del players["Awards"]
players["Player"] = players["Player"].str.replace("*", "", regex=False)




#groups players by name and year and also applies the single_row function
players = players.groupby(["Player", "Year"]).apply(single_row)

#drops 2 unneeded index levels 
players.index = players.index.droplevel()
players.index = players.index.droplevel()

#combines the players and mvp dataframes and fills listed NA columns with 0
combined = players.merge(mvps, how="outer", on=["Player", "Year"])
combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)


standings = pd.read_csv("csv/data/Standings.csv")

standings["Team"] = standings["Team"].str.replace("*", "", regex=False)

nickname = {}

with open("nicknames.txt", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev, name = line.replace("\n", "").split(",")
        nickname[abbrev] = name

combined["Team"] = combined["Team"].map(nickname)

stats = combined.merge(standings, how="outer", on=["Team", "Year"])

del stats["Unnamed: 0"]

stats["GB"] = stats["GB"].str.replace("—", "0")
stats = stats.apply(pd.to_numeric, errors = "ignore")

print(stats.head(10))

"""
stats.to_csv("player_mvp_stats.csv")

stats.corr(numeric_only = True)["Share"].plot.bar()

plt.show()




highest_scoring_byplayers = stats[stats["G"] > 70].sort_values("PTS", ascending=False).head(10)

highest_scoring_byYear = stats[stats["G"] > 60].groupby("Year").apply(lambda x: x.sort_values("PTS", ascending=False).head(1))

highest_scoring_byYear.plot.bar("Year","PTS")

plt.show()

"""

