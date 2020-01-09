# Brian Blaylcok
# June 28, 2017

"""
Plot the location of the cameras
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB_v2')

from BB_MesoWest.MesoWest_STNinfo import get_station_info

stns = ['WBB', 'UUSYR', 'BFLAT', 'NAA', 'GNI', 'FPN', 'EYSC']

# Get station info
a = get_station_info(stns)
plt.figure(figsize=[8,10])

# Make map
m = Basemap(llcrnrlon=a['LON'].min()-.25, llcrnrlat=a['LAT'].min()-.25,\
            urcrnrlon=a['LON'].max()+.25, urcrnrlat=a['LAT'].max()+.25,)

m.arcgisimage(service='World_Shaded_Relief', xpixels=700, verbose=False)
# Overlay Utah Roads
BASE = '/uufs/chpc.utah.edu/common/home/u0553130/'
m.readshapefile(BASE+'shape_files/tl_2015_UtahRoads_prisecroads/tl_2015_49_prisecroads',
                            'roads',
                            linewidth=.5,
                            color='dimgrey')
m.drawstates()

# Plot locations on map
for i in range(0, len(a)):
    #
    plt.scatter(a['LON'][i], a['LAT'][i], s=60)
    #
    # North
    if a['STNID'][i] in ['EYSC']:
        plt.annotate('',
                     xy=(a['LON'][i], a['LAT'][i]+.11),
                     xytext=(a['LON'][i], a['LAT'][i]),
                     arrowprops=dict(facecolor='black', shrink=0.01))
        plt.text(a['LON'][i]+.02, a['LAT'][i]-.07, a['STNID'][i])
    # South
    if a['STNID'][i] in ['GNI', 'WBB']:
        plt.annotate('',
                     xy=(a['LON'][i], a['LAT'][i]-.11),
                     xytext=(a['LON'][i], a['LAT'][i]),
                     arrowprops=dict(facecolor='black', shrink=0.01))
        plt.text(a['LON'][i]+.02, a['LAT'][i]+.02, a['STNID'][i])
    # East
    if a['STNID'][i] in ['NAA']:
        plt.annotate('',
                     xy=(a['LON'][i]+.11, a['LAT'][i]),
                     xytext=(a['LON'][i], a['LAT'][i]),
                     arrowprops=dict(facecolor='black', shrink=0.01))
        
        plt.text(a['LON'][i]-.15, a['LAT'][i]+.05, a['STNID'][i])
    # West
    if a['STNID'][i] in ['WBB']:
        plt.annotate('',
                     xy=(a['LON'][i]-.11, a['LAT'][i]),
                     xytext=(a['LON'][i], a['LAT'][i]),
                     arrowprops=dict(facecolor='black', shrink=0.01))
        if a['STNID'][i] != 'WBB':
            plt.text(a['LON'][i]+.05, a['LAT'][i]+.05, a['STNID'][i])
    # Northwest
    if a['STNID'][i] in ['BFLAT', 'UUSYR', 'FPN']:
        plt.annotate('',
                     xy=(a['LON'][i]-.08, a['LAT'][i]+.08),
                     xytext=(a['LON'][i], a['LAT'][i]),
                     arrowprops=dict(facecolor='black', shrink=0.01))
        plt.text(a['LON'][i]+.02, a['LAT'][i]-.07, a['STNID'][i])

plt.savefig('cam_locs.png', bbox_inches='tight')
