#imports
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time
from selenium import webdriver

#list for years data will range
years = list(range(1991,2025))


"""
Function to parse data from a web page when given
"""
def parser(location, tag, cleanup_class, table_id, file_name):

    #for each id in table_id
    for x in range(len(table_id)):
        #to hold dataframes
        temp_dataframes= []
        temp_dataframes2 = []
        dataframes = []

        #for each year in list of years, find corresponding html page and opens it for reading
        for year in years:
            with open(location+"/{}.html".format(year),"r", encoding="utf-8") as f:
                page = f.read()

            #initializing a parser class
            soup = BeautifulSoup(page, "html.parser")

            #cleans up data table by removing unnecessary rows/classes in html
            for i in range(len(cleanup_class)):
                classes = soup.find_all(tag,class_ = cleanup_class[i])
                for i in classes:
                    i.decompose()

            
            if table_id[x] == "divs_standings_E":
                 #selecting the table for MVP
                table = soup.find(id="divs_standings_W")

                #assigning the table to a variable
                topic = pd.read_html(StringIO(str(table)))[0]

                #adding a column to identify what year the table is from
                topic["Year"] = year
                topic["Team"] = topic["Western Conference"]
                del topic["Western Conference"]
                #adding the table to a list
                dataframes.append(topic)


            #selecting the table for given table id
            table = soup.find(id=table_id[x])

            #assigning the table to a variable
            topic = pd.read_html(StringIO(str(table)))[0]

            #adding a column to identify what year the table is from
            topic["Year"] = year
            if table_id[x] == "divs_standings_E":
                topic["Team"] = topic["Eastern Conference"]
                del topic["Eastern Conference"]
            #adding the table to a list
            dataframes.append(topic)
            

        #merges dataframes into one
        topics = pd.concat(dataframes)


        #writes dataframes to csv file
        topics.to_csv("csv/"+file_name[x]+".csv")

"""
Function to scrape data from webpage and convert it into a locally stored HTML files

Input paramters:

url_start: url from where to scrape
folder_name: name of folder for html files to be saved in
"""
def scraper(url_start, file_name):

    #for each year in list of years
    for year in years:

        #selenium interface to interact with Google Chrome
        driver = webdriver.Chrome()

        #formats input url to specific year
        url = url_start.format(year)

        #opens the url and scrolls to the bottom
        driver.get(url)
        driver.execute_script("window.scrollTo(1,100000)")
        
        #pauses for 2 seconds to prevent time outs
        time.sleep(2)

        #gets the html webpage
        html= driver.page_source

        #stores html into folder
        with open(file_name+"/{}.html".format(year), "w+", encoding="utf-8") as f:
            f.write(html)

