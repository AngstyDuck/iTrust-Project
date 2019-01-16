"""
Second iteration of creation of state values, and checking if they adhere to axiomatic matrices


"""

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
DIRSTATESWADI = "./data/processed/statesWadi2.csv"
DIRCACHE = "./data/processed/cache.csv"

DIRFR1SPLIT00 = "./data/processed/FR1SplitData00.csv"
DIRFR1SPLIT01 = "./data/processed/FR1SplitData01.csv"


class Task2:
	def reduceSize(self):
		"""
		Only store one datapoint per 10 datapoints (from processedWadi)
		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0
		prevCount = 0

		with open(DIRPROCESSEDWADI) as csvfile0:
			with open(DIRSTATESWADI, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0 or counter0 - prevCount == 10:
						spamwriter.writerow(row)
						prevCount = counter0
						counter2 += 1
					counter0 += 1

		print("Done. Original size of datapoints: {0}; Reduced size of datapoints: {1}".format(counter0, counter2))

	def stateCreation(self):
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
		with open(DIRSTATESWADI) as csvfile0:
			with open(DIRCACHE, "w+") as csvfile1:
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
						prevVal = row[indexList["2_LT_002_PV"]]
					else:
						FR2State = None

						if prevVal > row[indexList["2_LT_002_PV"]]:
							FR2State = 0
						elif prevVal == row[indexList["2_LT_002_PV"]]:
							FR2State = 1
						else:
							FR2State = 2

						prevVal = copy.copy(row[indexList["2_LT_002_PV"]])
						currentRow = copy.copy(row)
						currentRow[indexList["2_LT_002_PV"]] = FR2State
						# print("For counter0: {0}, FR2 state changed to: {1}".format(counter0, currentRow[indexList["2_LT_002_PV"]]))
						spamwriter.writerow(currentRow)

					counter0 += 1

		# write cache to replace DIRSTATESWADI
		print("Writing into file...")
		with open(DIRCACHE) as csvfile0:
			with open(DIRSTATESWADI, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					spamwriter.writerow(row)

		print("done.")


	def fr1part0Expression(self):
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
		All datapoints where 1_MV_003 is open: 32926; 
		Datapoints when expression is satisfied: 6254 
		Ratio: 0.18994107999757032

		"""

		counter0 = 0
		counter1 = 0
		counter2 = 0  # all cases where 1_MV_003 is open
		counter3 = 0  # when expression is satisfied
		consecutiveViolation = False
		variables = ["2_LT_002_PV", "2_MV_003_STATUS", "2_FIT_001_PV", "2_FIT_002_PV", "2_FIT_003_PV"]
		indexList = {}

		with open(DIRSTATESWADI) as csvfile0:
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
				elif int(row[indexList["2_MV_003_STATUS"]]) == 2:
					counter2 += 1

					inputWaterTank = float(row[indexList["2_FIT_001_PV"]]) > 0
					waterLevelRising = float(row[indexList["2_LT_002_PV"]]) == 0
					outputLessInput = float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]) < float(row[indexList["2_FIT_001_PV"]])
					waterLevelFalling = float(row[indexList["2_LT_002_PV"]]) == 2
					outputMoreInput = float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]) > float(row[indexList["2_FIT_001_PV"]]) > 0
					waterLevelConst = float(row[indexList["2_LT_002_PV"]]) == 1
					outputEqlInput = float(row[indexList["2_FIT_002_PV"]]) + float(row[indexList["2_FIT_003_PV"]]) == float(row[indexList["2_FIT_001_PV"]]) > 0

					logExpOutput = inputWaterTank and ((waterLevelRising and outputLessInput) or (waterLevelFalling and outputMoreInput) or (waterLevelConst and outputEqlInput))


					if logExpOutput:
						consecutiveViolation = False
						counter3 += 1
					else:
						if consecutiveViolation:
							print("Consecutive Violation - inputWaterTank: {0}; waterLevelRising: {1}; outputLessInput: {2}; waterLevelFalling: {3}; outputMoreInput: {4}; waterLevelConst: {5}; outputEqlInput: {6}".format(inputWaterTank,waterLevelRising,outputLessInput,waterLevelFalling,outputMoreInput,waterLevelConst,outputEqlInput))
						else:
							print("Non-consecutive Violation - inputWaterTank: {0}; waterLevelRising: {1}; outputLessInput: {2}; waterLevelFalling: {3}; outputMoreInput: {4}; waterLevelConst: {5}; outputEqlInput: {6}".format(inputWaterTank,waterLevelRising,outputLessInput,waterLevelFalling,outputMoreInput,waterLevelConst,outputEqlInput))
							consecutiveViolation = True
						print("\n")


				counter0 += 1

			print("All datapoints where 2_MV_003_STATUS is open: {0}; Datapoints when expression is satisfied: {1} Ratio: {2}".format(counter2, counter3, counter3/counter2))











task2 = Task2()
# task2.reduceSize()
# task2.stateCreation()
task2.fr1part0Expression()







































































