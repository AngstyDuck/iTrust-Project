import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

DIR2_LT_002 = "./data/processed/2_LT_002Data.csv"
DIR2_MV_001 = "./data/processed/2_MCV_101Data.csv"
DIR2_MV_002 = "./data/processed/2_MV_101Data.csv"
DIROUTPUT = "./data/processed/2_LT_001DataNoInAndOut.csv"


for i in ["2_LT_001"]:
    """
    Plot graphs of data and save them as png pictures
    """
    inpDir = "./data/processed/"+i+"Data.csv"

    with open(inpDir) as csvfile:
        counter0 = 0
        counter1 = 0
        xArray = []
        yArray = []
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for row in spamreader:
            if counter1 != 0:
                if counter1-counter0 < 1000:
                    xArray.append(row[0])
                    yArray.append(row[1])
                else:
                    plt.plot(xArray, yArray)
                    plt.show()

                    string = "./data/"+i+"Visualization/picture"+str(counter0)+".png"
                    plt.savefig(string)

                    plt.figure()

                    counter0 = counter1
                    print(xArray)
                    print(yArray)
                    xArray = [row[0]]
                    yArray = [row[1]]
                    print("PING")


            counter1 += 1
            # print("sensor: {0}; counter: {1}".format(i,counter1))






































# fin
