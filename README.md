# Federal Reserve Economic Data (FRED) Scrape # 

## Purpose ## 
The purpose of this FRED python data scrape is to compile a complete list of all Federal Reserve Economic Data points. This script iterates over all FRED categories compiling a table of every unique FRED_ID, FRED Title, and FRED URL.  These results are intended for research and correlation testing with economic indicators. 
[FRED](https://fred.stlouisfed.org/categories)

## FREDScrape Usage ## 
``` ps1
python FREDScrape.py
```

## Results Usage ## 
```python
df = pdr.DataReader(FRED_ID, 'FRED', StartDate, EndDate)
df = (df[FRED_ID])
df = pd.DataFrame(data={"VALUE": df})    
df = df.reset_index()
return(df)
```