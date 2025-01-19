# NBA Award Predictor 🏀
A machine learning-based tool to predict the correct Top 5 for NBA awards using player statistics.

## Description
This project uses data from 1991-2024 to determine an accurate Top 5 for various NBA awards (list below) with approximately 70% accuracy by analyzing player statistics. It uses machine learning algorithms and publicly available NBA data to do this. 

## Features
- Scrapes data from 1991-2024 from Basketball Reference, a public database that has all the necessary data for this project
- Collects data on the following awards (plus current accurary for each in V1.0 of algorithm)
    - Most Valuable Player (MVP): 80.95%
    - Defensive Player of the Year (DPOY): 69.42%
    - Sixth Man of the Year (6MOY): 69.98%
    - Most Improved Player (MIP): 43.73%
    - Rookie of the Year (ROY): 82.6%
    - All NBA First Team (ALL-NBA): 79.54%
    - All Defensive First Team (ALL-DEF): 58.67%
    - All Rookie Team (ALL-ROOK): 74.17%
- Parses the data and stores it in CSV files and then cleans it to be used in predictive Algorithm
- Uses a Ridge regression model and predictive statistics to determine top 5 candidates for each award
- Stores data in TXT and CSV files for easy access and readability

## Use
Run each of the functions in main.py once, in the following order Scrape --> Parse --> Clean --> Predict. You can then view the stored data for each award in the corresponding subfolder in the All_Data_Precision_Stats folder, either in the .txt file or the .csv file. Or to view the top 10 for each award, run the View function in main.py with the input parameter for what year and award you want to see.

## Technologies
- Python
- Pandas
- SciKit-Learn
- BeautifulSoup
- Selenium

## Next Steps
- improve accuracy for predictor by giving weights for predictive stats used in algorithm to tailor for each award
- allow for data from before 1991 to be included
- allow for selection of dataset to use in predictions
- allow input data from current up-to-date stats to make prediction on current years awards
- create a user interface to make viewing data simpler
