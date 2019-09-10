import pandas as pd
import datetime as dt

def catalog2df(fileName):

    # Read in NCEDC catalog and output DateTime, Latitude, Longitude, Depth, and Magnitude to dataframe
    fullCatalog = pd.read_csv(fileName, skiprows=13)
    catalog = fullCatalog.iloc[:, 0:5]

    # Convert dateTime column to dt objects
    dtColumn = pd.to_datetime(catalog['DateTime'], format='%Y/%m/%d %X.%f')

    # Replace original DateTimecolumn with dtColumn
    catalog['DateTime'] = dtColumn
    

    return catalog


# if __name__ == '__main__':
#     catalog2df('~/Seismo-Tools/test_catalog.csv')