import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import collections
from readCatalogPandas import catalog2df
import datetime as dt

def driver():
    # Filter catalog
    newCatalog, search = configFilt(catalogFile, 
                                    minDate, maxDate,
                                    minLat, maxLat, 
                                    minLon, maxLon, 
                                    minDepth, maxDepth, 
                                    minMag, maxMag)

    # Get seismicity rate timeseries and plot
    dates, counts = seismicityCount(newCatalog, search)
    plotSumQuake(dates, counts)
    plt.show()

# ------------------------------- CONFIGURE -------------------------------
def configFilt(catalogFile, 
               minDate, maxDate,
               minLat, maxLat, 
               minLon, maxLon, 
               minDepth, maxDepth, 
               minMag, maxMag):

    # Create namedTuple for search parameters
    param = collections.namedtuple('searchParameters',
                                  ['minDate', 'maxDate',          # Must be 'YYYY/MM/DD HH:MM:SS' formatted strings
                                   'minLat', 'maxLat', 
                                   'minLon', 'maxLon', 
                                   'minDepth',  'maxDepth', 
                                   'minMag', 'maxMag'])

    # Read in EQ catalog data
    catalog  = catalog2df(catalogFile)

    # Set search parameters:
    search = param(minDate=minDate, maxDate=maxDate,
                   minLat=minLat, maxLat=maxLat, 
                   minLon=minLon, maxLon=maxLon, 
                   minDepth=minDepth, maxDepth=maxDepth, 
                   minMag=minMag, maxMag=maxMag)

    # Filter EQ catalog
    newCatalog = filterCatalog(catalog, search)

    return newCatalog, search


# ------------------------------- ANALYSIS -------------------------------

def filterCatalog(catalog, search):
    print()
    print('Number of earthquakes in original catalog: ' + str(len(catalog.index)))

    minDatetime = dt.datetime.strptime(search.minDate, '%Y/%m/%d %X')
    maxDatetime = dt.datetime.strptime(search.maxDate, '%Y/%m/%d %X')

    newCatalog = catalog[(catalog['DateTime']  >= minDatetime) &
                         (catalog['DateTime']  <= maxDatetime) &
                         (catalog['Latitude']  >= search.minLat) &
                         (catalog['Latitude']  <= search.maxLat)  &
                         (catalog['Longitude'] >= search.minLon) &
                         (catalog['Longitude'] <= search.maxLon) &
                         (catalog['Depth']     >= search.minDepth) & 
                         (catalog['Depth']     <  search.maxDepth) &
                         (catalog['Magnitude'] >= search.minMag) &
                         (catalog['Magnitude'] <  search.maxMag) ]

    print()
    print('Search parameters: ')
    print('minDate: '  + minDatetime.strftime('%Y/%m/%d'))
    print('maxDate: '  + maxDatetime.strftime('%Y/%m/%d'))
    print('minLon: '   + str(search.minLon))
    print('maxLon: '   + str(search.maxLon))
    print('minLat: '   + str(search.minLat))
    print('maxLat: '   + str(search.maxLat))
    print('minDepth: ' + str(search.minDepth))
    print('maxDepth: ' + str(search.maxDepth))
    print('minMag: '   + str(search.minMag))
    print('maxMag: '   + str(search.maxMag))
    print()
    print('Number of earthquakes in new catalog: ' + str(len(newCatalog.index)))
    print()
    print(newCatalog.head(5))
    print(newCatalog.tail())


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