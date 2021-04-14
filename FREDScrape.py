###############################################################
#####     FEDERAL RESERVE ECONOMIC DATA (FRED) SCRAPE     #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)             #####
#####     CREATE_DATE: 2021/03/25                         #####
#####     LAST_MODIFIED: 2021/04/10                       #####
###############################################################
import os 
import time
from bs4 import BeautifulSoup
import urllib.request
print('urllib.request: {}'.format(urllib.request.__version__))
import pandas as pd
print('Pandas: {}'.format(pd.__version__))
import requests
print('Requests: {}'.format(requests.__version__))

class FREDScrape:
    def __init__(self,SourceURL): 
        self.CategoryNew = []
        self.CategoryArchive = []
        self.results = []
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.SourceURL = SourceURL
        self.parser = 'html.parser'
        self.Output = pd.DataFrame(columns=['FRED ID', 'Title', 'URL']) 

    def get_title(self,URL):
        attempts = 0
        while attempts < 10:
            try:
                reqs = requests.get(URL)
                break
            except:
                attempts += 1
                print ('URL Lookup Failure: Try Again ' + str(attempts))
                time.sleep(10)
        soup2 = BeautifulSoup(reqs.text, self.parser)
        title = soup2.find('title').get_text()
        return (title)

    def FirstRun(self):
        resp = urllib.request.urlopen(self.SourceURL)
        soup = BeautifulSoup(resp, self.parser, from_encoding=resp.info().get_param('charset'))
        for link in soup.find_all('a', href=True):
            if 'categories' in link['href']:
                if ((link['href']).replace('/categories/','')) != '':
                    self.CategoryNew.append((link['href']).replace('/categories/','')) 
                if '/series/' in link['href'] and ((link['href']).replace('/series/','')) not in self.results:
                        self.results.append((link['href']).replace('/series/','')) 

        self.CategoryNew = list(set(self.CategoryNew))
        self.CategoryNew = sorted(self.CategoryNew, reverse=False)
        return(self.CategoryNew)

    def SubsequentRuns(self,CategoryNew,CategoryArchive,results,Output):
        TempCategoryNew = []
        for i in self.CategoryNew:
            self.CategoryArchive.append(i) 
            print('RUNNING: ' + self.SourceURL + '/' + i)
            attempts = 0
            while attempts < 5:
                try:
                    resp = urllib.request.urlopen(self.SourceURL + '/'+i)
                    break
                except:
                    attempts += 1
                    print ('Category Lookup Failure: Try Again ' + str(attempts))
                    time.sleep(10)
            soup = BeautifulSoup(resp, self.parser, from_encoding=resp.info().get_param('charset'))
            for link in soup.find_all('a', href=True):
                if 'categories' in link['href'] and 'http://' not in link['href']:
                    if ((link['href']).replace('/categories/','')) != '' and ((link['href']).replace('/categories','')) != '':  
                        TempCategoryNew.append((link['href']).replace(' /categories/','').replace('/categories/','')) 
                if '/series/' in link['href'] and ((link['href']).replace('/series/','')) not in self.results:
                        self.results.append((link['href']).replace('/series/','')) 
                        URL = ("https://fred.stlouisfed.org" +(link['href']))
                        title = self.get_title(URL)
                        while title == '504 Gateway Time-out':
                            title = self.get_title(URL)
                        self.Output = self.Output.append({'FRED ID': (link['href']).replace('/series/',''), 'Title': title, 'URL': URL}, ignore_index=True)

        TempCategoryNew = list(set(TempCategoryNew)) # UNIQUE NEW TEMPORARY CATEGORIES 
        TempCategoryNew = sorted(TempCategoryNew, reverse=False) # SORT NEW TEMPORARY CATEGORIES 
        self.CategoryNew = list(set(TempCategoryNew) - set(self.CategoryArchive)) # NEW CATEGORIES = TEMP NEW CATEGORIES THAT HAVE NOT ALREADY BEEN RUN
        self.CategoryNew = list(set(self.CategoryNew)) # UNIQUE NEW CATEGORIES 
        self.CategoryNew = sorted(self.CategoryNew, reverse=False) # SORT NEW CATEGORIES  
        return(self.CategoryNew)
            
if __name__ == "__main__":
    try:
        FRED = FREDScrape("https://fred.stlouisfed.org/categories")
        FRED.FirstRun()
        while len(FRED.CategoryNew) >= 1: 
            FRED.CategoryNew = FRED.SubsequentRuns(FRED.CategoryNew,FRED.CategoryArchive,FRED.results,FRED.Output)
        FRED.Output.to_csv(FRED.dir + r'\FRED_Output.csv', index=True)
        quit() 
    except:
        FRED.Output.to_csv(FRED.dir + r'\FRED_Output.csv', index=True)
        quit() 