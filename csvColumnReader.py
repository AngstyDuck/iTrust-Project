"""
README
Prints [NUMOFLINES] of lines from the .csv file.
"""


import csv


INPUTDIR = "./data/processed/FR2SplitData.csv"
NUMOFLINES = 1000


counter0 = 0
counter1 = 0
indexList = {}

variables = ["2_MV_003_STATUS"]



with open(INPUTDIR) as csvfile0:
	spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

	for row in spamreader:
		if counter0 == 0:
			for i in range(len(row)):
				for j in variables:
					if j in row[i]:
						indexList[j] = i
						counter1 += 1

			if counter1 != len(variables):
				print("ERROR: Retrieving column index from .csv file")
				break
		else:
			if counter0 > NUMOFLINES:
				break
			else:
				print("Key: {0}; Key Value: {1}".format(variables[0], row[indexList[variables[0]]]))

		counter0 += 1


