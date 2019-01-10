"""
README
Code objective is to print variance of water level in 2_LT_001 when inlet
and outlet of the tank is closed

Note about dataset:
- ER2 (2_LT_002) is unused for the entire duration. For water level,
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



Tmrw:


"""

import csv
import numpy as np
import copy



DIR2_LT_001 = "./data/processed/2_LT_001Data.csv"
DIR2_LT_002 = "./data/processed/2_LT_002Data.csv"
DIR1_P_005 = "./data/processed/1_P_005Data.csv"
DIR1_P_006 = "./data/processed/1_P_006Data.csv"
DIR1_MV_004 = "./data/processed/1_MV_004Data.csv"
DIR2_FIT_001 = "./data/processed/2_FIT_001Data.csv"
DIR2_FIT_002 = "./data/processed/2_FIT_002Data.csv"
DIR2_FIT_003 = "./data/processed/2_FIT_003Data.csv"

DIRPROCESSEDWADI = "./data/processed/processedWadi.csv"
DIRSTATESWADI = "./data/processed/statesWadi.csv"

DIRFR1SPLIT00 = "./data/processed/FR1SplitData00.csv"
DIRFR1SPLIT01 = "./data/processed/FR1SplitData01.csv"


# CACHEDIR0 = "./task1Cache0.csv"
# CACHEDIR1 = "./task1Cache1.csv"
# CACHEDIR2 = "./task1Cache2.csv"

# states for all valves (except MCVs): "1" for closed, "2" for opened, "0" for transition from one to another
# MCVs open with a percentage

class Task1:
	def checkData(self, inpStr):
		"""
		Verifies certain requirements for data
		- All data have same number of rows
		"""

		counter0=0

		with open(DIRPROCESSEDWADI) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")

			for row in spamreader:
				if counter0 == 0:
					for i in range(len(row)):
						if inpStr in row[i]:
							print(row[i])
					break

	def stateCreationFR2(self):
		"""
		Labels one of 4 states to 2_LT_002 data. 0 when value is zero; 1 when
		value is positive and unchanged; 2 when value is increasing; 3 when
		value is decreasing

		"""
		maxDiff = 0.2622999999999962

		counter0 = 0
		counter1 = 0

		prevVal = 0
		stateList = [0,0,0,0]

		with open(DIR2_LT_002DATASTATES,"w+") as csvfileOut:
			with open(DIR2_LT_002) as csvfile:
				spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfileOut, delimiter=" ", quotechar="|")

				# create pipeline; middle of pipeline is index 15
				for row in spamreader:
					if counter0 != 0:
						if counter0 == 1:
							prevVal = float(row[1])
						elif counter0 > 1:
							difference = float(row[1]) - prevVal
							if float(row[1]) == 0:
								# state 0: value is zero
								spamwriter.writerow([counter0, 0])
								stateList[0] += 1
							elif difference > maxDiff:
								# state 2: value is increasing
								spamwriter.writerow([counter0, 2])
								stateList[2] += 1
							elif difference < (maxDiff * -1):
								# state 3: value is decreasing
								spamwriter.writerow([counter0, 3])
								stateList[3] += 1
							else:
								# state 1: value is unchanged
								spamwriter.writerow([counter0, 1])
								stateList[1] += 1
							prevVal = float(row[1])
					counter0 += 1

				print("Increasing: {0}; Decreasing: {1}; Same Value: {2}".format(stateList[2], stateList[3], stateList[1]))

	def stateCreationFR3(self):
		"""
		Creates 6 different states that sensors 2_FIT_001 - 2_FIT_003 can take.
		Prints out list of all possible states

		stateList: [0, 0, 281855, 927746, 0, 0]

		"""
		variables = ["2_FIT_001", "2_FIT_002", "2_FIT_003"]
		indexList = {}
		statesList = [0,0,0,0,0,0]
		# state 0: in is positive out is zero; state 1: in is zero out is positive
		# state 2: in more than out; state 3: out more than in
		# state 4: in and out are zero; state 5: others
		counter0 = 0
		counter1 = 0

		with open(DIRPROCESSEDWADI) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")

			for row in spamreader:
				# retrieve index of column
				if counter0 == 0:
					for i in range(len(row)):
						for j in variables:
							if j in row[i]:
								indexList[j] = i
								counter1 += 1

					if counter1 != len(variables):
						print("ERROR: Retrieving column index from .csv file")
						print("counter1: {0}; columnNames: {1}; indexList: {2}".format(counter1, columnNames, indexList))
						break
				elif counter0 > 0:
					if row[indexList["2_FIT_001"]] == 0:
						if row[indexList["2_FIT_002"]] == 0 and row[indexList["2_FIT_003"]] == 0:
							statesList[4] += 1
						else:
							statesList[1] += 1
					elif row[indexList["2_FIT_002"]] == 0 and row[indexList["2_FIT_003"]] == 0:
						if row[indexList["2_FIT_001"]] != 0:
							statesList[0] += 1
					elif row[indexList["2_FIT_001"]] > row[indexList["2_FIT_002"]]+row[indexList["2_FIT_003"]]:
						statesList[2] += 1
					elif row[indexList["2_FIT_002"]]+row[indexList["2_FIT_003"]] > row[indexList["2_FIT_001"]]:
						statesList[3] += 1
					else:
						statesList[5] += 1

				counter0 += 1

			print("done.")
			print(statesList)

	def stateCreationFR6(self):
		"""
		Creates 4 different states that sensors 2_FIT_002 - 2_FIT_003 can take.
		Prints out list of all possible states. 2_FIT_002 is gravity flow,
		while 2_FIT_003 is booster pump.

		As long as values are less than 0.08, we'll consider as 0 due to sensor
		noise. This is because the minimum demand from all consumer tanks is
		0.1, and we're considering if the sensor value will be positive or just
		zero.

		For FR6, there are data points that do not make sense. Instances where
		there is a sufficiently high. We will be ignoring these rows, and make
		suitable adjustments to state creation functions
		"""
		variables = ["2_P_003_SPEED","2_FIT_002", "2_FIT_003"]
		indexList = {}
		statesList = [0,0,0,0,0]
		transitionCounter = 0
		transitionDurationDict = {}
		# state 0: neither are used; state 1: booster pump is used
		# state 2: gravity flow is used; state 3: others
		counter0 = 0
		counter1 = 0

		with open(DIRPROCESSEDWADI) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")

			for row in spamreader:
				# retrieve index of column
				if counter0 == 0:
					for i in range(len(row)):
						for j in variables:
							if j in row[i]:
								indexList[j] = i
								counter1 += 1

					if counter1 != len(variables):
						print("ERROR: Retrieving column index from .csv file")
						print("counter1: {0}; columnNames: {1}; indexList: {2}".format(counter1, columnNames, indexList))
						break

				elif counter0 > 0:
					if float(row[indexList["2_FIT_002"]]) < 0.08:
						if float(row[indexList["2_FIT_003"]]) < 0.08:
							if transitionCounter not in transitionDurationDict.keys():
								transitionDurationDict[transitionCounter] = 1
							else:
								transitionDurationDict[transitionCounter] += 1
								transitionCounter = 0

							statesList[0] += 1
						else:
							if transitionCounter not in transitionDurationDict.keys():
								transitionDurationDict[transitionCounter] = 1
							else:
								transitionDurationDict[transitionCounter] += 1
								transitionCounter = 0

							statesList[2] += 1
					elif float(row[indexList["2_FIT_003"]]) < 0.08 and float(row[indexList["2_FIT_002"]]) >= 0.08:
						if transitionCounter not in transitionDurationDict.keys():
							transitionDurationDict[transitionCounter] = 1
						else:
							transitionDurationDict[transitionCounter] += 1
							transitionCounter = 0

						statesList[1] += 1
					elif float(row[indexList["2_FIT_003"]]) >= 0.08 and float(row[indexList["2_FIT_002"]]) >= 0.08:
						transitionCounter += 1
						print("002: {0}; 003: {1}; 2_P_003_SPEED: {2}".format(row[indexList["2_FIT_002"]], row[indexList["2_FIT_003"]], row[indexList["2_P_003_SPEED"]]))
						statesList[4] += 1
					else:
						statesList[3] += 1

				counter0 += 1

			print("done.")
			print(statesList)
			print(transitionDurationDict)

	def stateCreationFR7(self):
		"""
		List down number of data points that have each states
		"""
		variables = ["2_PIT_001"]
		mean = -0.00018657402865699914
		stdDev = 2.4926490652793483
		indexList = {}
		upperThresh = mean + (3*stdDev)
		lowerThresh = mean - (3*stdDev)
		counter0 = 0
		counter1 = 0
		stateList = [0,0,0]  # [more, equals, less]

		with open(DIRPROCESSEDWADI) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")

			for row in spamreader:
				if counter0 == 0:
					for i in range(len(row)):
						for j in variables:
							if j in row[i]:
								indexList[j] = i
								counter1 += 1

					if counter1 != len(variables):
						print("ERROR: Retrieving column index from .csv file")
						print("counter1: {0}; columnNames: {1}; indexList: {2}".format(counter1, columnNames, indexList))
						break
				elif counter0 == 1:
					prevVal = float(row[indexList["2_PIT_001"]])
				elif counter0 > 1:
					currentVal = float(row[indexList["2_PIT_001"]])
					if currentVal - prevVal > upperThresh:
						stateList[0] += 1
					elif currentVal - prevVal < lowerThresh:
						stateList[2] += 1
					else:
						stateList[1] += 1
					prevVal = float(row[indexList["2_PIT_001"]])
				counter0 += 1
			print(stateList)

	def meanStdDevCreationFR7(self):
		"""
		Retrieve 2_PIT_001 data when 1_MV_002, 1_MV_004, 2_MV_006, and 2_MV_005
		is closed. Calculated mean and standard deviation of change in 2_PIT_001
		when 1_MV_002 and 1_MV_004 are closed.

		Mean: -0.00018657402865699914
		Standard Deviation: 2.4926490652793483

		stateList = [233, 1208892, 475]

		"""
		variables = ["1_MV_002", "1_MV_004", "2_MV_005", "2_MV_006", "2_PIT_001", "2_PIT_002", "2_PIT_003"]
		indexList = {}
		counter0 = 0
		counter1 = 0
		counter2 = 0
		addVal = 0
		prevVal = 0
		mean = 0
		stdDev = 0
		# stateList = [0,0,0]  # [more, equals, less]

		with open(DIRPROCESSEDWADI) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
			# retrieve index of column
			for row in spamreader:
				if counter0 == 0:
					for i in range(len(row)):
						for j in variables:
							if j in row[i]:
								indexList[j] = i
								counter1 += 1

					if counter1 != len(variables):
						print("ERROR: Retrieving column index from .csv file")
						print("counter1: {0}; columnNames: {1}; indexList: {2}".format(counter1, columnNames, indexList))
						break
				elif counter0 == 1:
					prevVal = float(row[indexList["2_PIT_001"]])
				elif counter0 > 1:
					if float(row[indexList["1_MV_002"]]) == 1 and float(row[indexList["1_MV_004"]]) == 1:
						addVal += float(row[indexList["2_PIT_001"]]) - prevVal
						counter2 += 1
					prevVal = float(row[indexList["2_PIT_001"]])
				counter0 += 1
			mean = addVal/counter2

		with open(DIRPROCESSEDWADI) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
			addVal = 0
			counter0 = 0
			counter2 = 0
			# retrieve index of column
			for row in spamreader:
				if counter0 == 1:
					prevVal = float(row[indexList["2_PIT_001"]])
				elif counter0 > 1:
					if float(row[indexList["1_MV_002"]]) == 1 and float(row[indexList["1_MV_004"]]) == 1:
						difference = float(row[indexList["2_PIT_001"]]) - prevVal
						addVal += (difference - mean)**2
						counter2 += 1
					else:
						prevVal = float(row[indexList["2_PIT_001"]])
				counter0 += 1
			stdDev = (addVal/counter2)**0.5
		print("mean: {0}; stdDev: {1}".format(mean, stdDev))

	def findMarginFR2(self):
		"""
		Applying on water level sensor of ER1, find the threshold of change in
		main water level. Upper threshold = mean + 3*std deviation;
		Lower threshold = mean + 3*std deviation

		mean: -4.604001322751313e-07
		stdDev = 0.013544393299907025

		"""

		stdDev = 0
		mean = 0
		prevVal = 0


		# retrieve mean value of difference
		with open(DIR2_LT_001) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
			counter = 0
			for row in spamreader:
				if counter == 1:
					prevVal = float(row[1])
				elif counter > 1:
					mean += float(row[1])-prevVal
					prevVal = float(row[1])
				counter += 1
			mean = mean/(counter-2)

		# retrieve standard deviation of difference
		with open(DIR2_LT_001) as csvfile:
			spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
			counter = 0
			for row in spamreader:
				if counter == 1:
					prevVal = float(row[1])
				elif counter > 1:
					difference = float(row[1])-prevVal
					stdDev += (difference-mean)**2
					prevVal = float(row[1])
				counter += 1
			stdDev = (stdDev/(counter-1))**0.5

			print("Mean value: {0}, Std value: {1}".format(mean, stdDev))
			print("Upper threshold: {0}, Lower threshold: {1}".format(mean+(3*stdDev), mean-(3*stdDev)))

	def createStateAllFR2(self):
		"""
		Creates states for columns in processed Wadi where there aren't any.
		FR1: 1_P_005_STATUS
		FR2: 2_LT_002_PV (need create state)
			 state 0: water level increase;
			 state 1: water level constant;
			 state 2: water level decrease;
		FR3: 2_FIT_001, 2_FIT_002, 2_FIT_003 (need create state)
			 state 0: in is positive out is zero;
			 state 1: in is zero out is positive;
			 state 2: in more than out;
			 state 3: out more than in;
			 state 4: in and out are zero;
			 state 5: others;
		FR6: 2_FIT_002, 2_FIT_003 (need create state)
			 state 0: neither are used;
			 state 1: booster pump is used
			 state 2: gravity flow is used;
			 state 3: others - ROW IS SKIPPED
		FR7: 2_PIT_001 (need create state)
			 state 0: water pressure increase;
			 state 1: water pressure constant;
			 state 2: water pressure decrease;
		FR8: 1_MV_004
		"""
		variables = ["1_P_005_STATUS", "2_LT_002_PV", "2_FIT_001", "2_FIT_002",
					 "2_FIT_003", "2_PIT_001", "1_MV_004"]
		currentRow = [0,0,0,0,0,0]
		counter0 = 0
		counter1 = 0
		counter2 = 0
		counter3 = 0
		counter4 = 0
		indexList = {}
		prevVals = [0,0]  # [FR2, FR7]

		FR2Mean = -4.604001322751313e-07
		FR2StdDev = 0.013544393299907025
		FR2UpperThresh = FR2Mean + (3*FR2StdDev)
		FR2LowerThresh = FR2Mean - (3*FR2StdDev)

		FR7Mean = -0.00018657402865699914
		FR7StdDev = 2.4926490652793483
		FR7UpperThresh = FR7Mean + (3*FR7StdDev)
		FR7LowerThresh = FR7Mean - (3*FR7StdDev)

		with open(DIRPROCESSEDWADI) as csvfile0:
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
							print("counter1: {0}; columnNames: {1}; indexList: {2}".format(counter1, columnNames, indexList))
							break

					elif counter0 == 1:
						prevVals = [float(row[indexList["2_LT_002_PV"]]), float(row[indexList["2_PIT_001"]])]

					elif counter0 > 1:
						# FR6
						if float(row[indexList["2_FIT_002"]]) < 0.08:
							if float(row[indexList["2_FIT_003"]]) < 0.08:
								currentRow[3] = 0
							else:
								currentRow[3] = 2
						elif float(row[indexList["2_FIT_003"]]) < 0.08 and float(row[indexList["2_FIT_002"]]) >= 0.08:
							currentRow[3] = 1

						else:
							currentRow = [-1,-1,-1,-1,-1,-1]
							prevVals = [float(row[indexList["2_LT_002_PV"]]), float(row[indexList["2_PIT_001"]])]
							continue

						# FR1
						currentRow[0] = int(row[indexList["1_P_005_STATUS"]])

						# FR2
						differenceFR2 = float(row[indexList["2_LT_002_PV"]]) - prevVals[0]
						if differenceFR2 > FR2UpperThresh:
							currentRow[1] = 0
							counter2 += 1
						elif differenceFR2 < FR2LowerThresh:
							currentRow[1] = 2
							counter3 += 1
						else:
							currentRow[1] = 1
							counter4 += 1

						#FR3
						if float(row[indexList["2_FIT_001"]]) == 0:
							if float(row[indexList["2_FIT_002"]]) == 0 and float(row[indexList["2_FIT_003"]]) == 0:
								currentRow[2] = 4
							else:
								currentRow[2] = 1
						elif float(row[indexList["2_FIT_002"]]) == 0 and float(row[indexList["2_FIT_003"]]) == 0:
							if float(row[indexList["2_FIT_001"]]) != 0:
								currentRow[2] = 0
						elif float(row[indexList["2_FIT_001"]]) > float(row[indexList["2_FIT_002"]])+float(row[indexList["2_FIT_003"]]):
							currentRow[2] = 2
						elif float(row[indexList["2_FIT_002"]])+float(row[indexList["2_FIT_003"]]) > float(row[indexList["2_FIT_001"]]):
							currentRow[2] = 3
						else:
							currentRow[2] = 5

						# FR7
						differenceFR7 = float(row[indexList["2_PIT_001"]]) - prevVals[1]
						if differenceFR7 > FR7UpperThresh:
							currentRow[4] = 0
						elif differenceFR7 < FR7LowerThresh:
							currentRow[4] = 2
						else:
							currentRow[4] = 1

						# FR8
						currentRow[5] = int(row[indexList["1_MV_004"]])

						prevVals = [float(row[indexList["2_LT_002_PV"]]), float(row[indexList["2_PIT_001"]])]

					spamwriter.writerow(currentRow)
					currentRow = [-1,-1,-1,-1,-1,-1]
					counter0 += 1
					print("counter0: {0}".format(counter0))
					print("Increase: {0}; Constant: {1}, Decrease: {2}".format(counter2, counter4, counter3))
				print("done.")


	def splitDatasetFR1(self):
		"""
		Splits dataset into 2 parts, one where 2_MV_003 is closed "DIRFR1SPLIT00", and one where
		2_MV_003 is opened "DIRFR1SPLIT01".

		Note: 
		counter2: 877990, counter3: 329236


		Correct values for increase, constant, decrease (from createStateAllFR2())
		Increase: 75048; Constant: 1055083, Decrease: 76721

		"""
		variables = ["2_MV_003", "2_LT_002_PV"]
		counter0 = 0
		counter1 = 0
		counter2 = 0
		counter3 = 0
		counter4 = 0
		indexList = {}
		prevVals = [0]  # [FR2]

		FR2Mean = -4.604001322751313e-07
		FR2StdDev = 0.013544393299907025
		FR2UpperThresh = FR2Mean + (3*FR2StdDev)
		FR2LowerThresh = FR2Mean - (3*FR2StdDev)


		with open(DIRPROCESSEDWADI) as csvfile0:
			with open(DIRFR1SPLIT00, "w+") as csvfile1:
				with open(DIRFR1SPLIT01, "w+") as csvfile2:
					spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
					spamwriter0 = csv.writer(csvfile1, delimiter=" ", quotechar="|")
					spamwriter1 = csv.writer(csvfile2, delimiter=" ", quotechar="|")

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
								spamwriter0.writerow(row)
								spamwriter1.writerow(row)
						elif counter0 == 1:
							prevVals[0] = float(row[indexList["2_LT_002_PV"]])
						elif counter0 > 1:
							# Giving states to FR2
							differenceFR2 = float(row[indexList["2_LT_002_PV"]]) - prevVals[0]
							if differenceFR2 > FR2UpperThresh:
								row[indexList["2_LT_002_PV"]] = 0
								counter2 += 1
							elif differenceFR2 < FR2LowerThresh:
								row[indexList["2_LT_002_PV"]] = 2
								counter4 += 1
							else:
								row[indexList["2_LT_002_PV"]] = 1
								counter3 += 1

							# Conditional splitting of dataset
							if int(row[indexList["2_MV_003"]]) == 1:
								spamwriter0.writerow(row)
							elif int(row[indexList["2_MV_003"]]) == 2:
								spamwriter1.writerow(row)

							prevVals[0] = float(row[indexList["2_LT_002_PV"]])


						counter0 += 1
						print("counter0: {0}; water level values: {1}".format(counter0, row[indexList["2_LT_002_PV"]]))

					print("increase: {0}; constant: {1}; decrease: {2}".format(counter2, counter3, counter4))


	def checkERValves(self):
		"""
		Print out sum of possible states for 1_MV_001, 1_MV_002, 1_MV_003, 1_MV_004

		Surprisingly results:
		Variable: 1_MV_001; States: {'1': 877990, '0': 2375, '2': 329236}
		Variable: 1_MV_002; States: {'1': 1209601}
		Variable: 1_MV_003; States: {'1': 1209601}
		Variable: 1_MV_004; States: {'1': 866456, '0': 2637, '2': 340508}

		Variable: 2_MV_001; States: {'1': 1209601}
		Variable: 2_MV_002; States: {'1': 1209601}
		Variable: 2_MV_003; States: {'2': 275926, '0': 11897, '1': 921778}
		Variable: 2_MV_004; States: {'2': 1209601}

		Implications: Output from ER2 seemed to be usually larger than input

		This means that neither ER1 nor 2 are constant water levels...?

		"""
		# variables = ["1_MV_001", "1_MV_002", "1_MV_003", "1_MV_004"]
		variables = ["2_MV_001_STATUS", "2_MV_002_STATUS", "2_MV_003_STATUS", "2_MV_004_STATUS"]
		counter0 = 0
		counter1 = 0
		stateList = [{}, {}, {}, {}]
		counter5 = 0
		indexList = {}
		prevVals = [0]  # [FR2]

		FR2Mean = -4.604001322751313e-07
		FR2StdDev = 0.013544393299907025
		FR2UpperThresh = FR2Mean + (3*FR2StdDev)
		FR2LowerThresh = FR2Mean - (3*FR2StdDev)


		with open(DIRPROCESSEDWADI) as csvfile0:
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
				elif counter0 > 0:
					for i in range(len(variables)):
						if row[indexList[variables[i]]] not in stateList[i].keys():
							stateList[i][row[indexList[variables[i]]]] = 1
						else:
							stateList[i][row[indexList[variables[i]]]] += 1
				counter0 += 1

			for i in range(len(stateList)):
				print("Variable: {0}; States: {1}".format(variables[i], stateList[i]))



# execute
task1 = Task1()

# non-state variables
# 2_LT_002_PV (x), 2_FIT_001_PV (x), 2_P_003_SPEED, 2_PIT_001_PV

for i in range(1):
	task1.splitDatasetFR1()




























# fin
