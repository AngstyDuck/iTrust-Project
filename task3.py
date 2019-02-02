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
DIRFR6SPLIT = "./data/processed/FR6SplitData.csv"
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
									counter1 += 1
									print(row[i])

						if counter1 != len(variables):
							print("ERROR: Retrieving column index from .csv file. \nNumber of variables provided: {0}; Number of variables found: {1}".format(len(variables), counter1))
							break

						# ensure that first row is added in the same column order as subsequent rows 
						for i in variables:
							currentRow.append(row[indexList[i]])

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
				print(variables)

	def FR2StateCreate(self):
		"""
		Creates state for 2_LT_002_PV, and copies same values for the rest of the columns.
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
						print("Reading row: {0}; Row: {1}".format(counter0, currentRow))
						currentRow.clear()
						prevRow = row

					counter0 += 1
				print(indexList)
					
	def FR2ExpressionVerify(self):
		"""
		Verify expression:
		DP2(Is water level rising?) = DP2(Is water level rising?) AND DP8(output < input)) 
		AND DP8(Is 1_MV_003 open?) AND DP1(Is there input to water tanks?)
		
		Note - States for 2_LT_002_PV
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where ER water level is increasing
		counter3 = 0  # counts number of data points where logical expression is fulfilled
		counter4 = 0  # to count consecutive violations
		violateList = {}
		indexList = {}
		variables = ["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"]

		with open(DIRFR2STATESWADI) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

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

				else:
					if row[indexList["2_LT_002_PV"]] == '0':
						counter2 += 1

						inputMoreOutput = float(row[indexList["2_FIT_001_PV"]]) >= (float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]))
						valveOpen = float(row[indexList["2_MV_003_STATUS"]]) == 2
						inputNotZero = float(row[indexList["2_FIT_001_PV"]]) > 0
						expressionFulfiled = inputMoreOutput and valveOpen and inputNotZero

						if expressionFulfiled:
							counter3 += 1

							# for counting consecutive violations
							if counter4 not in violateList.keys():
								violateList[counter4] = 1
							else:
								violateList[counter4] += 1
							counter4 = 0

						else:
							print("Wrong datapoint - inputMoreOutput: {0}; valveOpen: {1}; inputNotZero: {2};\nRow: {3};".format(inputMoreOutput, valveOpen, inputNotZero, row))

							# for counting consecutive violations
							counter4 += 1

						# print("Progress - counter0: {0}; inputMoreOutput: {1}; valveOpen: {2}; inputNotZero: {3};\nRow: {4};".format(counter0, inputMoreOutput, valveOpen, inputNotZero, row))

				counter0 += 1
				
			print("Results\nTotal number of datapoints: {0}; Datapoints that satisfy expression: {1}; Ratio: {2};\nIndexList: {3};".format(counter2, counter3, counter3/counter2, indexList))
			print("Consecutive violations: {0}".format(violateList))

	def FR6ExpressionVerify(self):
		"""
		DP6(Is booster pump turned on?) == DP8(Total consumption > DP6(Is booster pump turned on?) AND gravity and booster flow input)

		"2_P_003_STATUS" - Whether booster pump is turned on
		"2_FIT_002_PV" - Gravity flow
		"2_FIT_003_PV" - Booster flow
		"TOTAL_CONS_REQUIRED_FLOW" - Total consumption flow

		Results:
		Total number of datapoints: 3325; Datapoints that satisfy expression: 2787; Ratio: 0.8381954887218045
		Consecutive violations: {18: 1, 0: 2537, 2: 46, 3: 24, 1: 143, 7: 6, 4: 14, 6: 5, 5: 5, 9: 2, 11: 1, 14: 1, 8: 2}

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where booster pump is turned on
		counter3 = 0  # counts number of data points where logical expression is fulfilled
		counter4 = 0  # to count consecutive violations
		violateList = {}
		indexList = {}
		variables = ["2_P_003_STATUS", "2_FIT_002_PV", "2_FIT_003_PV", "TOTAL_CONS_REQUIRED_FLOW"]

		with open(DIRFR6SPLIT) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

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

				else:
					if row[indexList["2_P_003_STATUS"]] == '2':  # if pump is turned on
						counter2 += 1

						if float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]) < float(row[indexList["TOTAL_CONS_REQUIRED_FLOW"]]):
							counter3 += 1

							# for counting consecutive violations
							if counter4 not in violateList.keys():
								violateList[counter4] = 1
							else:
								violateList[counter4] += 1
							counter4 = 0

						else:
							print("total input to consumption: {0}; total output from consumption: {1};".format(float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]), float(row[indexList["TOTAL_CONS_REQUIRED_FLOW"]])))

							# for counting consecutive violations
							counter4 += 1


				counter0 += 1

			print("Results -\nTotal number of datapoints: {0}; Datapoints that satisfy expression: {1}; Ratio: {2}".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations: {0}".format(violateList))

	def FR7ExpressionVerify(self):
		pass



# for testing FR2
# Task3().splitData(["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"], 60, DIRFR2SPLIT)
# Task3().FR2StateCreate()
# Task3().FR2ExpressionVerify()

# for testing FR6
# Task3().splitData(["2_P_003_STATUS", "2_FIT_002_PV", "2_FIT_003_PV", "TOTAL_CONS_REQUIRED_FLOW"], 60, DIRFR6SPLIT)
# Task3().FR6ExpressionVerify()

# for testing FR7














































