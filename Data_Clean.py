#imports
import pandas as pd

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

#function to merge the players and award data to create a single dataframe saved in a csv file
def player_award_merge(type,awards):
  
  #reads the appropriate award csv
  award = pd.read_csv("csv/"+type+"/"+awards+".csv")

  #variables to store subsets of columns that will be used depending on award
  perm = ["Player", "Year"]
  pts = ["Pts Won", "Pts Max", "Share"]
  ws = ["WS", "WS/48"]
  defense = ["DWS","DBPM","DRtg"]

  #columns to keep for every award
  toKeep = perm + pts + ws
  
  #columns to keep for defensive awards
  if awards == "DPOY" or awards == "ALL-DEF":
      toKeep = toKeep + defense

  #keeps only the selected subset of columns in the dataframe
  award = award[toKeep]
    
  #reads the players csv file and cleans it up
  players = pd.read_csv("csv\data\Players.csv")
  del players["Unnamed: 0"]
  del players["Rk"]
  del players["Awards"]
  players["Player"] = players["Player"].str.replace("*", "", regex=False)

  #groups players by name and year and also applies the single_row function
  players = players.groupby(perm).apply(single_row)

  #drops 2 unneeded index levels 
  players.index = players.index.droplevel()
  players.index = players.index.droplevel()

  #combines the players and mvp dataframes and fills listed NA columns with 0
  combined = players.merge(award, how="outer", on=perm)
  
  #fills any values with NA with a 0
  combined[pts] = combined[pts].fillna(0)

  standings = pd.read_csv("csv/data/Standings.csv")

  #replaces * in any of the team names
  standings["Team"] = standings["Team"].str.replace("*", "", regex=False)

  #creates an empty dictionary
  nickname = {}

  #reads the nicknames file and maps abbreviations to the team name
  #This is because the Players csv uses the full name but the awards csv uses abbreviation
  with open("nicknames.txt", encoding="utf-8") as f:
      lines = f.readlines()
      for line in lines[1:]:
          abbrev, name = line.replace("\n", "").split(",")
          nickname[abbrev] = name


  #maps the team name onto the combined dataframe
  combined["Team"] = combined["Team"].map(nickname)

  #outer merges standings dataframe and combined on Team and Year columns
  stats = combined.merge(standings, how="outer", on=["Team", "Year"])

  #Cleans up the data to prevent issues
  del stats["Unnamed: 0"]
  stats["GB"] = stats["GB"].str.replace("—", "0")
  stats = stats.apply(pd.to_numeric, errors = "ignore")
  
  #write the stats dataframe to the appropriate csv file
  stats.to_csv("csv/merged_stats/player_"+awards+"_stats.csv")

  

