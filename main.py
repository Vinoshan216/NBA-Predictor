from Parse_Scrape import scraper, parser
from Data_Clean import player_award_merge
from Machine_Learning import input_data, backtest, find_avg_precision, write_stats
import os, pandas as pd
from sklearn.linear_model import Ridge





def create_folder(path):
  try:
    os.mkdir(path)
  except FileExistsError:
    print(f"Directory '{path}' already exists.")
  except PermissionError:
      print(f"Permission denied: Unable to create '{path}'.")
  except Exception as e:
      print(f"An error occurred: {e}") 

"""
WARNING

Only run Scrape, Parse, and Clean once each, as there will be various errors that occur, including but 
not limited to: web page time out for making too many requests, creating files that already exist or 
overwriting large files. For View, it will show the 
"""


#Scrape
def scrape():
  #array to hold values for scraper:
  #[url, html_folder_name]
  scraper_values = [
    ["https://www.basketball-reference.com/leagues/NBA_{}_per_game.html", "all_players"],
    ["https://www.basketball-reference.com/awards/awards_{}.html", "awards"],
    ["https://www.basketball-reference.com/leagues/NBA_{}_standings.html", "standings"]
  ]

  #creates a folder and calls scraper for each scraper value
  for i in range(len(scraper_values)):
    create_folder(scraper_values[i][1])
    scraper(scraper_values[i][0], scraper_values[i][1])

#Parse
def parse():
  #values for parser
  #[html_folder_name, tag, class_remove, table, file_name, csv_folder]
  parser_values = [
    ["all_players", 'tr', ["thead","norank"], ["per_game_stats"], ["Players"],"data"],
    ["awards", 'tr', ["thead", "over_header"], ["leading_all_nba", "leading_all_defense", "leading_all_rookie"], ["ALL-NBA", "ALL-DEF", "ALL-ROOK"], "team_awards"],
    ["standings", 'tr', ["thead"], ["divs_standings_E"], ["Standings"],"data"],
    ["awards", 'tr', ["over_header"], ["mvp", "roy","dpoy", "smoy", "mip"], ["MVP", "ROY", "DPOY", "6MOY", "MIP"],"individual_awards"]
  ]

  #creates csv folder
  create_folder("csv")

  #creates subfolder in csv to hold each parsed dataframe's csv
  for i in range(len(parser_values)):
      create_folder("csv/"+parser_values[i][5])
      parser(parser_values[i][0],parser_values[i][1], parser_values[i][2], parser_values[i][3], parser_values[i][4], parser_values[i][5])


#Clean
def clean():
  merge_values = [
      ["team_awards","ALL-NBA"],
      ["team_awards","ALL-ROOK"],
      ["team_awards","ALL-DEF"],
      ["individual_awards","MVP"],
      ["individual_awards","DPOY"],
      ["individual_awards","6MOY"],
      ["individual_awards","MIP"],
      ["individual_awards","ROY"]
  ]

  for i in range(len(merge_values)):
    create_folder("csv/"+merge_values[i][0])
    player_award_merge(merge_values[i][0], merge_values[i][1])


#Predict
def predict():
  #name of folder to save data
  version = "All_Data_Precision_Stats_1.0"
  #list of awards
  awards = ["MVP", "ROY", "DPOY", "6MOY", "MIP","ALL-NBA", "ALL-DEF", "ALL-ROOK"]
  #creates folder, and opens txt file to hold cumulative data
  create_folder(version)
  f2 = open(version+"/Cumulative.txt", "w")

  #for each award, creates a subfolder to hold data
  #writes stats to txt and csv files
  for award in awards:
    create_folder(version+"/"+award)
    write_stats(version, award, f2)



#View
def view(award, year):
  
  year = [year]
  #reads csv file
  df = pd.read_csv("All_Data_Precision_Stats_1.0/"+award+"/Dataframe.csv")

  #filters the data to specified year
  mask = df["Year"].isin(year)
  year_data = df[mask]
  
  #prints top 10
  print(year_data.head(10))


#Call as follows: view("award", year)
#view("MVP", 2024)
