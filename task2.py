"""
Second iteration of creation of state values, and checking if they adhere to axiomatic matrices


"""

import csv
import numpy as np
import copy
from decimal import Decimal



DIR2_LT_001 = "./data/processed_clean/2_LT_001Data.csv"
DIR2_LT_002 = "./data/processed_clean/2_LT_002Data.csv"
DIR1_P_005 = "./data/processed_clean/1_P_005Data.csv"
DIR2_FIT_001 = "./data/processed_clean/2_FIT_001Data.csv"
DIR1_MV_004 = "./data/processed_clean/1_MV_004Data.csv"
DIR2_FIT_001 = "./data/processed_clean/2_FIT_001Data.csv"
DIR2_FIT_002 = "./data/processed_clean/2_FIT_002Data.csv"
DIR2_FIT_003 = "./data/processed_clean/2_FIT_003Data.csv"

DIRPROCESSEDWADI = "./data/processed_clean/processedWadi.csv"
DIRFR1SPLIT = "./data/processed_clean/FR1SplitData.csv"
DIRSTATESWADI = "./data/processed_clean/statesWadi2.csv"
DIRCACHE = "./data/processed_clean/cache.csv"


class Task2:
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
		When interval between data points == 10:
		All datapoints where 2_MV_003_STATUS is open: 27567; 
		Datapoints when expression is satisfied: 17987; 
		Ratio: 0.6524830413175173

		When interval between data points == 60:
		All datapoints where 2_MV_003_STATUS is open: 4590; 
		Datapoints when expression is satisfied: 3744; 
		Ratio: 0.8156862745098039
		
		Threshold: 1
		  All datapoints where 2_MV_003_STATUS is open: 4590; Datapoints when expression is satisfied: 4543; Ratio: 0.989760348583878
		Threshold: 2
		  All datapoints where 2_MV_003_STATUS is open: 4590; Datapoints when expression is satisfied: 4578; Ratio: 0.9973856209150327
		Threshold: 3
		  All datapoints where 2_MV_003_STATUS is open: 4590; Datapoints when expression is satisfied: 4586; Ratio: 0.9991285403050109
		Threshold: 4
		  All datapoints where 2_MV_003_STATUS is open: 4590; Datapoints when expression is satisfied: 4589; Ratio: 0.9997821350762527
		Threshold: 5
		  All datapoints where 2_MV_003_STATUS is open: 4590; Datapoints when expression is satisfied: 4590; Ratio: 1.0

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









task2 = Task2()
# task2.FR1reduceSize()
# task2.FR1stateCreation()
# task2.FR1part0Expression()







































































