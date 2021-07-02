import pandas as pd
import datetime as dt

def read_eq_catalog(file_name,  format):

    """
    Read in seismic catalog and output DateTime, Latitude, Longitude, Depth, and Magnitude to dataframe
    Compatible formats:
    Northern California Earthquake Data Cender - 'NCEDC'
    Southern California Seismic Network - 'SCSN'
    """

    if format == 'NCEDC':
        full_catalog = pd.read_csv(file_name, skiprows=13)
        catalog = full_catalog.iloc[:, 0:5]

        # Convert dateTime column to dt objects
        dtColumn = pd.to_datetime(catalog['DateTime'], format='%Y/%m/%d %X.%f')

        # Replace original DateTimecolumn with dtColumn
        catalog['DateTime'] = dtColumn
    
    elif format == 'SCSN':
        # Header:
        # YYY MM DD  HH mm SS.ss  LATITUDE LONGITUDE Q MAG     DEPTH NPH    RMS   EVID
        # full_catalog = pd.read_csv(file_name, skiprows=9)
        dates = []
        lat   = []
        lon   = []
        depth = []
        mag   = []

        with open(file_name, 'r') as file:
            for line in file:
                # 2021 01 01  00 54 22.44 
                if line[0] != '#' and line[0] != '\n':
                    # Dates
                    try:
                        dates.append(dt.datetime.strptime(line[:20], '%Y %m %d  %H %M %S'))
                        

                    except ValueError:
                        # Some entries have more than 60s?
                        M = int(line[15:17])
                        S = int(line[18:20]) 

                        # Reset sec count
                        if S > 59:
                            S -= 60
                            M += 1

                        # Modify string
                        date_str = line[:15] + ' ' + str(M) + ' ' + str(S)
                        dates.append(dt.datetime.strptime(date_str, '%Y %m %d  %H %M %S'))

                    # Coordinates
                    lat_deg = float(line[25:27])
                    lat_min = float(line[28:32])
                    lat.append(lat_deg + lat_min/60)

                    lon_deg = float(line[33:37])
                    lon_min = float(line[38:42])
                    lon.append(lon_deg + lon_min/60)

                    # Depth
                    depth.append(float(line[53:59]))

                    # Magnitude
                    mag.append(float(line[46:49]))

        catalog = pd.DataFrame({'date': dates, 'lat': lat, 'lon': lon, 'depth': depth, 'mag': mag})
        # catalog = []
    

    return catalog


if __name__ == '__main__':
    # catalog2df('~/Seismo-Tools/test_catalog.csv')
    catalog = read_eq_catalog('/Users/evavra/Projects/SSAF/Seismicity/SCSN_20210701/2021.catalog', 'SCSN')
    print(catalog)