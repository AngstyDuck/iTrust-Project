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
DIRFR7SPLIT = "./data/processed/FR7SplitData.csv"
DIRFR8SPLIT = "./data/processed/FR8SplitData.csv"
DIRFR2STATESWADI = "./data/processed/FR2States.csv"
DIRFR7STATESWADI = "./data/processed/FR7States.csv"
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
						for j in variables:
							for i in range(len(row)):
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
		Verify expression (there're 2 expressions, each complementary to the other):
		Expression 1
		DP2(Is water level rising?) = DP2(Is water level rising?) AND DP8(output < input)) 
		AND DP8(Is 1_MV_003 open?) AND DP1(Is there input to water tanks?)

		Expression 2
		DP2(Is water level falling?) = DP2(Is water level falling?) AND DP8(output > input))
		
		Note - States for 2_LT_002_PV
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		Results 
		Expression 1
		Total number of datapoints: 10161; Datapoints that violate expression: 2866; Ratio: 0.28205885247515006;
		Expression 2
		Total number of datapoints: 9998; Datapoints that violate expression: 2113; Ratio: 0.21134226845369075;

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where ER water level is increasing for expression 1
		counter3 = 0  # counts number of data points where logical expression is violated for expression 1
		counter4 = 0  # to count consecutive violations for expression 1
		counter5 = 0  # counters number of data points where ER water level is decreasing for expression 2
		counter6 = 0  # counts number of data points where logical expression is violated for expression 2
		counter7 = 0  # to count consecutive violations for expression 2
		consecutiveTresh0 = 15
		consecutiveTresh1 = 1
		violateList0 = {}
		violateList1 = {}
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
					if row[indexList["2_LT_002_PV"]] == '0':  # verifying expression 1
						counter2 += 1

						inputMoreOutput = float(row[indexList["2_FIT_001_PV"]]) > (float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]))
						valveOpen = float(row[indexList["2_MV_003_STATUS"]]) == 2
						inputNotZero = float(row[indexList["2_FIT_001_PV"]]) > 0
						expressionFulfiled = inputMoreOutput and valveOpen and inputNotZero

						if expressionFulfiled:

							# for counting consecutive violations
							if counter4 not in violateList0.keys():
								violateList0[counter4] = 1
							else:
								violateList0[counter4] += 1
							counter4 = 0

						else:
							# print("Expression 0 wrong datapoint - inputMoreOutput: {0}; valveOpen: {1}; inputNotZero: {2};\nRow: {3};".format(inputMoreOutput, valveOpen, inputNotZero, row))

							# for counting consecutive violations
							counter4 += 1

						# print("Progress - counter0: {0}; inputMoreOutput: {1}; valveOpen: {2}; inputNotZero: {3};\nRow: {4};".format(counter0, inputMoreOutput, valveOpen, inputNotZero, row))
					elif row[indexList["2_LT_002_PV"]] == '2':  # verifying expression 2
						counter5 += 1

						outputMoreInput = float(row[indexList["2_FIT_001_PV"]]) < (float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]))

						if outputMoreInput:

							# for counting consecutive violations
							if counter7 not in violateList1.keys():
								violateList1[counter7] = 1
							else:
								violateList1[counter7] += 1
							counter7 = 0

						else:
							# print("Expression 1 wrong datapoint - outputMoreInput: {0};\nRow: {1};".format(outputMoreInput, row))

							# for counting consecutive violations
							counter7 += 1

				counter0 += 1

			for i in violateList0.keys():
				if i > consecutiveTresh0:
					counter3 += violateList0[i]*i
			for i in violateList1.keys():
				if i > consecutiveTresh1:
					counter6 += violateList1[i]*i
				
			print("Results for expression 1\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2};".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations for expression 1: {0}".format(violateList0))
			print("Results for expression 2\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2};".format(counter5, counter6, counter6/counter5))
			print("Consecutive violations for expression 2: {0}".format(violateList1))
			print("indexList: {0}".format(indexList))

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
		consecutiveTresh = 1
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

			if counter4 not in violateList.keys():
				violateList[counter4] = 1
			else:
				violateList[counter4] += 1

			for i in violateList.keys():
				if i > consecutiveTresh:
					counter3 += violateList[i]*i			

			print("Results -\nTotal number of datapoints: {0}; Datapoints that satisfy expression: {1}; Ratio: {2}".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations: {0}".format(violateList))

	def FR7StateCreate(self):
		"""
		Creates state for 2_PIT_002 and whether the number of opened input valves for consumption tanks are increasing/constant/decreasing.
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		"""
		counter0 = 0
		counter1 = 0
		indexList = {}
		currentRow = []
		prevRow = None
		variables = ["2_PIT_002", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"]
		outputVariables = ["2_PIT_002", "pressure_state", "num_open_valves", "open_valves_state"]

		with open(DIRFR7SPLIT) as csvfile0:
			with open(DIRFR7STATESWADI, "w+") as csvfile1:
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

						for i in outputVariables:
							currentRow.append(i)
						
						spamwriter.writerow(currentRow)
						currentRow.clear()

					elif counter0 == 1:
						currentRow.append(row[indexList["2_PIT_002"]])
						
						# to count number of opened input valves for consumption tanks
						num_open_valves = 0
						for i in range(1, len(variables)):
							if float(row[indexList[variables[i]]]) > 0:
								num_open_valves += 1
						
						currentRow.append(num_open_valves)
						currentRow.append(1)  # arbitrary constant state for starting datapoint
						prevRow = copy.copy(currentRow)
						currentRow.clear()

					else:
						currentRow.append(row[indexList["2_PIT_002"]])

						# to determine if water pressure at gravity valve is increasing/const/decreasing
						if float(row[indexList["2_PIT_002"]]) > float(prevRow[indexList["2_PIT_002"]]):
							currentRow.append(0)
						elif float(row[indexList["2_PIT_002"]]) == float(prevRow[indexList["2_PIT_002"]]):
							currentRow.append(1)
						else:
							currentRow.append(2)

						# to count number of opened input valves for consumption tanks
						num_open_valves = 0
						for i in range(1, len(variables)):
							if float(row[indexList[variables[i]]]) > 0:
								num_open_valves += 1
						currentRow.append(num_open_valves)

						# to determine number of valves is increasing/const/decreasing
						if currentRow[1] > prevRow[1]:
							currentRow.append(0)
						elif currentRow[1] == prevRow[1]:
							currentRow.append(1)
						else:
							currentRow.append(2)

						print("Progress: {0}; Writing row: {1}".format(counter0, currentRow))
						prevRow = copy.copy(currentRow)
						spamwriter.writerow(currentRow)
						currentRow.clear()

					counter0 += 1
				print("State creation done.")

	def FR7ExpressionVerify(self):
		"""
		Verifies 2 logical expressions

		Expression 0
		DP7(Did pressure of gravity pump decrease?) == DP7(Did pressure of gravity pump decrease?) AND DP6(Number of opened input valves increase?)

		Note:
		A sizable amount datapoints supports instances where pressure at gravity pump decreasing while number of opened input consumption valves remains constant

		Result:
		Total number of datapoints: 61183; Datapoints that violate expression: 20326; Ratio: 0.3322164653580243;

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where pressure of gravity pump is decreasing for expression 1
		counter3 = 0  # counts number of data points where logical expression is violated for expression 1
		counter4 = 0  # to count consecutive violations for expression
		testcounter = 0
		consecutiveTresh0 = 5
		violateList0 = {}
		indexList = {}
		variables = ["2_PIT_002", "pressure_state", "num_open_valves", "open_valves_state"]

		with open(DIRFR7STATESWADI) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

			for row in spamreader:
				if counter0 == 0:
					print(row)
					for i in range(len(row)):
						for j in variables:
							if j in row[i]:
								indexList[j] = i
								counter1 += 1

					if counter1 != len(variables):
						print("ERROR: Retrieving column index from .csv file, counter1: {0}; len(variables): {1}".format(counter1, len(variables)))
						break

					print(indexList)

				else:
					if float(row[indexList["pressure_state"]]) == 2:
						counter2 += 1

						if float(row[indexList["open_valves_state"]]) == 0:
							# for counting consecutive violations
							if counter4 not in violateList0.keys():
								violateList0[counter4] = 1
							else:
								violateList0[counter4] += 1

							counter4 = 0

						else:
							# for counting consecutive violations
							# if float(row[indexList["2_FIT_002"]]) != 1 and float(row[indexList["2_LT_002"]]) != 1:
							# 	print("Expression 0 violating data point - 2_FIT_002: {0}; 2_LT_002: {1}".format(float(row[indexList["2_FIT_002"]]), float(row[indexList["2_LT_002"]])))
							# 	counter4 += 1
							print("Expression 0 violating datapoint, pressure_state: {0}; open_valves_state: {1}".format(row[indexList["pressure_state"]], row[indexList["open_valves_state"]]))
							counter4 += 1

				counter0 += 1

			if counter4 not in violateList0.keys():
				violateList0[counter4] = 1
			else:
				violateList0[counter4] += 1

			for i in violateList0.keys():
				if i > consecutiveTresh0:
					counter3 += violateList0[i]*i
				
			print("Results for expression 0\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2};".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations for expression 1: {0}".format(violateList0))
			print("indexList: {0}".format(indexList))

	def FR8ExpressionVerify(self):
		"""
		Will be verifying multiple logical expressions.
		
		Expression 0
		True == ( FR8(Is 2_MV_003 open?) AND FR1(Pump into ER2 is turned on) ) XOR ( FR8(Is 2_MV_003 closed?) AND FR1(Pump into ER2 is turned off 1_P_005) ) ) AND FR8(Is 2_MCV_007 closed?)
		Expression 1
		True == (FR8(Is 2_MV_006 turned on?) AND FR6(Is 2_P_003 turned on? ) XOR ( FR8(Is 2_MV_006 turned off?) AND FR6(Is 2_P_003 turned off?) ) AND FR8(Is 2_MCV_007 closed?)
		Expression 2
		FR8(Is 2_MCV_101 > 0) == FR8(Is 2_MCV_101 > 0) AND FR8(Is 2_MV_101 closed?) AND FR8(Is 2_MCV_007 closed?)
		Expression 3
		FR8(Is 2_MCV_201 > 0) == FR8(Is 2_MCV_201 > 0) AND FR8(Is 2_MV_201 closed?) AND FR8(Is 2_MCV_007 closed?)
		Expression 4
		FR8(Is 2_MCV_301 > 0) == FR8(Is 2_MCV_301 > 0) AND FR8(Is 2_MV_301 closed?) AND FR8(Is 2_MCV_007 closed?)
		Expression 5
		FR8(Is 2_MCV_401 > 0) == FR8(Is 2_MCV_401 > 0) AND FR8(Is 2_MV_401 closed?) AND FR8(Is 2_MCV_007 closed?)
		Expression 6
		FR8(Is 2_MCV_501 > 0) == FR8(Is 2_MCV_501 > 0) AND FR8(Is 2_MV_501 closed?) AND FR8(Is 2_MCV_007 closed?)
		Expression 7
		FR8(Is 2_MCV_601 > 0) == FR8(Is 2_MCV_601 > 0) AND FR8(Is 2_MV_601 closed?) AND FR8(Is 2_MCV_007 closed?)


		Result:
		Expression 0 - Total: 20160; Violate: 0; Violate ratio: 0.0;
		Expression 1 - Total: 20160; Violate: 10; Violate ratio: 0.000496031746031746;
		Expression 2 - Total: 9132; Violate: 53; Violate ratio: 0.005803766973280771;
		Expression 3 - Total: 10036; Violate: 48; Violate ratio: 0.004782781984854523;
		Expression 4 - Total: 11663; Violate: 56; Violate ratio: 0.004801509045700077;
		Expression 5 - Total: 8564; Violate: 54; Violate ratio: 0.006305464736104624;
		Expression 6 - Total: 9790; Violate: 51; Violate ratio: 0.0052093973442288045;
		Expression 7 - Total: 10724; Violate: 57; Violate ratio: 0.005315180902648265;
		"""
		counter0 = 0
		counter1 = 0
		totalCounter = [0,0,0,0,0,0,0,0]
		violateCounter = [0,0,0,0,0,0,0,0]
		consecCounter = [0,0,0,0,0,0,0,0]
		consecThresh = [1,1,1,1,1,1,1,1]
		violateList = [{},{},{},{},{},{},{},{}]
		indexList = {}
		variables = ["2_MV_003", "1_P_005_STATUS", "2_MCV_007", "2_MV_006", "2_P_003_STATUS", "2_MCV_101", "2_MV_101_STATUS", "2_MCV_201", "2_MV_201_STATUS", "2_MCV_301", "2_MV_301_STATUS", "2_MCV_401", "2_MV_401_STATUS", "2_MCV_501", "2_MV_501_STATUS", "2_MCV_601", "2_MV_601_STATUS"]

		with open(DIRFR8SPLIT) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

			for row in spamreader:
				if counter0 == 0:
					print(row)
					for j in variables:
						for i in range(len(row)):
							if j in row[i]:
								indexList[j] = i
								counter1 += 1
					if counter1 != len(variables):
						print("ERROR: Retrieving column index from .csv file, counter1: {0}; len(variables): {1}".format(counter1, len(variables)))
						break
				else:
					# Expression 0 and 1
					if float(row[indexList["2_MCV_007"]]) == 0:
						totalCounter[0] += 1
						totalCounter[1] += 1
						expression0 = (float(row[indexList["2_MV_003"]]) == 2 and float(row[indexList["1_P_005_STATUS"]]) == 2) ^ (float(row[indexList["2_MV_003"]]) == 1 and float(row[indexList["1_P_005_STATUS"]]) == 1)
						expression1 = (float(row[indexList["2_MV_006"]]) == 2 and float(row[indexList["2_P_003_STATUS"]]) == 2) ^ (float(row[indexList["2_MV_006"]]) == 1 and float(row[indexList["2_P_003_STATUS"]]) == 1)

						if expression0:
							# for counting consecutive violations
							if consecCounter[0] not in violateList[0].keys():
								violateList[0][consecCounter[0]] = 1
							else:
								violateList[0][consecCounter[0]] += 1
							consecCounter[0] = 0

						else:
							# for counting consecutive violations
							consecCounter[0] += 1

						if expression1:
							# for counting consecutive violations
							if consecCounter[1] not in violateList[1].keys():
								violateList[1][consecCounter[1]] = 1
							else:
								violateList[1][consecCounter[1]] += 1
							consecCounter[1] = 0

						else:
							# for counting consecutive violations
							consecCounter[1] += 1

					# Expression 2
					if float(row[indexList["2_MCV_101"]]) > 0:
						totalCounter[2] += 1

						if float(row[indexList["2_MV_101_STATUS"]]) == 1 and float(row[indexList["2_MCV_007"]]) == 0:
							# for counting consecutive violations
							if consecCounter[2] not in violateList[2].keys():
								violateList[2][consecCounter[2]] = 1
							else:
								violateList[2][consecCounter[2]] += 1
							consecCounter[2] = 0

						else:
							# for counting consecutive violations
							consecCounter[2] += 1

					# Expression 3
					if float(row[indexList["2_MCV_201"]]) > 0:
						totalCounter[3] += 1

						if float(row[indexList["2_MV_201_STATUS"]]) == 1 and float(row[indexList["2_MCV_007"]]) == 0:
							# for counting consecutive violations
							if consecCounter[3] not in violateList[3].keys():
								violateList[3][consecCounter[3]] = 1
							else:
								violateList[3][consecCounter[3]] += 1
							consecCounter[3] = 0

						else:
							# for counting consecutive violations
							consecCounter[3] += 1

					# Expression 4
					if float(row[indexList["2_MCV_301"]]) > 0:
						totalCounter[4] += 1

						if float(row[indexList["2_MV_301_STATUS"]]) == 1 and float(row[indexList["2_MCV_007"]]) == 0:
							# for counting consecutive violations
							if consecCounter[4] not in violateList[4].keys():
								violateList[4][consecCounter[4]] = 1
							else:
								violateList[4][consecCounter[4]] += 1
							consecCounter[4] = 0

						else:
							# for counting consecutive violations
							consecCounter[4] += 1

					# Expression 5
					if float(row[indexList["2_MCV_401"]]) > 0:
						totalCounter[5] += 1

						if float(row[indexList["2_MV_401_STATUS"]]) == 1 and float(row[indexList["2_MCV_007"]]) == 0:
							# for counting consecutive violations
							if consecCounter[5] not in violateList[5].keys():
								violateList[5][consecCounter[5]] = 1
							else:
								violateList[5][consecCounter[5]] += 1
							consecCounter[5] = 0

						else:
							# for counting consecutive violations
							consecCounter[5] += 1

					# Expression 6
					if float(row[indexList["2_MCV_501"]]) > 0:
						totalCounter[6] += 1

						if float(row[indexList["2_MV_501_STATUS"]]) == 1 and float(row[indexList["2_MCV_007"]]) == 0:
							# for counting consecutive violations
							if consecCounter[6] not in violateList[6].keys():
								violateList[6][consecCounter[6]] = 1
							else:
								violateList[6][consecCounter[6]] += 1
							consecCounter[6] = 0

						else:
							# for counting consecutive violations
							consecCounter[6] += 1

					# Expression 7
					if float(row[indexList["2_MCV_601"]]) > 0:
						totalCounter[7] += 1

						if float(row[indexList["2_MV_601_STATUS"]]) == 1 and float(row[indexList["2_MCV_007"]]) == 0:
							# for counting consecutive violations
							if consecCounter[7] not in violateList[7].keys():
								violateList[7][consecCounter[7]] = 1
							else:
								violateList[7][consecCounter[7]] += 1
							consecCounter[7] = 0

						else:
							# for counting consecutive violations
							consecCounter[7] += 1

				counter0 += 1

			for i in range(len(violateList)):
				for j in violateList[i].keys():
					if j > consecThresh[i]:
						violateCounter[i] += violateList[i][j]

			print("Results:")
			for i in range(8):
				print("Expression {0} - Total: {1}; Violate: {2}; Violate ratio: {3};".format(i, totalCounter[i], violateCounter[i], violateCounter[i]/totalCounter[i]))

# for testing FR2
# Task3().splitData(["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"], 60, DIRFR2SPLIT)
Task3().FR2StateCreate()
Task3().FR2ExpressionVerify()

# for testing FR6
# Task3().splitData(["2_P_003_STATUS", "2_FIT_002_PV", "2_FIT_003_PV", "TOTAL_CONS_REQUIRED_FLOW"], 60, DIRFR6SPLIT)
# Task3().FR6ExpressionVerify()

# for testing FR7
# Task3().splitData(["2_PIT_002", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], 10, DIRFR7SPLIT)
# Task3().FR7StateCreate()
# Task3().FR7ExpressionVerify()

# for testing FR8
# Task3().splitData(["2_MV_003", "1_P_005_STATUS", "2_MCV_007", "2_MV_006", "2_P_003_STATUS", "2_MCV_101", "2_MV_101_STATUS", "2_MCV_201", "2_MV_201_STATUS", "2_MCV_301", "2_MV_301_STATUS", "2_MCV_401", "2_MV_401_STATUS", "2_MCV_501", "2_MV_501_STATUS", "2_MCV_601", "2_MV_601_STATUS"], 60, DIRFR8SPLIT)
# Task3().FR8ExpressionVerify()












































