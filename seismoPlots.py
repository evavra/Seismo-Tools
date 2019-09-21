from readCatalogPandas import catalog2df
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import shapefile as shp
import pandas as pd


# All plotting methods are designed to take Pandas dataframes, column formats are specified in each method.


def driver():
    calderaShp = '/Users/ellisvavra/Thesis/GIS_Database/caldera_wgs84.shp'
    monoShp = '/Users/ellisvavra/Thesis/GIS_Database/mono_ll/mono_ll.shp'
    crowleyShp = '/Users/ellisvavra/Thesis/GIS_Database/crowley_ll/crowley_ll.shp'
    catalogFile = '/Users/ellisvavra/Thesis/seismicity/catalogs/ncedc_20140101_20190909.csv'

    xaxis = 'unfolded'
    bounds = [-119.25, -118.25, 37.25, 38.5, -20, 0]

    catalog = catalog2df(catalogFile)
    fig = plt.figure(figsize=(15,10))
    ax = plt.subplot(111)

    ax0, ax1, ax2 = swath(catalog, bounds, xaxis, 'viridis', 1, ax)

    plt.plotShp(caldera, 'black', 2)
    plt.plotShp(mono, 'cyan', 1)
    plt.plotShp(crowley, 'cyan', 1)

    plt.show()


# ------------------------- CONFIGURE -------------------------

def configMap():
    calderaShp = '/Users/ellisvavra/Thesis/GIS_Database/caldera_wgs84.shp'
    monoShp = '/Users/ellisvavra/Thesis/GIS_Database/mono_ll/mono_ll.shp'
    crowleyShp = '/Users/ellisvavra/Thesis/GIS_Database/crowley_ll/crowley_ll.shp'
    # catalogFile = '/Users/ellisvavra/Thesis/seismicity/catalogs/ncedc_20140101_20190909.csv'
    # Load data
    caldera = readShp(calderaShp)
    mono = readShp(monoShp)
    crowley = readShp(crowleyShp)
    # catalog = catalog2df(catalogFile)

    # Figure settings
    # fig = plt.figure(figsize=(10,10))
    # ax = plt.subplot(111)
    # ax.set_aspect(1.3)

    plotShp(caldera, 'black', 2)
    plotShp(mono, 'cyan', 1)
    plotShp(crowley, 'cyan', 1)
    # map(catalog, 'viridis_r', 3)

    # plt.xlim([-119.25, -118.5])
    # plt.ylim([37.25, 37.8])

    # plt.show()

# ------------------------- READ -------------------------

def readShp(fileName):
    # Reads ESRI shapefile (.shp) to dataframe containing verticies with following format:
    # [0] Latitude
    # [1] Longitude

    # Load shapefile
    sf = shp.Reader(fileName)

    # Extract x and y coordinates from shapefile
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]

        # print(x[:10])
        # print(y[:10])

        shape = pd.DataFrame(list(zip(y, x)) , columns=['Latitude', 'Longitude'])

        # print(shape.head(5))

    return shape




# ------------------------- PLOT -------------------------

def plotShp(shape, c, zorder):
    # Takes dataframe containing polygon verticies with following format:
    # [0] Latitude
    # [1] Longitude

    plt.plot(shape['Longitude'], 
             shape['Latitude'], 
             color=c, 
             zorder=zorder)


def map(catalog, cmap, zorder):
    # Takes dataframe with following format:
    # [0] DateTime 
    # [1] Latitude 
    # [2] Longitude 
    # [3] Depth 
    # [4] Magnitude
    plt.set_cmap(cmap)
    plt.scatter(catalog['Longitude'], 
                catalog['Latitude'], 
                marker='.', 
                s=10**catalog['Magnitude'] / 10, 
                c=-catalog['Depth'],
                vmin=-15,
                vmax=0,
                alpha=1,
                zorder=zorder)

    cbar = plt.colorbar(ticks=None, label="Depth [km]")


def swath(catalog, bounds, xaxis, cmap, zorder, subFigID):
    # Takes dataframe with following format:
    # [0] DateTime 
    # [1] Latitude 
    # [2] Longitude 
    # [3] Depth 
    # [4] Magnitude

    plt.set_cmap(cmap)

    if xaxis == 'EW':

        s_scale = 4**catalog['Magnitude']
        c_scale = catalog['Magnitude']

        # EW Swath
        ax = plt.subplot(subFigID)
        ax.title.set_text('West - East')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Depth')
        obj = ax.scatter(catalog['Longitude'], 
                    -catalog['Depth'], 
                    marker='.', 
                    s=s_scale, 
                    c=c_scale,
                    vmin=0,
                    vmax=max(catalog['Magnitude']),
                    # c=-catalog['Depth'],
                    # vmin=-15,
                    # vmax=0,
                    alpha=1,
                    zorder=zorder)
        ax.axis([bounds[0], bounds[1], bounds[4], bounds[5]])


        cbar = plt.colorbar(obj)
        cbar.set_label("Magnitude")

        # plt.scatter(catalog['Longitude'], 
        #             -catalog['Depth'], 
        #             marker='.', 
        #             s=10**catalog['Magnitude'] / 100, 
        #             c=10**catalog['Magnitude'] / 100,
        #             vmin=0,
        #             vmax=5,
        #             # c=-catalog['Depth'],
        #             # vmin=-15,
        #             # vmax=0,
        #             alpha=1,
        #             zorder=zorder)
        # plt.axis([bounds[0], bounds[1], bounds[4], bounds[5]])
        # plt.set_aspect(0.05)

    elif xaxis == 'NS':

        s_scale = 4**catalog['Magnitude']
        c_scale = catalog['Magnitude']

        # NS swath
        ax = plt.subplot(subFigID)
        ax.title.set_text('South - North')
        ax.set_xlabel('Latitude')
        obj = ax.scatter(catalog['Latitude'], 
                    -catalog['Depth'], 
                    marker='.', 
                    s=s_scale, 
                    c=c_scale,
                    vmin=0,
                    vmax=max(catalog['Magnitude']),
                    # c=-catalog['Depth'],
                    # vmin=-15,
                    # vmax=0,
                    alpha=1,
                    zorder=zorder)
        ax.axis([bounds[2], bounds[3], bounds[4], bounds[5]])

        cbar = plt.colorbar(obj)
        cbar.set_label("Magnitude")

        # plt.scatter(catalog['Latitude'], 
        #             -catalog['Depth'], 
        #             marker='.', 
        #             s=10**catalog['Magnitude'] / 100, 
        #             c=10**catalog['Magnitude'] / 100,
        #             vmin=0,
        #             vmax=5,
        #             # c=-catalog['Depth'],
        #             # vmin=-15,
        #             # vmax=0,
        #             alpha=1,
        #             zorder=zorder)
        # plt.axis([bounds[2], bounds[3], bounds[4], bounds[5]])
        # plt.set_aspect(0.05 * 1.3)


    elif xaxis == 'both':
        gs = gridspec.GridSpec(1, 2,width_ratios=[abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]) * 1.3])
        
        s_scale = 4**catalog['Magnitude']
        c_scale = catalog['Magnitude']

        # EW Swath
        ax1 = plt.subplot(gs[0])
        ax1.title.set_text('West - East')
        ax1.set_xlabel('Longitude')
        ax1.set_ylabel('Depth')
        plt.scatter(catalog['Longitude'], 
                    -catalog['Depth'], 
                    marker='.', 
                    s=s_scale, 
                    c=c_scale,
                    vmin=0,
                    vmax=max(catalog['Magnitude']),
                    # c=-catalog['Depth'],
                    # vmin=-15,
                    # vmax=0,
                    alpha=1,
                    zorder=zorder)
        ax1.axis([bounds[0], bounds[1], bounds[4], bounds[5]])

        # NS swath
        ax2 = plt.subplot(gs[1])
        ax2.title.set_text('South - North')
        ax2.set_xlabel('Latitude')
        plt.scatter(catalog['Latitude'], 
                    -catalog['Depth'], 
                    marker='.', 
                    s=s_scale, 
                    c=c_scale,
                    vmin=0,
                    vmax=max(catalog['Magnitude']),
                    # c=-catalog['Depth'],
                    # vmin=-15,
                    # vmax=0,
                    alpha=1,
                    zorder=zorder)
        ax2.axis([bounds[2], bounds[3], bounds[4], bounds[5]])

    elif xaxis == 'unfolded':

        gs = gridspec.GridSpec(2, 2)
        
        s_scale = 4**catalog['Magnitude']
        c_scale = catalog['Magnitude']

        # Map view
        ax0 = plt.subplot(gs[0])
        ax0.title.set_text('Map')
        ax0.set_xlabel('Longitude')
        ax0.set_ylabel('Latitude')
        plt.scatter(catalog['Longitude'], 
            catalog['Latitude'], 
            marker='.', 
            s=s_scale, 
            c=c_scale,
            vmin=0,
            vmax=max(catalog['Magnitude']),
            # c=-catalog['Depth'],
            # vmin=-15,
            # vmax=0,
            alpha=1,
            zorder=zorder)
        ax0.axis([bounds[0], bounds[1], bounds[2], bounds[3]])

        # EW Swath
        ax1 = plt.subplot(gs[2])
        ax1.title.set_text('West - East')
        ax1.set_xlabel('Longitude')
        ax1.set_ylabel('Depth')
        plt.scatter(catalog['Longitude'], 
                    -catalog['Depth'], 
                    marker='.', 
                    s=s_scale, 
                    c=c_scale,
                    vmin=0,
                    vmax=max(catalog['Magnitude']),
                    # c=-catalog['Depth'],
                    # vmin=-15,
                    # vmax=0,
                    alpha=1,
                    zorder=zorder)
        ax1.axis([bounds[0], bounds[1], bounds[4], bounds[5]])

        # NS swath
        ax2 = plt.subplot(gs[1])
        ax2.title.set_text('South - North')
        ax2.set_xlabel('Depth')
        ax2.set_label('Latitude')
        plt.scatter(-catalog['Depth'], 
                    catalog['Latitude'], 
                    marker='.', 
                    s=s_scale, 
                    c=c_scale,
                    vmin=0,
                    vmax=max(catalog['Magnitude']),
                    # c=-catalog['Depth'],
                    # vmin=-15,
                    # vmax=0,
                    alpha=1,
                    zorder=zorder)
        ax2.axis([bounds[5], bounds[4], bounds[2], bounds[3]])

        return ax0, ax1, ax2

if __name__ == '__main__':
    driver()