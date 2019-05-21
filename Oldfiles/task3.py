"""
README
Create logical expressions for FR1, FR2, FR6, FR7, and FR8


Note about dataset:
- ER1 (2_LT_001) is unused for the entire duration. For water level,
Max Difference: 0.2622999999999962; Mean Difference: 0.0038681211144183853
Absolute Mean: 70.91059999999999; Absolute mean - min: 0.6424000000000092
- Consumption tanks (e.g. "2_T_101") have sensors that track it's water level
(2_LS_101_AL and 2_LS_101_AH) that switches between 0 and 1. ..AL switches to 1
when water level is below the sensor, ..AH switches to 1 when water level is
above the sensor
- Pumps and valves have 3 different states: 0,1,2. 2 when the pump is on/valve
is open, 1 when the pump is off/valve is closed, 0 when transiting from one
state to another.
- 1_P_005 is either state 1 or state 2; 1_P_006 is state 1. 1_P_006, like all
second pumps, act as a backup pump in case 1_P_005 fails.
- Valves at input and output of elevated tanks are 2_MV_001 to 2_MV_004 (venkat say de). The 
diagram display wrongly (venkat didnt say de)


"""




import csv
import numpy as np
import copy



DIR2_LT_001 = "./data/processed_clean/2_LT_001Data.csv"
DIR2_LT_002 = "./data/processed_clean/2_LT_002Data.csv"
DIR1_P_005 = "./data/processed_clean/1_P_005Data.csv"
DIR2_FIT_001 = "./data/processed_clean/2_FIT_001Data.csv"
DIR1_MV_004 = "./data/processed_clean/1_MV_004Data.csv"
DIR2_FIT_001 = "./data/processed_clean/2_FIT_001Data.csv"
DIR2_FIT_002 = "./data/processed_clean/2_FIT_002Data.csv"
DIR2_FIT_003 = "./data/processed_clean/2_FIT_003Data.csv"

DIRPROCESSEDWADI = "./data/processed_clean/processedWadi.csv"
DIRFR2SPLIT = "./data/processed_clean/FR2SplitData.csv"
DIRFR6SPLIT = "./data/processed_clean/FR6SplitData.csv"
DIRFR7SPLIT = "./data/processed_clean/FR7SplitData.csv"
DIRFR8SPLIT = "./data/processed_clean/FR8SplitData.csv"
DIRFR2STATESWADI = "./data/processed_clean/FR2States.csv"
DIRFR6STATESWADI = "./data/processed_clean/FR6States.csv"
DIRFR7STATESWADI = "./data/processed_clean/FR7States.csv"
DIRCACHE = "./data/processed_clean/cache.csv"


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

						# adding all variables + 2_LT_002_PV_State, and extra column not found in original data
						currentRow.append("water_level_state")
						for i in variables:
							currentRow.append(row[indexList[i]])

						spamwriter.writerow(currentRow)
						currentRow.clear()

					elif counter0 == 1:
						prevRow = row

					else:
						if row[indexList["2_LT_002_PV"]] > prevRow[indexList["2_LT_002_PV"]]:
							currentRow.append(0)
						elif row[indexList["2_LT_002_PV"]] == prevRow[indexList["2_LT_002_PV"]]:
							currentRow.append(1)
						else:
							currentRow.append(2)

						# adding raw value of water level

						for i in range(0,len(variables)):
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
		Expression 0
		DP2(Is water level rising?) = DP2(Is water level rising?) AND DP8(output < input)) 
		AND DP8(Is 1_MV_003 open?) AND DP1(Is there input to water tanks?)

		Expression 1
		DP2(Is water level falling?) = DP2(Is water level falling?) AND DP8(output > input))
		
		Note - States for 2_LT_002_PV
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		Results 
		Threshold: 1
		  Expression 1
		  Total number of datapoints: 10161; Datapoints that violate expression: 2866; Ratio: 0.28205885247515006;
		  Expression 2
		  Total number of datapoints: 9998; Datapoints that violate expression: 2113; Ratio: 0.21134226845369075;
		Threshold: 2
		  Expression 1
		  Total number of datapoints: 60755; Datapoints that violate expression: 42894; Ratio: 0.7060159657641346;
		  Expression 2
		  Total number of datapoints: 60161; Datapoints that violate expression: 20675; Ratio: 0.3436611758448164;
		Threshold: 3
		  Expression 1
		  Total number of datapoints: 60755; Datapoints that violate expression: 42828; Ratio: 0.704929635420953;
		  Expression 2
		  Total number of datapoints: 60161; Datapoints that violate expression: 20360; Ratio: 0.33842522564452054;
		Threshold 4
		  Expression 1
		  Total number of datapoints: 60755; Datapoints that violate expression: 42792; Ratio: 0.7043370915973994;
		  Expression 2
		  Total number of datapoints: 60161; Datapoints that violate expression: 19948; Ratio: 0.3315769352238161;
		Threshold 5
		  Expression 1
		  Total number of datapoints: 60755; Datapoints that violate expression: 42747; Ratio: 0.7035964118179574;
		  Expression 2
		  Total number of datapoints: 60161; Datapoints that violate expression: 19478; Ratio: 0.3237645650836921;

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where ER water level is increasing for expression 1
		counter3 = 0  # counts number of data points where logical expression is violated for expression 1
		counter4 = 0  # to count consecutive violations for expression 1
		counter5 = 0  # counters number of data points where ER water level is decreasing for expression 2
		counter6 = 0  # counts number of data points where logical expression is violated for expression 2
		counter7 = 0  # to count consecutive violations for expression 2
		consecViolate0 = False
		consecViolate1 = False
		consecutiveTresh0 = 5
		consecutiveTresh1 = 5
		violateList0 = {}
		violateList1 = {}
		indexList = {}
		variables = ["water_level_state", "2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"]

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
					if row[indexList["water_level_state"]] == '0':  # verifying expression 1
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
							consecViolate0 = False

						else:
							print("Expression 0 wrong datapoint - Consecutive violate?: {0}; inputMoreOutput: {1}; valveOpen: {2}; inputNotZero: {3};\nRow: {4};".format(consecViolate0, inputMoreOutput, valveOpen, inputNotZero, row))

							# for counting consecutive violations
							counter4 += 1
							consecViolate0 = True

						# print("Progress - counter0: {0}; inputMoreOutput: {1}; valveOpen: {2}; inputNotZero: {3};\nRow: {4};".format(counter0, inputMoreOutput, valveOpen, inputNotZero, row))
					
					elif row[indexList["water_level_state"]] == '2':  # verifying expression 2
						counter5 += 1

						outputMoreInput = float(row[indexList["2_FIT_001_PV"]]) < (float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]))

						if outputMoreInput:

							# for counting consecutive violations
							if counter7 not in violateList1.keys():
								violateList1[counter7] = 1
							else:
								violateList1[counter7] += 1
							counter7 = 0
							consecViolate1 = False

						else:
							# print("Expression 1 wrong datapoint - Consecutive violate?: {0}; outputMoreInput: {1};\nRow: {2};".format(consecViolate1, outputMoreInput, row))

							# for counting consecutive violations
							counter7 += 1
							consecViolate1 = True

				counter0 += 1

			for i in violateList0.keys():
				if i > consecutiveTresh0:
					counter3 += violateList0[i]*i
			for i in violateList1.keys():
				if i > consecutiveTresh1:
					counter6 += violateList1[i]*i
			
			print("indexList: {0}".format(indexList))	
			print("Results for expression 1\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2};".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations for expression 1: {0}".format(violateList0))
			print("Results for expression 2\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2};".format(counter5, counter6, counter6/counter5))
			print("Consecutive violations for expression 2: {0}".format(violateList1))

	def FR6ExpressionVerify(self):
		"""
		WARNING - NUMBER OF VIOLATING DATAPOINTS IS TOO HIGH

		DP6(Is booster pump turned on?) == DP8(Total consumption > Total output from ER) AND DP6(Is booster pump turned on?)

		"2_P_003_STATUS" - Whether booster pump is turned on
		"2_FIT_002_PV" - Gravity flow
		"2_FIT_003_PV" - Booster flow
		"TOTAL_CONS_REQUIRED_FLOW" - Total consumption flow

		Results:
		Threshold: 1
		  Total number of datapoints: 3325; Datapoints that violate expression: 394; Ratio: 0.11849624060150377
		Threshold: 2
		  Total number of datapoints: 3325; Datapoints that violate expression: 302; Ratio: 0.09082706766917294
	  	Threshold: 3
		  Total number of datapoints: 3325; Datapoints that violate expression: 230; Ratio: 0.06917293233082707

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where booster pump is turned on
		counter3 = 0  # counts number of data points where logical expression is violated
		counter4 = 0  # to count consecutive violations
		consecutiveTresh = 3
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

			print("Results -\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2}".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations: {0}".format(violateList))

	def FR6StateCreate1(self):
		"""
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		DP6(Is booster pump turned on?) == DP6(Is booster pump turned on?) AND DP2(Water level of consumer tank is not "high" state) AND DP2(ER water level of elevated tank is not increasing) AND DP7(Booster pump pressure does not increase) DP3(Booster pump flow does not decrease?)

		"2_P_003_STATUS" - Whether booster pump is turned on
		"2_FIT_003_PV" - Booster flow
		"2_FIT_003_STATUS" - Booster flow state
		"2_PIT_003" - Pressure level of booster pump
		"Booster_pressure_state" - State of pressure level of booster pump
		"2_LT_002" - Water level of elevated tank
		"ER_water_level_state" - State of water level of elevated tank 
		"2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH" - Water level of consumer tank
		"Number of consumer tanks with high water level" - total consumer tanks at 'high' state
		"State of high water level consumer tanks" - State of total consumer tanks at 'high' state

		"""
		counter0 = 0
		counter1 = 0
		indexList = {}
		currentRow = []
		prevRow = None

		variables = ["2_P_003_STATUS", "2_FIT_003_PV", "2_PIT_003", "2_LT_002", "2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH"]
		outputVariables = ["2_P_003_STATUS", "2_FIT_003_PV", "2_FIT_003_STATUS", "2_PIT_003", "Booster_pressure_state", "2_LT_002", "ER_water_level_state", "Number of consumer tanks with high water level", "State of high water level consumer tanks"]

		with open(DIRFR6SPLIT) as csvfile0:
			with open(DIRFR6STATESWADI, "w+") as csvfile1:
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
						highWaterLevelCounter = 0

						for i in ["2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH"]:
							if row[indexList[i]] == "1":
								highWaterLevelCounter += 1
								print("PING")
						
						prevRow = copy.copy(row)
						prevRow.append(highWaterLevelCounter)
						prevRow.append(None)  # State of high water level consumer tanks

					else:
						for i in ["2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH"]:
							if row[indexList[i]] == "1":
								highWaterLevelCounter += 1
								print("PING")

						currentRow.append(row[indexList["2_P_003_STATUS"]])

						currentRow.append(row[indexList["2_FIT_003_PV"]])						
						if row[indexList["2_FIT_003_PV"]] > prevRow[indexList["2_FIT_003_PV"]]:
							currentRow.append("0")
						elif row[indexList["2_FIT_003_PV"]] == prevRow[indexList["2_FIT_003_PV"]]:
							currentRow.append("1")
						else:
							currentRow.append("2")

						currentRow.append(row[indexList["2_PIT_003"]])
						if row[indexList["2_PIT_003"]] > prevRow[indexList["2_PIT_003"]]:
							currentRow.append("0")
						elif row[indexList["2_PIT_003"]] == prevRow[indexList["2_PIT_003"]]:
							currentRow.append("1")
						elif row[indexList["2_PIT_003"]] < prevRow[indexList["2_PIT_003"]]:
							currentRow.append("2")

						currentRow.append(row[indexList["2_LT_002"]])
						if row[indexList["2_LT_002"]] > prevRow[indexList["2_LT_002"]]:
							currentRow.append("0")
						elif row[indexList["2_LT_002"]] == prevRow[indexList["2_LT_002"]]:
							currentRow.append("1")
						else:
							currentRow.append("2")

						highWaterLevelCounter = 0
						for i in ["2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH"]:
							if row[indexList[i]] == "1":
								highWaterLevelCounter += 1
								print("PING")

						currentRow.append(str(highWaterLevelCounter))
						if highWaterLevelCounter > prevRow[-2]:
							currentRow.append("0")
						elif highWaterLevelCounter == prevRow[-2]:
							currentRow.append("1")
						else:
							currentRow.append("2")

						print(currentRow)
						spamwriter.writerow(currentRow)
						currentRow.clear()

						prevRow = copy.copy(row)
						prevRow.append(highWaterLevelCounter)
						prevRow.append(None)  # State of high water level consumer tanks

					counter0 += 1

	def FR6ExpressionVerify1(self):
		"""
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		DP6(Is booster pump turned on?) == DP6(Is booster pump turned on?) AND DP2(Water level of consumer tank is not "high" state) AND DP2(ER water level of elevated tank is not increasing) AND DP7(Booster pump pressure does not increase) AND DP3(Booster pump flow does not decrease?)

		"2_P_003_STATUS" - Whether booster pump is turned on
		"2_FIT_003_PV" - Booster flow
		"2_FIT_003_STATUS" - Booster flow state
		"2_PIT_003" - Pressure level of booster pump
		"Booster_pressure_state" - State of pressure level of booster pump
		"2_LT_002" - Water level of elevated tank
		"ER_water_level_state" - State of water level of elevated tank 
		"2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH" - Water level of consumer tank
		"Number of consumer tanks with high water level" - total consumer tanks at 'high' state
		"State of high water level consumer tanks" - State of total consumer tanks at 'high' state

		Threshold: 1
		Total number of datapoints: 3325; Datapoints that violate expression: 2799; Ratio: 0.8418045112781954
		Threshold: 2
		Total number of datapoints: 3325; Datapoints that violate expression: 2705; Ratio: 0.8135338345864662
		Threshold: 3
		Total number of datapoints: 3325; Datapoints that violate expression: 2609; Ratio: 0.7846616541353384


		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where booster pump is turned on
		counter3 = 0  # counts number of data points where logical expression is violated
		counter4 = 0  # to count consecutive violations
		consecutiveTresh = 3
		violateList = {}
		indexList = {}
		combiViolate = {}
		variables = ["2_P_003_STATUS", "2_FIT_003_PV", "2_FIT_003_STATUS", "2_PIT_003", "Booster_pressure_state", "2_LT_002", "ER_water_level_state", "Number of consumer tanks with high water level", "State of high water level consumer tanks"]

		with open(DIRFR6STATESWADI) as csvfile0:
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
					if row[indexList["2_P_003_STATUS"]] == "2":
						counter2 += 1
						# logicalExpressionFulfilled = row[indexList["Number of consumer tanks with high water level"]] == "0" and row[indexList["ER_water_level_state"]] != "0" and row[indexList["Booster_pressure_state"]] != "0" and row[indexList["2_FIT_003_STATUS"]] != "2"

						# For testing condition, and collecting combinations of violations
						instanceCombiViolate = ""
						if row[indexList["Number of consumer tanks with high water level"]] == "0":
							pass
						else:
							instanceCombiViolate += "0,"
						if row[indexList["ER_water_level_state"]] != "0":
							pass
						else:
							instanceCombiViolate += "1,"
						if row[indexList["Booster_pressure_state"]] != "0":
							pass
						else:
							instanceCombiViolate += "2,"
						if row[indexList["2_FIT_003_STATUS"]] != "2":
							pass
						else:
							instanceCombiViolate += "3,"

						if instanceCombiViolate not in combiViolate.keys():
							combiViolate[instanceCombiViolate] = 1
						else:
							combiViolate[instanceCombiViolate] += 1
						# ----

						if instanceCombiViolate == "":
						# if logicalExpressionFulfilled:

							# for counting consecutive violations
							if counter4 not in violateList.keys():
								violateList[counter4] = 1
							else:
								violateList[counter4] += 1
							counter4 = 0

						else:
							print("Number of consumer tanks with high water level: {0}; ER_water_level_state: {1}; Booster_pressure_state: {2}; 2_FIT_003_STATUS: {3}".format(float(row[indexList["Number of consumer tanks with high water level"]]), float(row[indexList["ER_water_level_state"]]), float(row[indexList["Booster_pressure_state"]]), float(row[indexList["2_FIT_003_STATUS"]])))

							# For counting consecutive violations
							counter4 += 1

				counter0 += 1

			# For counting consecutive violations
			if counter4 not in violateList.keys():
				violateList[counter4] = 1
			else:
				violateList[counter4] += 1

			for i in violateList.keys():
				if i > consecutiveTresh:
					counter3 += violateList[i]*i

			print("Results -\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2}".format(counter2, counter3, counter3/counter2))
			
			# For counting consecutive violations
			print("Consecutive violations: {0}".format(violateList))

			# For counting combinations of violations
			print("---- Combinations of violations ----")
			print("Assuming \n0 - 'Number of consumer tanks with high water level'; \n1 - 'ER_water_level_state'; \n2 - 'Booster_pressure_state'; \n3 - '2_FIT_003_STATUS'")
			print(combiViolate)


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
		variables = ["2_PIT_002", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "2_FIT_002", "2_FIT_003"]
		outputVariables = ["2_PIT_002", "pressure_state", "total_output", "output_state", "total_open_valves", "open_valves_state"]

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
						currentRow.append(None)  # space filler for 'pressure state'
						
						currentRow.append(float(row[indexList["2_FIT_002"]])+float(row[indexList["2_FIT_003"]]))
						currentRow.append(None)  # space filler for 'output_state'

						# to count number of opened input valves for consumption tanks
						total_open_valves = 0
						for i in range(1, len(variables)-2):
							total_open_valves += float(row[indexList[variables[i]]])
						currentRow.append(total_open_valves)
						currentRow.append(None)  # space filler for 'open_valves_state'

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

						currentRow.append(float(row[indexList["2_FIT_002"]]) + float(row[indexList["2_FIT_003"]]))
						
						# determine if total output from ER is increasing/decreasing/constant
						if float(row[indexList["2_FIT_002"]]) + float(row[indexList["2_FIT_003"]]) > float(prevRow[2]):
							currentRow.append(0)
						elif float(row[indexList["2_FIT_002"]]) + float(row[indexList["2_FIT_003"]])== float(prevRow[2]):
							currentRow.append(1)
						else:
							currentRow.append(2)

						# to count number of opened input valves for consumption tanks
						total_open_valves = 0
						for i in range(1, len(variables)-2):
							total_open_valves += float(row[indexList[variables[i]]])
						currentRow.append(total_open_valves)

						# to determine number of valves is increasing/const/decreasing
						if currentRow[4] > prevRow[4]:
							currentRow.append(0)
						elif currentRow[4] == prevRow[4]:
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
		DP7(Did pressure of gravity pump decrease?) == DP7(Did pressure of gravity pump decrease?) AND DP6(total percentage of opened input valves increase?) AND DP6(Total flow increase?)

		Note:
		A sizable amount datapoints supports instances where pressure at gravity pump decreasing while number of opened input consumption valves remains constant

		Result:
		Threshold: 1
		  Total number of datapoints: 11464; Datapoints that violate expression: 7018; Ratio: 0.6121772505233776;
		Threshold: 2
		  Total number of datapoints: 11464; Datapoints that violate expression: 6374; Ratio: 0.5560013956734124;
		Threshold: 3
		  Total number of datapoints: 11464; Datapoints that violate expression: 5759; Ratio: 0.5023551988834613;
		Threshold: 4
		  Total number of datapoints: 11464; Datapoints that violate expression: 5163; Ratio: 0.45036636427076066;
		Threshold: 5
		  Total number of datapoints: 11464; Datapoints that violate expression: 4553; Ratio: 0.3971563154221912;

		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where pressure of gravity pump is decreasing for expression 1
		counter3 = 0  # counts number of data points where logical expression is violated for expression 1
		counter4 = 0  # to count consecutive violations for expression
		consecViolate = False
		consecutiveTresh0 = 5
		violateList0 = {}
		indexList = {}
		variables = ["2_PIT_002", "pressure_state", "total_output", "output_state", "total_open_valves", "open_valves_state"]

		with open(DIRFR7STATESWADI) as csvfile0:
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
					if float(row[indexList["pressure_state"]]) == 2:
						counter2 += 1

						if float(row[indexList["open_valves_state"]]) == 0 and float(row[indexList["output_state"]]) == 0:
							# for counting consecutive violations
							if counter4 not in violateList0.keys():
								violateList0[counter4] = 1
							else:
								violateList0[counter4] += 1

							consecViolate = False
							counter4 = 0

						else:
							# for counting consecutive violations
							# if float(row[indexList["2_FIT_002"]]) != 1 and float(row[indexList["2_LT_002"]]) != 1:
							# 	print("Expression 0 violating data point - 2_FIT_002: {0}; 2_LT_002: {1}".format(float(row[indexList["2_FIT_002"]]), float(row[indexList["2_LT_002"]])))
							# 	counter4 += 1
							print("-> Expression 0 violating datapoint, consecViolate?: {0}; pressure_state: {1}; output_state: {2}; open_valves_state: {3}\nrow: {4}".format(consecViolate, row[indexList["pressure_state"]], row[indexList["output_state"]], row[indexList["open_valves_state"]], row))
							consecViolate = True
							counter4 += 1

				counter0 += 1

			if counter4 not in violateList0.keys():
				violateList0[counter4] = 1
			else:
				violateList0[counter4] += 1

			for i in violateList0.keys():
				if i > consecutiveTresh0:
					counter3 += violateList0[i]*i
			
			print("indexList: {0}".format(indexList))	
			print("Results for expression 0\nTotal number of datapoints: {0}; Datapoints that violate expression: {1}; Ratio: {2};".format(counter2, counter3, counter3/counter2))
			print("Consecutive violations for expression 1: {0}".format(violateList0))

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
# Task3().splitData(["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"], 10, DIRFR2SPLIT)
# Task3().FR2StateCreate()
# Task3().FR2ExpressionVerify()

# for testing FR6
# Task3().splitData(["2_P_003_STATUS", "2_FIT_002_PV", "2_FIT_003_PV", "TOTAL_CONS_REQUIRED_FLOW"], 60, DIRFR6SPLIT)
# Task3().FR6ExpressionVerify()

# NEW for testing FR6
# Task3().splitData(["2_P_003_STATUS", "2_FIT_003_PV", "2_PIT_003", "2_LT_002", "2_LS_101_AH", "2_LS_201_AH", "2_LS_301_AH", "2_LS_401_AH", "2_LS_501_AH", "2_LS_601_AH"], 60, DIRFR6SPLIT)
Task3().FR6StateCreate1()
Task3().FR6ExpressionVerify1()

# for testing FR7
# Task3().splitData(["2_PIT_002", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "2_FIT_002", "2_FIT_003"], 60, DIRFR7SPLIT)
# Task3().FR7StateCreate()
# Task3().FR7ExpressionVerify()

# for testing FR8
# Task3().splitData(["2_MV_003", "1_P_005_STATUS", "2_MCV_007", "2_MV_006", "2_P_003_STATUS", "2_MCV_101", "2_MV_101_STATUS", "2_MCV_201", "2_MV_201_STATUS", "2_MCV_301", "2_MV_301_STATUS", "2_MCV_401", "2_MV_401_STATUS", "2_MCV_501", "2_MV_501_STATUS", "2_MCV_601", "2_MV_601_STATUS"], 60, DIRFR8SPLIT)
# Task3().FR8ExpressionVerify()












































