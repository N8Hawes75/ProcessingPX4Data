#==============================================
#
#  Nathaniel Hawes, nh979416@ohio.edu
#
#==============================================


import pandas as pd
import numpy as np
import pyproj
from matplotlib import pyplot as plt

# import warnings
# warnings.filterwarnings('ignore')
P = pyproj.Proj(proj='utm', zone=17, ellps='WGS84', preserve_units=False)

class PosData():
    def __init__(self, filename, Start, Mid, End):
        file = pd.read_csv(filename)

        time = file.iloc[0:8000, 0:1].values
        x    = file.iloc[0:7500, Start:Mid].values
        y    = file.iloc[0:7500, Mid:End].values
        lat  = file.iloc[0:8000, 2:3].values
        lon  = file.iloc[0:8000, 3:4].values

        self.time = np.array(time)
        self.lat  = np.array(lat)
        self.lon  = np.array(lon)
        self.x    = np.array(x)
        self.y    = np.array(y)

class WayPtsData():
    def __init__(self, filename, Start, Mid, End, Origin, Pos):
        file = pd.read_csv(filename)
        time = file.iloc[0:8000, 0:1].values
        xpts = file.iloc[0:7500, Start:Mid].values
        ypts = file.iloc[0:7500, Mid:End].values

        homex = Pos.lon[0]        # Sets the origin of the waypoint data ("Current lat/lon")
        homey = Pos.lat[0]
        
        nanArr    = np.isnan(xpts)                 # Parsing out the NaNs and repeats
        lon       = np.array([])
        lat       = np.array([])
        self.time = np.array([])
        last_ind  = -1

        for i in range(len(xpts)):
            if (nanArr[i] == False):
                if (last_ind >= 0):
                    if (i > 0 and np.not_equal(lon[last_ind],xpts[i])):      # Tests to see if the current value is equal to the last value
                        lon = np.append(lon, xpts[i])
                        lat = np.append(lat, ypts[i])
                        self.time = np.append(self.time, time[i])
                        last_ind += 1
                else:
                    lon = np.append(lon, xpts[i])
                    lat = np.append(lat, ypts[i])
                    self.time = np.append(self.time, time[i])
                    last_ind += 1
        
        # self.xpts, self.ypts = pyproj.transformer.Transformer('epsg:4326', 'epsg:3638', lon, lat)
        
        homex,homey = P(homex,homey)
        xpts, ypts  = P(lat, lon)
        self.xpts = xpts - homex
        self.ypts = ypts - homey

        # print(homex,homey)
        # print(xpts, ypts)

        # self.xpts *= 0.3048
        # self.ypts *= 0.3048



if __name__ == "__main__":
    dir      = "/home/nathan/Documents/PRACAS_FlightTestData/"
    IntDir   = "Intruder_UAV/Intruder_FlightTest_"
    MissDir  = "Mission_UAV/Mission_FlightTest_"
    testDir  = "/home/nathan/Documents/PRACAS_FlightTestData/Test.csv"

    Madj1    = 3700#4250
    Madj2    = 1550#1500
    Iadj1    = 2500
    Iadj2    = 500

    PosPlts  = True
    HeadPlts = False
    Waypts   = True
    TestPlot = not True
    lw       = 2

    fig,ax1  = plt.subplots()

    Intruder = PosData(dir + IntDir + "vehicle_local_position_0.csv", 4, 5, 6)
    IntWay   = WayPtsData(dir + IntDir + "position_setpoint_triplet_0.csv", 42,43,44,82, Intruder)

    Mission  = PosData(dir + MissDir + "vehicle_local_position_0.csv", 4, 5, 6)
    MissWay  = WayPtsData(dir + MissDir + "position_setpoint_triplet_0.csv", 42,43,44,82, Mission)

    if (PosPlts):
        ax1.plot(Intruder.y[Iadj1:len(Intruder.y)-Iadj2],Intruder.x[Iadj1:len(Intruder.x)-Iadj2], 'orange', linewidth= lw, label="Intruder Path", zorder = 2)
        ax1.scatter(Intruder.y[Iadj1],Intruder.x[Iadj1], c='k', marker=(3,0,-90), s=150, label="Intruder Start", edgecolor = 'g', zorder = 10)
        ax1.scatter(Intruder.y[len(Intruder.y)-Iadj2],Intruder.x[len(Intruder.y)-Iadj2], c='k', marker=(3,0,-90), s=150, label="Intruder End", edgecolor = 'r', zorder = 10)

        ax1.plot(Mission.y[Madj1:len(Mission.y)-Madj2],Mission.x[Madj1:len(Mission.x)-Madj2], 'b', linewidth= lw, label="Mission Path", zorder = 2)
        ax1.scatter(Mission.y[Madj1],Mission.x[Madj1], c='g', marker=(3,0,-45), s=150, label="Mission Start", edgecolor = 'k', zorder = 10)
        ax1.scatter(Mission.y[len(Mission.y)-Madj2],Mission.x[len(Mission.x)-Madj2], c='r', marker=(3,0,-35), s=150, label="Mission End", edgecolor = 'k', zorder = 10)

    if (HeadPlts):
        IntHead = PosData(dir + IntDir + "vehicle_local_position_0.csv",4,6,20)

    if(Waypts):
        MwayAdj1 = 3
        MwayAdj2 = 1

        # ax1.plot(IntWay.xpts,IntWay.ypts,"r*", label="Intruder Waypoints", markersize = 10)
        ax1.plot(MissWay.xpts[0:MwayAdj1],MissWay.ypts[0:MwayAdj1],"b*", label="Original Mission Waypoints", markersize = 10, zorder = 3)
        ax1.scatter(MissWay.xpts[MwayAdj1:len(MissWay.xpts)-MwayAdj2],MissWay.ypts[MwayAdj1:len(MissWay.xpts)-MwayAdj2],c="yellow", label="PRACAS Waypoints", s = 100,edgecolor='k',marker = '*', zorder = 4)
        ax1.plot(MissWay.xpts[len(MissWay.xpts)-MwayAdj2:len(MissWay.xpts)],MissWay.ypts[len(MissWay.xpts)-MwayAdj2:len(MissWay.xpts)],"b*", markersize = 10, zorder = 3)

    if(TestPlot):
        plt.scatter(0,0,marker=(3,0,-90),s=2000, c = 'yellow', edgecolor = 'k')


    ax1.axis('equal')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.grid(True)
    plt.legend(loc = 'lower left')
    plt.show()