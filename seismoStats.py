import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import collections
from readCatalogPandas import catalog2df
import datetime as dt

def driver():
    # Filter catalog
    newCatalog, search = configFilt()

    # Get seismicity rate timeseries and plot
    dates, counts = seismicityCount(newCatalog, search)
    plotSumQuake(dates, counts)
    plt.show()

# ------------------------------- CONFIGURE -------------------------------
def configFilt():

    # Create namedTuple for search parameters
    param = collections.namedtuple('searchParameters',
                      ['minDate', 'maxDate',          # Must be 'YYYY/MM/DD HH:MM:SS' formatted strings
                       'minLat', 'maxLat', 
                       'minLon', 'maxLon', 
                       'minDepth',  'maxDepth', 
                       'minMag', 'maxMag'])

    # Read in EQ catalog data
    catalogFile = '~/Thesis/seismicity/ncedc_20140101_20190909.csv'
    catalog  = catalog2df(catalogFile)

    # Set search parameters:
    minDate = '2014/11/01 00:00:00'
    maxDate = '2019/08/01 00:00:00'
    minLat = 37
    maxLat = 39
    minLon = -120
    maxLon = -118
    minDepth = -1
    maxDepth = 20
    minMag = 1
    maxMag = 9
    search = param(minDate=minDate, maxDate=maxDate,
                   minLat=minLat, maxLat=maxLat, 
                   minLon=minLon, maxLon=maxLon, 
                   minDepth=minDepth, maxDepth=maxDepth, 
                   minMag=minMag, maxMag=maxMag)

    # search1 = param(minDate=minDate, maxDate=maxDate,
    #                minLat=minLat, maxLat=maxLat, 
    #                minLon=minLon, maxLon=maxLon, 
    #                minDepth=minDepth, maxDepth=maxDepth, 
    #                minMag=0, maxMag=1)
    # search2 = param(minDate=minDate, maxDate=maxDate,
    #                minLat=minLat, maxLat=maxLat, 
    #                minLon=minLon, maxLon=maxLon, 
    #                minDepth=minDepth, maxDepth=maxDepth, 
    #                minMag=1, maxMag=2)
    # search3 = param(minDate=minDate, maxDate=maxDate,
    #                minLat=minLat, maxLat=maxLat, 
    #                minLon=minLon, maxLon=maxLon, 
    #                minDepth=minDepth, maxDepth=maxDepth, 
    #                minMag=2, maxMag=3)
    # search4 = param(minDate=minDate, maxDate=maxDate,
    #                minLat=minLat, maxLat=maxLat, 
    #                minLon=minLon, maxLon=maxLon, 
    #                minDepth=minDepth, maxDepth=maxDepth, 
    #                minMag=3, maxMag=9)

    # Filter EQ catalog
    newCatalog = filterCatalog(catalog, search)


    return newCatalog, search


# ------------------------------- ANALYSIS -------------------------------

def filterCatalog(catalog, search):

    newCatalog = catalog[(catalog['DateTime'] >= search.minDate) &
                         (catalog['DateTime'] <= search.maxDate) &
                         (catalog['Latitude'] >= search.minLat) &
                         (catalog['Latitude'] <= search.maxLat) &
                         (catalog['Longitude'] >= search.minLon) &
                         (catalog['Longitude'] <= search.maxLon) &
                         (catalog['Depth'] >= search.minDepth) & 
                         (catalog['Depth'] < search.maxDepth) &
                         (catalog['Magnitude'] >= search.minMag) &
                         (catalog['Magnitude'] < search.maxMag) ]

    return newCatalog


def seismicityCount(catalog, search):

    # Convert date range to datetime format
    minDatetime = dt.datetime.strptime(search.minDate, '%Y/%m/%d %X')
    maxDatetime = dt.datetime.strptime(search.maxDate, '%Y/%m/%d %X')
    # Get number of days in range
    days = maxDatetime - minDatetime
    print(days.days)

    # Count the cummulative number of earthquakes occuring on/before each day in range
    dates = []
    numQuakes = []

    for i in range(int(days.days)):
        dates.append(minDatetime + dt.timedelta(days=i))
        numQuakes.append(len(catalog[catalog['DateTime'] <= dates[-1]]))
        # print(dates[-1].strftime('%Y/%m/%d'), str(numQuakes[-1]))

    return dates, numQuakes


# ------------------------------- PLOTS -------------------------------

def plotSumQuake(dates, counts):
    plt.grid(zorder=0)
    plt.plot(dates, counts)#, c='C0')
    plt.xlabel('Date')
    plt.ylabel('Cumulative number of events')
    plt.axis([min(dates), max(dates), 0, max(counts) + 10])

if __name__ == '__main__':
    driver()