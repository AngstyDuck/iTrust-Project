import csv
import numpy as np

DIRPROCESSEDWADI = "./data/processed/processedWadi.csv"
DIRFR1SPLIT = "./data/processed/FR1SplitData.csv"
DIRSTATESWADI = "./data/processed/statesWadi2.csv"


counter0 = 0
index = 3

with open(DIRFR1SPLIT) as csvfile0:
	with open(DIRSTATESWADI) as csvfile1:
		spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
		spamreader1 = csv.reader(csvfile1, delimiter=" ", quotechar="|")

		for row in spamreader:
			anotherRow = spamreader1.__next__()

			assert anotherRow[index] == row[index], "Counter0: {0}; anotherRow[0]: {1}; anotherRow[1]: {2}".format(counter0, anotherRow[0], row[0])

			counter0 += 1

		print("done.")
