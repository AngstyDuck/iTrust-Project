# state creation and verify all FRs
import csv
import numpy as np
import copy



DIR2_LT_001 = "./data/processed/2_LT_001Data.csv"
DIR2_LT_002 = "./data/processed/2_LT_002Data.csv"
DIR1_P_005 = "./data/processed/1_P_005Data.csv"
DIR2_FIT_001 = "./data/processed/2_FIT_001Data.csv"
DIR1_MV_004 = "./data/processed/1_MV_004Data.csv"
DIR2_FIT_001 = "./data/processed/2_FIT_001Data.csv"
DIR2_FIT_002 = "./data/processed/2_FIT_002Data.csv"
DIR2_FIT_003 = "./data/processed/2_FIT_003Data.csv"

DIRPROCESSEDWADI = "./data/processed/processedWadi.csv"
DIRFR2SPLIT = "./data/processed/FR2SplitData.csv"
DIRFR2STATESWADI = "./data/processed/FR2States.csv"
DIRCACHE = "./data/processed/cache.csv"


class Task3:
	def splitData(self, variables, interval, ouptutDIR):
		"""
		- var: a list that contains string representations of sensor data names that we want to retain
		- interval: integer interval between datapoints
		- ouputDIR: string DIR of output
		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # number of rows added
		prevVal = 0
		indexList = {}
		currentRow = []


		with open(DIRPROCESSEDWADI) as csvfile0:
			with open(ouptutDIR, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						counter2 += 1

						for i in range(len(row)):
							for j in variables:
								if j in row[i]:
									indexList[j] = i
									currentRow.append(row[i])
									counter1 += 1

						if counter1 != len(variables):
							print("ERROR: Retrieving column index from .csv file")
							break

						print("Reading row {0}; writing: {1}".format(counter0, currentRow))
						spamwriter.writerow(currentRow)
						currentRow.clear()

					elif counter0 - prevVal == interval:
						for i in variables:
							currentRow.append(row[indexList[i]])

						prevVal = counter0
						counter2 += 1

						print("Reading row {0}; writing: {1}".format(counter0, currentRow))
						spamwriter.writerow(currentRow)
						currentRow.clear()

					counter0 += 1

				print("Done. Total read rows: {0}; Total written rows: {1}".format(counter0, counter2))

	def FR2StateCreate(self):
		"""
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		"""
		counter0 = 0
		counter1 = 0
		indexList = {}
		currentRow = []
		prevRow = None
		variables = ["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"]

		with open(DIRFR2SPLIT) as csvfile0:
			with open(DIRFR2STATESWADI, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						for i in range(len(row)):
							for j in variables:
								if j in row[i]:
									indexList[j] = i
									counter1 += 1

						if counter1 != len(variables):
							print("ERROR: Retrieving column index from .csv file, counter1: {0}; len(variables): {1}".format(counter1, len(variables)))
							break

						spamwriter.writerow(row)

					elif counter0 == 1:
						prevRow = row

					else:
						if row[indexList["2_LT_002_PV"]] > prevRow[indexList["2_LT_002_PV"]]:
							currentRow.append(0)
						elif row[indexList["2_LT_002_PV"]] == prevRow[indexList["2_LT_002_PV"]]:
							currentRow.append(1)
						else:
							currentRow.append(2)

						for i in range(1,len(variables)):
							currentRow.append(row[indexList[variables[i]]])

						spamwriter.writerow(currentRow)
						currentRow.clear()
						prevRow = row

					print("Reading row: {0}; Row: {1}".format(counter0, currentRow))
					print("prevRow: {0}".format(prevRow))
					counter0 += 1
					
















Task3().splitData(["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"], 10, DIRFR2SPLIT)
Task3().FR2StateCreate()
















































