"""
Explore new dataset 'WADI_attackdata_October.txt'

Note: All results will be in relation with data of a hacked system

"""

import csv
import numpy as np
import copy


raw_data_dir = "./data/Wadi_data/WADI_attackdata_October.txt"
dest_data_dir = "./data/processed_dirty/WADI_attackdata_October.csv"

DIRPROCESSEDWADI = "./data/processed_dirty/WADI_attackdata_October.csv"

DIRFR1SPLIT = "./data/processed_dirty/FR1SplitData.csv"
DIRFR6SPLIT = "./data/processed_dirty/FR6SplitData.csv"
DIRFR8SPLIT = "./data/processed_clean/FR8SplitData.csv"

DIRSTATESWADI = "./data/processed_dirty/statesWadi2.csv"
DIRCACHE = "./data/processed_dirty/cache.csv"

DIRFR6DATATIMESPLIT = "./data/processed_dirty/FR6dataTimeSplit.csv"
DIRFR8DATATIMESPLIT = "./data/processed_dirty/FR8dataTimeSplit.csv"



class Task4:

	def csvCreate(self):
		"""
		Converts txt file into csv file
		"""
		with open(dest_data_dir, "w+") as writefile0:
			with open(raw_data_dir, "r") as readfile0:
			
				counter0 = 0
				counter1 = 0  # count number of rows printed

				spamwriter = csv.writer(writefile0, delimiter=" ", quotechar="|")


				for line in readfile0:
					if (counter0 >= 4):
						input_list = line.split(",")
						input_list[-1] = input_list[-1].split("\n")[0]  # remove "\n" at the end of every row
						spamwriter.writerow(input_list)

						print(input_list)
						counter1 += 1

					counter0 += 1

				print("done. Number of rows: {0}".format(counter1))

	def extractDatapoints(self, startTime, endTime, dir):

		# process time
		def convertString(inp):
			inp = copy.deepcopy(inp)
			inp = inp.split(" ")
			amORpm = None
			
			inp[0] = inp[0].split("/")
			inp[1] = inp[1].split(":")

			if (int(inp[1][0]) > 12):
				amORpm = "PM"
				inp[1][0] = str(int(inp[1][0])-12)
			else:
				amORpm = "AM"

			return (inp[0][1]+"/"+inp[0][0]+"/2017", ":".join(inp[1]), amORpm)

		startTime = convertString(startTime)  # (date, time, am or pm)
		endTime = convertString(endTime)  # (date, time, am or pm)

		counter0 = 0
		counter1 = 0
		counter2 = 0  # number of rows added
		writeState = False
		indexList = {}
		variables = ["Date", "Time"]

		with open(DIRPROCESSEDWADI) as csvfile0:
			with open(dir, "w+") as csvfile1:
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
							print("ERROR: Retrieving column index from .csv file. \nNumber of variables provided: {0}; Number of variables found: {1}".format(len(variables), counter1))
							break	

						spamwriter.writerow(row)

					else:
						if not writeState:
							dateFulfilled = (startTime[0] in row[indexList["Date"]])
							timeFulfiled = (startTime[1] in row[indexList["Time"]]) and (startTime[2] in row[indexList["Time"]])
							if (dateFulfilled and timeFulfiled):
								writeState = True
						else:
							dateFulfilled = (endTime[0] in row[indexList["Date"]])
							timeFulfiled = (endTime[1] in row[indexList["Time"]]) and (endTime[2] in row[indexList["Time"]])
							if (dateFulfilled and timeFulfiled):
								writeState = False
								break
							else:
								spamwriter.writerow(row)
								counter2 += 1
					
					print("Progress: {0}".format(counter0))
					counter0 += 1

		print("Done. {0} rows added".format(counter2))

	def FR1reduceSize(self):
		"""
		Only store one datapoint per 10 datapoints (from processedWadi)
		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0
		prevCount = 0

		with open(DIRPROCESSEDWADI) as csvfile0:
			with open(DIRFR1SPLIT, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0 or counter0 - prevCount == 60:
						spamwriter.writerow(row)
						prevCount = counter0
						counter2 += 1
					counter0 += 1

		print("reduceSize done. Original size of datapoints: {0}; Reduced size of datapoints: {1}".format(counter0, counter2))

	def FR1stateCreation(self):
		"""
		Replaces statesWadi2 with one where water level of ER2 are states. Compares water level 
		with previous datapoint to determine if water level is increasing/decreasing/constant. 
		
		state: 0 -> Increase
		state: 1 -> Constant
		state: 2 -> Decrease


		"""
		counter0 = 0
		counter1 = 0
		prevVal = None
		currentRow = None
		variables = ["2_LT_002_PV"]
		indexList = {}

		# write new rows into cache
		with open(DIRFR1SPLIT) as csvfile0:
			with open(DIRSTATESWADI, "w+") as csvfile1:
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
							print("ERROR: Retrieving column index from .csv file")
							break

						spamwriter.writerow(row)

					elif counter0 == 1:
						prevVal = round(float(row[indexList["2_LT_002_PV"]]), 5)
						spamwriter.writerow(row)
					else:
						FR2State = None

						if round(float(row[indexList["2_LT_002_PV"]]), 5) > prevVal:
							FR2State = 0
						elif prevVal == round(float(row[indexList["2_LT_002_PV"]]), 5):
							FR2State = 1
						else:
							FR2State = 2

						prevVal = copy.copy(round(float(row[indexList["2_LT_002_PV"]]), 5))
						currentRow = copy.copy(row)
						currentRow[indexList["2_LT_002_PV"]] = FR2State
						# print("For counter0: {0}, FR2 state changed to: {1}".format(counter0, currentRow[indexList["2_LT_002_PV"]]))
						spamwriter.writerow(currentRow)

					counter0 += 1

		print("stateCreation done.")

	def FR1part0Expression(self):
		"""
		Proves part 0 of the FR1 logic expression

		DP1(Is there input to water tanks?) = (DP8(Is 1_MV_003 open?) AND DP1(Is there input to water tanks?) AND 
		(DP2(Is water level rising?) AND DP8(output < input)) OR 
		(DP2(Is water level falling?) AND DP8(output > input > 0)) OR 
		DP2(Is water level constant?) AND DP8(output = input > 0))
		)) 

		input to water tank: 2_FIT_001
		output from water tank: 2_FIT_002, 2_FIT_003

		Result: 
		Threshold: 1
		  All datapoints where 2_MV_003_STATUS is open: 637; Datapoints when expression is satisfied: 630; Ratio: 0.989010989010989
		Threshold: 2
		  All datapoints where 2_MV_003_STATUS is open: 637; Datapoints when expression is satisfied: 633; Ratio: 0.9937205651491365
		Threshold: 3
		  All datapoints where 2_MV_003_STATUS is open: 637; Datapoints when expression is satisfied: 636; Ratio: 0.9984301412872841
		Threshold: 4
		  All datapoints where 2_MV_003_STATUS is open: 637; Datapoints when expression is satisfied: 636; Ratio: 0.9984301412872841
		Threshold: 5
		  All datapoints where 2_MV_003_STATUS is open: 637; Datapoints when expression is satisfied: 637; Ratio: 1.0

		"""

		counter0 = 0
		counter1 = 0
		counter2 = 0  # all cases where 1_MV_003 is open
		counter3 = 0  # sum of total violating datapoints
		counter4 = 0  # counting consecutive violations
		counter5 = 0  # counting length of consecutive violations
		consecutiveViolation = False
		variables = ["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"]
		indexList = {}
		consecViolationLength = {}
		consecViolationDisplayList = []
		consecViolationThresh = 5  # only consider an official violation when there are >[insert number] consecutive violations

		with open(DIRSTATESWADI) as csvfile0:
			with open(DIRFR1SPLIT) as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamreader1 = csv.reader(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					anotherRow = spamreader1.__next__()

					if counter0 == 0:
						for i in range(len(row)):
							for j in variables:
								if j in row[i]:
									indexList[j] = i
									counter1 += 1

						if counter1 != len(variables):
							print("ERROR: Retrieving column index from .csv file")
							break
					elif counter0 > 1:
						if int(row[indexList["2_MV_003_STATUS"]]) == 2:
							counter2 += 1

							inputWaterTank = round(float(row[indexList["2_FIT_001_PV"]]),5)> 0
							waterLevelRising = round(float(row[indexList["2_LT_002_PV"]]), 5) == 0
							outputLessInput = round(float(row[indexList["2_FIT_002_PV"]]), 5) + round(float(row[indexList["2_FIT_003_PV"]]), 5) < round(float(row[indexList["2_FIT_001_PV"]]), 5)
							waterLevelFalling = round(float(row[indexList["2_LT_002_PV"]]), 5) == 2
							outputMoreInput = round(float(row[indexList["2_FIT_002_PV"]]), 5) + round(float(row[indexList["2_FIT_003_PV"]]), 5) > round(float(row[indexList["2_FIT_001_PV"]]), 5) > 0
							waterLevelConst = round(float(row[indexList["2_LT_002_PV"]]), 5) == 1
							outputEqlInput = round(float(row[indexList["2_FIT_002_PV"]]), 5) + round(float(row[indexList["2_FIT_003_PV"]]), 5) == round(float(row[indexList["2_FIT_001_PV"]]), 5) > 0

							logExpOutput = inputWaterTank and ((waterLevelRising and outputLessInput) or (waterLevelFalling and outputMoreInput) or (waterLevelConst and outputEqlInput))


							if logExpOutput:
								# --- When expression is obeyed
								consecutiveViolation = False
								consecViolationDisplayList.clear()

								# add consecutive violations to dictionary
								if counter5 not in consecViolationLength.keys():
									consecViolationLength[counter5] = 1
								else:
									consecViolationLength[counter5] += 1
								counter5 = 0
								# ----

							else:
								# --- When expression is not obeyed
								if consecutiveViolation:
									counter4 += 1
									display = "Consecutive Violation - inputWaterTank: {0}; waterLevelRising: {1}; outputLessInput: {2}; waterLevelFalling: {3}; outputMoreInput: {4}; waterLevelConst: {5}; outputEqlInput: {6}\nWater level: {7}; Total Output: {8}; Total Input: {9}; Row: {10}\n".format(inputWaterTank,waterLevelRising,outputLessInput,waterLevelFalling,outputMoreInput,waterLevelConst,outputEqlInput,anotherRow[indexList["2_LT_002_PV"]], float(anotherRow[indexList["2_FIT_002_PV"]]) + float(anotherRow[indexList["2_FIT_003_PV"]]), float(anotherRow[indexList["2_FIT_001_PV"]]), counter0+1)
									consecViolationDisplayList.append(display)
									# print(display)
								else:
									display = "Non-Consecutive Violation - inputWaterTank: {0}; waterLevelRising: {1}; outputLessInput: {2}; waterLevelFalling: {3}; outputMoreInput: {4}; waterLevelConst: {5}; outputEqlInput: {6}\nWater level: {7}; Total Output: {8}; Total Input: {9}; Row: {10}\n".format(inputWaterTank,waterLevelRising,outputLessInput,waterLevelFalling,outputMoreInput,waterLevelConst,outputEqlInput,anotherRow[indexList["2_LT_002_PV"]], float(anotherRow[indexList["2_FIT_002_PV"]]) + float(anotherRow[indexList["2_FIT_003_PV"]]), float(anotherRow[indexList["2_FIT_001_PV"]]), counter0+1)
									consecViolationDisplayList.append(display)
									# print(display)
									consecutiveViolation = True

								counter5 += 1  # counting length of consecutive violations

								if counter5 == 3:
									for i in consecViolationDisplayList:
										print(i)
									# print("Row number when violations happen 5 times consecutively: {0}".format(counter0+1))  # counter0+1 cos rows start at index 1
						else:
							# --- When input valve to ER2 is not opened
							consecutiveViolation = False
							consecViolationDisplayList.clear()

							# add consecutive violations to dictionary
							if counter5 not in consecViolationLength.keys():
								consecViolationLength[counter5] = 1
							else:
								consecViolationLength[counter5] += 1
							counter5 = 0
							# ----

					counter0 += 1

				print("--- output report ---")
				# removing consecutive violations that are within acceptable threshold
				for i in consecViolationLength.keys():
					if i > consecViolationThresh:
						counter3 += consecViolationLength[i]
						print("Violation length: {0}; Violation occurence: {1}".format(i, consecViolationLength[i]))

				print("All datapoints where 2_MV_003_STATUS is open: {0}; Datapoints when expression is satisfied: {1}; Ratio: {2}".format(counter2, counter2-counter3, (counter2-counter3)/counter2))
				print("Number of consecutive violations: {0}".format(counter3))
				print("--- end ---")

	def splitData(self, variables, interval, inputDIR, ouptutDIR):
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


		with open(inputDIR) as csvfile0:
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
		  Total number of datapoints: 433; Datapoints that violate expression: 60; Ratio: 0.13856812933025403
		Threshold: 2
		  Total number of datapoints: 433; Datapoints that violate expression: 40; Ratio: 0.09237875288683603
	  	Threshold: 3
		  Total number of datapoints: 433; Datapoints that violate expression: 28; Ratio: 0.06466512702078522

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of data points where booster pump is turned on
		counter3 = 0  # counts number of data points where logical expression is violated
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
		Expression 0 - Total: 2854; Violate: 1; Violate ratio: 0.000350385423966363;
		Expression 1 - Total: 2854; Violate: 4; Violate ratio: 0.001401541695865452;
		Expression 2 - Total: 1376; Violate: 9; Violate ratio: 0.006540697674418605;
		Expression 3 - Total: 1519; Violate: 9; Violate ratio: 0.005924950625411455;
		Expression 4 - Total: 1527; Violate: 9; Violate ratio: 0.005893909626719057;
		Expression 5 - Total: 1204; Violate: 8; Violate ratio: 0.006644518272425249;
		Expression 6 - Total: 1465; Violate: 8; Violate ratio: 0.005460750853242321;
		Expression 7 - Total: 1415; Violate: 10; Violate ratio: 0.007067137809187279;

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

# Task4().csvCreate()
# Task4().FR1reduceSize()
# Task4().FR1stateCreation()
# Task4().FR1part0Expression()

# for testing FR1



# for testing FR8
# Task4().extractDatapoints("10/10/17 17:40:00", "10/10/17 17:49:40", DIRFR8DATATIMESPLIT)
# Task4().splitData(["2_MV_003", "1_P_005_STATUS", "2_MCV_007", "2_MV_006", "2_P_003_STATUS", "2_MCV_101", "2_MV_101_STATUS", "2_MCV_201", "2_MV_201_STATUS", "2_MCV_301", "2_MV_301_STATUS", "2_MCV_401", "2_MV_401_STATUS", "2_MCV_501", "2_MV_501_STATUS", "2_MCV_601", "2_MV_601_STATUS"], 1, DIRFR8DATATIMESPLIT, DIRFR8SPLIT)
Task4().FR8ExpressionVerify()

# for testing FR6
# Task4().extractDatapoints(DIRFR6DATATIMESPLIT)
# Task4().splitData(["2_P_003_STATUS", "2_FIT_002_PV", "2_FIT_003_PV", "TOTAL_CONS_REQUIRED_FLOW"], 1, DIRFR6DATATIMESPLIT, DIRFR6SPLIT)
# Task4().FR6ExpressionVerify()


# for extracting attacked data
# print(Task4().extractDatapoints())


