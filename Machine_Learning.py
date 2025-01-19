import pandas as pd
from sklearn.linear_model import Ridge


"""
Use:

function to select which award to input and which predictor categories to use

Input:

award - Award to read csv file from (String)

Returns:

stats - dataframe holding stats for the input award (Dataframe)
predictors - list of stats to use for predictions (string list)
"""

def input_data (award):
  #reads the csv file
  stats = pd.read_csv("csv/merged_stats/player_"+award+"_stats.csv")

  #cleans up the dataframe
  del stats["Unnamed: 0"]
  stats = stats.fillna(0)

  def_predictors = ["DWS","DBPM","DRtg"]
  
      
  #list of columns that will be used as contributors to the predictor
  predictors = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
        '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
        'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year',
        'WS', 'WS/48', 'W', 'L', 'W/L%', 'GB',
        'PS/G', 'PA/G', 'SRS']
  
  if award == "DPOY" or award == "ALL-DEF": predictors = predictors+def_predictors

  return stats, predictors


"""
function to check accuracy of predicted vs actual data. This function gets the top 
5 names with highest value in Share column (actual) and then all the values from the 
Predictions column (predicted). It then iterates through the predicted column to see 
if the actual top 5 were predicted. If one of the actual top 5 is predicted, it adds a
score of 1 to the found counter. It then checks how many iterations it took to get to
that name, which is represented by the seen counter. The score that gets appended to the
score array is the found counter divided by how many iterations it took to find that player.
This means that if 1st predicted player is in "actual" on the first iteration, then the 
appended score would be 1, but if the next predicted player isn't found until the 5 iteration,
then the appended score would 2/5 or 0.4. The functions return is the mean of the score array,
which represents the aggregate average precision metric for the predictions

TLDR: Accuracy of predicting Top by by sorting Top 5 players by Share rank, ordered by Predicted rank, 
remove all players not in Top 5. Score is rank they appear in divided by Prediction Rank. 
Returns mean of Top 5's score
"""
"""

Use:

function find average precision of input dataframe

Input:

combination - dataframe of combined dataframes

Returns:

mean_score - mean of score for predicted ranks (float)
"""

def find_avg_precision(combination):

  #gets the top 5 names with highest value in Share column, from first to last
  actual = combination.sort_values("Share", ascending=False).head(5)

  #gets the names with highest value in Predictions column, from first to last
  predicted = combination.sort_values("Predictions", ascending=False)

  #array to hold 
  score=[]
  found = 0
  seen = 1

  """
  for each player in the "Predicted" dataframe, if the player is in the "Actual" dataframe,
  it increments the found counter and then adds the ratio of how long it to took to find the player (found) compared how many 
  iterations the loop has been through (seen). It then adds this ratio to the "score" array.
  """
  for index, row in predicted.iterrows():
    if row["Player"] in actual["Player"].values:
      found += 1
      score.append(found/seen)
    seen += 1

  mean_score = sum(score) / len(score)
  #returns the mean of the values in score
  return mean_score



"""
Use:

function to add ranks into the combinaton dataframe for diagnostics. Adds a column
for Share Rank and Predicted Rank, and another column to show the difference between
the two

Input:

combination - dataframe of combined dataframes

Returns:

combination - dataframe of combined dataframes with new columns
"""

def add_ranks(combination):
  combination = combination.sort_values("Share", ascending=False)
  combination["Actual_Rk"] = list(range(1, combination.shape[0]+1))

  combination = combination.sort_values("Predictions", ascending=False)
  combination["Predicted_Rk"] = list(range(1, combination.shape[0]+1))

  combination["Diff"] = combination["Actual_Rk"] - combination["Predicted_Rk"]

  return combination


"""
Use:

function to predict and create data

Input:

stats - dataframe holding stats for the input award (Dataframe)
model - Regression model (Ridge)
years - list of years (int list)
predictors - list of stats to use for predictions (string list)

Returns:

mean_score - mean of avg_precision_sum (float)
avg_precision_sum - average precision sum for each year of award (float list)
pd.concat(all_predictions) - dataframe holding all data for award (Dataframe)
""" 
def backtest(stats, model, years, predictors):
  #holds
  avg_precision_sum = []
  all_predictions = []
  
  #for each year, starting from year 5(1996), so there is data
  #to use for predictions
  for year in years[5:]:

    #training will use data from before that year
    train = stats[stats["Year"]<year]

    #testing will use data of that year
    test = stats[stats["Year"] == year]

    
    #fits the model using the predictors to predict share
    model.fit(train[predictors], train["Share"])

    #creates a numpy array holding the data
    predictions = model.predict(test[predictors])

    #turns the numpy array into a dataframe and puts the data under Predictions
    predictions = pd.DataFrame(predictions, columns=["Predictions"], index=test.index)

    #combines the columns of Player and Share from test with predictions
    combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)


    combination["Year"] = year

    combination = add_ranks(combination)

    #holds all the values from combination
    all_predictions.append(combination)

    #calls find_avg_precision to get the average precision of the predicted values
    avg_precision_sum.append(find_avg_precision(combination))

  mean_score = sum(avg_precision_sum)/len(avg_precision_sum)
  return mean_score, avg_precision_sum, pd.concat(all_predictions)

"""
Use:
Function to write stats to files

Input:

version - name of folder to save data in (string)
award - name of award to use (string)
f2 - file to hold cumulative stats (File)

Returns:

None
"""
def write_stats(version, award, f2):
  #initialized a ridge regression model with alpha 0.1
  reg = Ridge(alpha=0.1)

  #list of years that data exists for
  years = list(range(1991,2025))
  

  #writing the accuracy stats to a separate text file
  f = open(version+"/"+award+"/Precision.txt", "w")
  
  #calls input_data and then backtest to generate mean average precision, 
  #average precision each year, and the data frame holding all award data
  stats, predictors = input_data(award)
  mean_ap, ap_year, all_predictions = backtest(stats, reg, years, predictors)

  #writes to Cumulative file to show mean AP for each award
  f2.write("{} = {}%\n\n".format(award, round(mean_ap,4)*100))

  #merges AP each year with corresponding year into 1 array
  merged_array = [list(pair) for pair in zip(years[5:], ap_year)]

  #writes data to txt file
  f.writelines([award+" Statistics\n\n",
               "Average Precision = {}%\n\n".format(round(mean_ap,4)*100),
               "Year    Precision\n\n"])

  for i in range(len(merged_array)):
    f.write("{} = {}%\n".format(merged_array[i][0], round(merged_array[i][1],4)*100))

  #creates csv file to hold dataframe
  all_predictions.to_csv(version+"/"+award+"/Dataframe.csv", index=False)
