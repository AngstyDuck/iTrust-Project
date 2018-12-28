"""
README
Prints [NUMOFLINES] of lines from the .csv file.
"""


import csv

# INPUTDIR = "./data/processed/2_LT_001DataNoInAndOut.csv"
INPUTDIR = "./data/processed/2_MV_006Data.csv"
NUMOFLINES = 100



with open(INPUTDIR) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
    counter=0
    for row in spamreader:
        if counter > NUMOFLINES:
            break
        print(", ".join(row))
        counter += 1
