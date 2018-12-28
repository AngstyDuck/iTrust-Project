"""
README

To do: Clean data. Empty entries must be filled with None or 0; Ensure all data
columns are integers.

"""

import numpy as np
import csv


INPUTDIR = "./data/Wadi_data/WADI_14days.csv"
OUTPUTDIR = "./data/processed/processedWadi.csv"


with open(INPUTDIR) as csvfile:
    with open(OUTPUTDIR,"w+") as csvfileOut:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        spamwriter = csv.writer(csvfileOut, delimiter=" ", quotechar="|")
        counter=0
        for row in spamreader:
            # to only include rows that matter
            if counter < 4:
                counter += 1
                continue

            # joining, then splitting each row by their ","
            row = "".join(row)
            row = row.split(",")

            # write back to file
            spamwriter.writerow(row)

            print("Row {0}".format(counter))
            counter += 1

print("Done.")
