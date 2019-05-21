"""
07/5/19
- Try having 5 buckets: mean +- 2 stddev; mean +- 1 stddev (if the datapoints already don't follow when we bucket them into 3 buckets, how will bucketing into 5 buckets make things better?)

(discuss solutions with venkat)
- double check value of pump for FR1 - if the value is discrete why are we calculating mean and std =.=


for 2 std dev:
- FR1 the very prominent dip happened in datapoint 3760 to datapoint 4097
- FR8 the very prominent dip happened in datapoint 3760 to datapoint 4142



"""

import csv
import numpy as np
import copy
import matplotlib
matplotlib.use("Qt5Agg")  # specify backend for matplotlib
import matplotlib.pyplot as plt



class Task5:

	def csvCreate(self):
		"""
		Converts txt file into csv file. The directory of the txt file would be assigned to raw_data_dir,
		and the directory of the destination file will be assigned to dest_data_dir
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


	def convertString(self, inp):
		"""
		Used in conjunction with attack_table_WADI.pdf, converts the text in "Starting Time"/"Ending Time"
		into a formatted turple.
		e.g. "9/10/17 19:25:00" --> ("9/10/2017", "7:25:00PM")

		Returns (date, time, am or pm)
		"""

		inp = copy.deepcopy(inp)
		inp = inp.split(" ")
		amORpm = None
		
		inp[0] = inp[0].split("/")
		inp[1] = inp[1].split(":")

		if (int(inp[1][0]) > 12):
			amORpm = "PM"
			inp[1][0] = str(int(inp[1][0])-12)
		elif (int(inp[1][0]) == 12):
			amORpm = "PM"
			inp[1][0] = str(12)
		else:
			amORpm = "AM"

		return (inp[0][1]+"/"+inp[0][0]+"/2017", ":".join(inp[1]), amORpm)


	def extractDatapoints(self, input_dir, output_dir, startTime, endTime):
		"""
		Retrieve datapoints that are within startTime and endTime (copied directly from "Starting Time" and 
		"Ending Time" in attack_table_WADI.pdf). Extract these datapoints from input_dir and write them into
		output_dir.

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file
		:startTime: Datapoints after this time will be extracted
		:endTime: Datapoints after this will not be extracted

		"""

		startTime = self.convertString(startTime)  # (date, time, am or pm)
		endTime = self.convertString(endTime)  # (date, time, am or pm)

		counter0 = 0
		counter1 = 0
		counter2 = 0  # number of rows added
		writeState = False
		indexList = {}
		variables = ["Date", "Time"]

		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
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


	def calStats(self, input_dir, variables, proportion=1.0):
		"""
		Returns a dictionary where each key is the name of the sensor/motor, and each corresponding value is
		[mean, standard deviation, max value, min value]

		:input_dir: String representing the directory of the input file
		:variables: a list of names of sensors/motors that we'll be calculating values from.
		:proportion: proportion of datapoints that will be used to calculate the statistics. We'll be using the
			first portion of the data points for calculation. E.g. if proportion==0.6, the first 60% of the 
			datapoints are used to calculate the variable's mean and standard deviation.

		"""
		counter0 = 0
		counter1 = 0
		totalRow = 0  # total number of rows in the csv file
		endRow = 0  # row to end calculation
		indexList = {}
		counterDict = {}
		statsDict = {}

		for i in variables:
			statsDict[i] = [0,0,0,9999999]  # [mean, standard deviation, max, min]
			counterDict[i] = [0,0,0,0]   # [sum of all, sum of (difference with mean)^2]

		# calculate total number of rows
		with open(input_dir) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

			for row in spamreader:
				totalRow += 1

			endRow = int(totalRow * proportion)  # rounded down

		# calculate mean, max, and min
		print("Calculating mean, max and min...")
		with open(input_dir) as csvfile0:
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
				elif counter0 <= endRow:
					for i in variables:
						counterDict[i][0] += float(row[indexList[i]])

						# max and min
						if float(row[indexList[i]]) > statsDict[i][2]:
							statsDict[i][2] = float(row[indexList[i]])
						if float(row[indexList[i]]) < statsDict[i][3]:
							statsDict[i][3] = float(row[indexList[i]])
				else:
					break

				counter0 += 1
		for i in variables:
			statsDict[i][0] = counterDict[i][0]/counter0


		# calculate standard deviation
		print("Calculating standard deviation...")
		with open(input_dir) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

			counter0 = 0
			for row in spamreader:
				if counter0 != 0:
					if counter0 <= endRow:
						for i in variables:
							counterDict[i][1] += (float(row[indexList[i]]) - statsDict[i][0])**2
					else:
						# where counter0 > endRow
						break
				else:
					# where counter0 == 0
					pass
				
				counter0 += 1

		for i in variables:
			statsDict[i][1] = (counterDict[i][1]/counter0)**0.5

		for i in variables:
			print("Variable:{0};Mean:{1};Standard Deviation:{2};Max:{3};Min:{4};".format(i, statsDict[i][0], statsDict[i][1], statsDict[i][2], statsDict[i][3]))

		return statsDict


	def createIndexList(self, row, variables):
		"""
		Returns indexList for all functions. indexList is a dictionary where the key is the name of the 
		sensor/motor, and the value is its index within the row.

		:row: first row of csvfile
		:variables: variables to retrieve index from
		"""
		counter0 = 0
		indexList = {}

		for j in variables:
			for i in range(len(row)):
				if j in row[i]:
					indexList[j] = i
					counter0 += 1
		if counter0 != len(variables):
			print("ERROR: Retrieving column index from .csv file, counter1: {0}; len(variables): {1}".format(counter1, len(variables)))
			return

		return indexList


	def returnList(self, input_dir, output_dir):
		"""
		returnList writes a row of "1"s (if datapoint follows logical expression) and "0"s (if datapoint does
		not follow logical expression), and a row of date and time corresponding to the datapoint (in the 
		previous row) that share the same index.

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file
		"""
		variables = ["Date", "Time", "Output"]
		indexList = {}
		output = []
		output_timedate = []
		counter0 = 0
		testCounter = 0

		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)

					else:
						output.append(row[indexList["Output"]])
						output_timedate.append(row[indexList["Time"]]+";"+row[indexList["Date"]])

					counter0 += 1

				print("returnList complete, number of datapoints written: {0}".format(counter0-1))
				spamwriter.writerow(output)
				spamwriter.writerow(output_timedate)


	def FR1stateCreation(self, input_dir, output_dir, statsDict, numberStdDev=2):
		"""
		Assign the column values of each datapoint to state 1, 2, and 3 depending on the upper and lower 
		bounds of each column values.

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file
		:statsDict: The dictionary output of the function calStats()
		:numberStdDev: The number of standard deviations from the mean which represents the upper and 
			lower bounds. Values above the upper bound, below the lower bound, and in between, make up
			the three possible states a datapoint will have.

		"""
		counter0 = 0
		counter1 = 0
		indexList = {}
		variables = ["Date", "Time", "1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"]


		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						row += ["water_pump_state", "water_level_state", "mcv_state", "water_pump_value", "water_level_value", "mcv_value"]
						spamwriter.writerow(row)
					else:
						addToWrite = [0,0,0]

						water_pump_value = float(row[indexList["1_P_005"]])
						if water_pump_value < statsDict["1_P_005"][0]-(numberStdDev*statsDict["1_P_005"][1]):
							addToWrite[0] = 0
						elif water_pump_value < statsDict["1_P_005"][0]+(numberStdDev*statsDict["1_P_005"][1]):
							addToWrite[0] = 1
						else:
							addToWrite[0] = 2

						water_level_value = float(row[indexList["2_LT_002_PV"]])
						if water_level_value < statsDict["2_LT_002_PV"][0]-numberStdDev*statsDict["2_LT_002_PV"][1]:
							addToWrite[1] = 0
						elif water_level_value < statsDict["2_LT_002_PV"][0]+numberStdDev*statsDict["2_LT_002_PV"][1]:
							addToWrite[1] = 1
						else:
							addToWrite[1] = 2

						mcvMean = (statsDict["2_MCV_101"][0] + statsDict["2_MCV_201"][0] + statsDict["2_MCV_301"][0] + statsDict["2_MCV_401"][0] + statsDict["2_MCV_501"][0] + statsDict["2_MCV_601"][0])
						mcvStdDev = (statsDict["2_MCV_101"][1]**2 + statsDict["2_MCV_201"][1]**2 + statsDict["2_MCV_301"][1]**2 + statsDict["2_MCV_401"][1]**2 + statsDict["2_MCV_501"][1]**2 + statsDict["2_MCV_601"][1]**2)**0.5
						mcv_value = float(row[indexList["2_MCV_101"]]) + float(row[indexList["2_MCV_201"]]) + float(row[indexList["2_MCV_301"]]) + float(row[indexList["2_MCV_401"]]) + float(row[indexList["2_MCV_501"]]) + float(row[indexList["2_MCV_601"]])
						if mcv_value < mcvMean - numberStdDev*mcvStdDev:
							addToWrite[2] = 0
						elif mcv_value < mcvMean + numberStdDev*mcvStdDev:
							addToWrite[2] = 1
						else:
							addToWrite[2] = 2

						row += addToWrite
						row += [water_pump_value, water_level_value, mcv_value]
						spamwriter.writerow(row)

					counter0 += 1
				print("mcv - mean: {0}, stddev: {1}".format(mcvMean, mcvStdDev))
				print("state creation done")


	def FR1ExpressionVerify(self, input_dir, output_dir):
		"""
		Assigns value of "1" if logical expression is not violated, "0" otherwise.

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file

		Logical Expression:
		state of pump1 to ER == state of water level of ER == state of sum of "open-ness" (expressed in percentage) 
		of consumer tank inlets
		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of datapoints that are relevant and follow expression
		indexList = {}
		variables = ["Date", "Time", "1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "water_pump_state", "water_level_state", "mcv_state", "water_pump_value", "water_level_value", "mcv_value"]
		output_variables = ["Date", "Time", "Output", "water_pump_state", "water_level_state", "mcv_state", "water_pump_value", "water_level_value", "mcv_value"]

		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						spamwriter.writerow(output_variables)  # for first row in output csv file

					else:
						if row[indexList["water_pump_state"]]==row[indexList["water_level_state"]] and row[indexList["water_pump_state"]]==row[indexList["mcv_state"]]:
							counter2 += 1
							spamwriter.writerow([row[indexList["Date"]], 
								row[indexList["Time"]], 
								"1", 
								row[indexList["water_pump_state"]], 
								row[indexList["water_level_state"]], 
								row[indexList["mcv_state"]], 
								row[indexList["water_pump_value"]], 
								row[indexList["water_level_value"]], 
								row[indexList["mcv_value"]]])
						else:
							spamwriter.writerow([row[indexList["Date"]], 
								row[indexList["Time"]], 
								"0",
								row[indexList["water_pump_state"]], 
								row[indexList["water_level_state"]], 
								row[indexList["mcv_state"]], 
								row[indexList["water_pump_value"]], 
								row[indexList["water_level_value"]], 
								row[indexList["mcv_value"]]])

					counter0 += 1

				print("Done. Number of datapoints that follow expression: {0}, Ratio: {1}".format(counter2, counter2/counter0))


	def FR8stateCreation(self, input_dir, output_dir, statsDict, numberStdDev=2):
		"""
		Assign the column values of each datapoint to state 1, 2, and 3 depending on the upper and lower 
		bounds of each column values.

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file
		:statsDict: The dictionary output of the function calStats()
		:numberStdDev: The number of standard deviations from the mean which represents the upper and 
			lower bounds. Values above the upper bound, below the lower bound, and in between, make up
			the three possible states a datapoint will have.

		"""
		waterLevelLimit = None;  # a threshold. water level above 
		counter0 = 0
		counter1 = 0
		indexList = {}
		variables = ["Date", "Time", "2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"]

		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						row += ["water_level_state", "consumption_state", "mcv_state", "water_level_value", "consumption_value", "mcv_value"]
						spamwriter.writerow(row)

					else:
						addToWrite = [0,0,0]

						water_level_value = float(row[indexList["2_LT_002_PV"]])
						if water_level_value < statsDict["2_LT_002_PV"][0]-(numberStdDev*statsDict["2_LT_002_PV"][1]):
							addToWrite[0] = 0
						elif water_level_value < statsDict["2_LT_002_PV"][0]+(numberStdDev*statsDict["2_LT_002_PV"][1]):
							addToWrite[0] = 1
						else:
							addToWrite[0] = 2

						consumption_value = float(row[indexList["2_FIT_002"]]) + float(row[indexList["2_FIT_003"]])
						if consumption_value < (statsDict["2_FIT_002"][0]+statsDict["2_FIT_003"][0])-numberStdDev*(((statsDict["2_FIT_002"][1]**2)+(statsDict["2_FIT_003"][1]**2))**0.5):
							addToWrite[1] = 0
						elif consumption_value < (statsDict["2_FIT_002"][0]+statsDict["2_FIT_003"][0])+numberStdDev*(((statsDict["2_FIT_002"][1]**2)+(statsDict["2_FIT_003"][1]**2))**0.5):
							addToWrite[1] = 1
						else:
							addToWrite[1] = 2

						mcvMean = (statsDict["2_MCV_101"][0] + statsDict["2_MCV_201"][0] + statsDict["2_MCV_301"][0] + statsDict["2_MCV_401"][0] + statsDict["2_MCV_501"][0] + statsDict["2_MCV_601"][0])
						mcvStdDev = (statsDict["2_MCV_101"][1]**2 + statsDict["2_MCV_201"][1]**2 + statsDict["2_MCV_301"][1]**2 + statsDict["2_MCV_401"][1]**2 + statsDict["2_MCV_501"][1]**2 + statsDict["2_MCV_601"][1]**2)**0.5
						mcv_value = float(row[indexList["2_MCV_101"]]) + float(row[indexList["2_MCV_201"]]) + float(row[indexList["2_MCV_301"]]) + float(row[indexList["2_MCV_401"]]) + float(row[indexList["2_MCV_501"]]) + float(row[indexList["2_MCV_601"]])
						if mcv_value < mcvMean - numberStdDev*mcvStdDev:
							addToWrite[2] = 0
						elif mcv_value < mcvMean + numberStdDev*mcvStdDev:
							addToWrite[2] = 1
						else:
							addToWrite[2] = 2

						row += addToWrite
						row += [water_level_value, consumption_value, mcv_value]
						spamwriter.writerow(row)

					counter0 += 1
					# print("Progress: {0}".format(counter0))
				print("State Creation done")


	def FR8ExpressionVerify(self, input_dir, output_dir):
		"""
		Assigns value of "1" if logical expression is not violated, "0" otherwise.

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file

		state of water level of ER == state of gravity meter water flow == state of sum of % of "open-ness" of consumer tank inlets
		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of datapoints that follow expression
		indexList = {}
		variables = ["Date", "Time", "2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "water_level_state", "consumption_state", "mcv_state", "water_level_value", "consumption_value", "mcv_value"]
		output_variables = ["Date", "Time", "Output", "water_level_state", "consumption_state", "mcv_state", "water_level_value", "consumption_value", "mcv_value"]

		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						spamwriter.writerow(output_variables)  # for first row of output csv file

					else:
						if row[indexList["water_level_state"]]==row[indexList["consumption_state"]] and row[indexList["water_level_state"]]==row[indexList["mcv_state"]]:
							counter2 += 1
							spamwriter.writerow([row[indexList["Date"]], 
								row[indexList["Time"]], 
								"1", 
								row[indexList["water_level_state"]], 
								row[indexList["consumption_state"]], 
								row[indexList["mcv_state"]], 
								row[indexList["water_level_value"]], 
								row[indexList["consumption_value"]], 
								row[indexList["mcv_value"]]])
						else:
							spamwriter.writerow([row[indexList["Date"]], 
								row[indexList["Time"]], 
								"0", 
								row[indexList["water_level_state"]], 
								row[indexList["consumption_state"]], 
								row[indexList["mcv_state"]], 
								row[indexList["water_level_value"]], 
								row[indexList["consumption_value"]], 
								row[indexList["mcv_value"]]])

					counter0 += 1

				print("Done. Number of datapoints that follow expression: {0}, Ratio: {1}".format(counter2, counter2/counter0))


	def GraphCreateResult(self, input_dir, output_dir):
		"""
		Returns csv file, where each datapoint indicates "1" under "Output" when an attack is happening, "0" otherwise

		:input_dir: String representing the directory of the input file
		:output_dir: String representing the directory of the output file

		"""
		counter0 = 0
		counter1 = 0
		attackTiming = []
		stateList = []  # represent True/False depending on whether current datapoint is between some attack timing
		indexList = {}
		variables = ["Date", "Time"]
		output_variables = ["Date", "Time", "Output"]

		testCounter = 0  # count number of times its a timing start/end point

		for i in ATTACKTIMING:
			attackTiming.append([self.convertString(i[0]), self.convertString(i[1])])
			stateList.append(0)

		with open(input_dir) as csvfile0:
			with open(output_dir, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						spamwriter.writerow(output_variables)
					else:
						for i in range(len(ATTACKTIMING)):
							startEndState = [False, False]  # represent if time and date of datapoint == that of start/end time

							for j in range(2):
								dateFulfilled = False
								timeFulfiled = False

								if attackTiming[i][j][0] in row[indexList["Date"]]:
									dateFulfilled = True
								if attackTiming[i][j][1] in row[indexList["Time"]]:
									if attackTiming[i][j][2] in row[indexList["Time"]]:
										timeFulfiled = True

								if dateFulfilled and timeFulfiled:
									testCounter += 1
									startEndState[j] = True

							# if datapoint is either at start/end point
							# each element in stateList represent an attack. if the state of the element is 1, that attack is being conducted
							if startEndState[0] != startEndState[1]:
								# if datapoint is at start point and state of attack timing is "has not started yet"
								if startEndState[0] and not stateList[i]==1:
									stateList[i] = 1

								# if datapoint is at end point and state of attack timing is "has already started"
								elif startEndState[1] and stateList[i]==1:
									stateList[i] = 0

								# if datapoint is neither at start nor end point
								elif not startEndState[0] and not startEndState[1]:
									pass

								else:
									print("startEndState error! startEndState[0]: {0}; startEndState[1]: {1}; Attack timing is in progress: {2}".format(startEndState[0], startEndState[1], stateList[i]))
									return

							# if any of the attacks are happening, state of output should be 1, otherwise 0
							outputColumnValue = sum(stateList)
							if outputColumnValue > 1:  # if there're more than one attack happening, set the state of output as 1
								outputColumnValue = 1

						addedRow = [row[indexList["Date"]], row[indexList["Time"]]] + [outputColumnValue]
						spamwriter.writerow(addedRow)
						print(addedRow)
					counter0 += 1
				print("Graph Create End.")
				print("testCounter: {0}".format(testCounter))


	def TotalTest(self, dirty_data_dir, fr_result_dir):
		"""
		Checks that all csv files contain same number of datapoints, returns True if this test passes, False otherwise
		
		:dirty_data_dir: String of dir of DIRGRAPHRESULT
		:fr_result_dir: a dictionary that contains {name of FR:string value of dir of result}. All csv files are expected to have same number of datapoints
		"""
		counterList = []
		dir_list = [dirty_data_dir]


		# populate list with dirs from fr_result_dir
		for i in fr_result_dir.keys():
			dir_list.append(fr_result_dir[i])

		for i in dir_list:
			counter0 = 0

			with open(i) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

				for row in spamreader:
					counter0 += 1

			counterList.append(counter0)

		if len(counterList) >= 2:
			output = True

			# print("--- TotalTest results ---")
			# if all elements in counterList is the same, output remains True
			for i in range(len(dir_list)):
				# print("file: {0}, length: {1}".format(dir_list[i], counterList[i]))
				output  = output and (counterList[0] == counterList[i])
			# print("--- TotalTest result end ---")

			return output

		else:
			print("There're less than 2 dirs provided in total")
			return


	def TotalStats(self, dirty_data_dir, fr_result_dir, testPass, testOrder, FRrelation):
		"""
		Counts number of False positive, True positive, False negative, True negative
		Attack is defined as positive.

		:dirty_data_dir: directory of the dirty data after formatted by the function returnList()
		:fr_result_dir: directory where key is name of FR, and value is the output of the FR from the 
			returnList() function
		:testPass: output from the function TotalTest()
		:testOrder: A list of FRs representing the FRs attacked as detailed by attack_table_WADI.pdf (in order)
		:FRrelation: How each FR is related to other FRs in accordance to the axiomatic matrix of the FRs

		Note:
		dirty data is 1 when there is an attack, 0 when there is not
		fr is 1 when there is no attack, 0 when there is
		"""
		testCounter = 0
		output = []

		if not testPass:
			print("TotalTest did not pass")
			return

		if len(fr_result_dir.keys()) == 0:
			print("There is no DIR provided for the FRs")
			return

		for i in fr_result_dir.keys():
			suboutput = {"Name":None, "True positive":0, "False positive":0, "True negative":0, "False negative":0, "Not counted":0, "Total points":0}
			dirtyDataList = None
			FRList = None

			with open(dirty_data_dir) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				for row in spamreader:
					dirtyDataList = copy.deepcopy(row)

			with open(fr_result_dir[i]) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				for row in spamreader:
					FRList = copy.deepcopy(row)

			suboutput["Name"] = i

			testOrderCounter = -1
			preVal = "0.0"
			for j in range(len(dirtyDataList)):
				if dirtyDataList[j] == "1.0":
					# positive
					if preVal == "0.0":
						testOrderCounter += 1


					if testOrder[testOrderCounter] in FRrelation[i]:
						if FRList[j] == "0.0":
							# True
							suboutput["True positive"] += 1
							# print("True positive - dirty: {0}; fr: {1}".format(dirtyDataList[i], FRList[i]))
						else:
							# False
							suboutput["False positive"] += 1
							# print("False positive - dirty: {0}; fr: {1}".format(dirtyDataList[i], FRList[i]))
					else:
						suboutput["Not counted"] += 1

				else:
					# negative
					if testOrder[testOrderCounter] in FRrelation[i]:
						if FRList[j] == "1.0":
							# True
							suboutput["True negative"] += 1
							# print("True negative - dirty: {0}; fr: {1}".format(dirtyDataList[i], FRList[i]))
						else:
							# False
							suboutput["False negative"] += 1
							# print("False negative - dirty: {0}; fr: {1}".format(dirtyDataList[i], FRList[i]))
					else:
						suboutput["Not counted"] += 1

				preVal = copy.deepcopy(dirtyDataList[j])
				suboutput["Total points"] += 1

			output.append(suboutput)
		print("Total stats done")
		print(output)


	def TotalGraphRead(self, dirty_data_dir, fr_result_dir, testPass):
		"""
		Expresses DIRGRAPHRESULT, as well as results of all FRs as a graph

		:param dirty_data_dir: String of dir of DIRGRAPHRESULT
		:param fr_result_dir: a dictionary that contains {name of FR:string value of dir of result}. All csv files are expected to have same number of datapoints
		:param testPass: Output of GraphTest, Boolean True if test passes, Boolean False otherwise
		"""
		counter0 = 0
		counter1 = 0
		fileLength = 0  # represent int number of datapoints in csv files
		compress_length = 1000  # represent the number of datapoints we're compressing the entire dataset to
		dataPointRecord = {}  # big boi. Dictionary with key:source of list, value:lists(each representing an FR/dirty data) of 1000 elements, 1 for true, 0 for false
		nameDirtyData = "Dirty Dataset"  # label for dirty dataset for graph
		time_list = []

		
		if not testPass:
			print("TotalTest did not pass")
			return

		fr_result_dir[nameDirtyData] = dirty_data_dir  # append dirty data dir into dictionary so we can onvert everything at one go

		# fill up dataPointRecord with key:value pairs where key=name of DR/dirty data; value=list of float elements
		for i in fr_result_dir.keys():
			with open(fr_result_dir[i]) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

				# convert list element into float objects
				subList = []
				for j in spamreader.__next__():
					subList.append(float(j))
				dataPointRecord[i] = copy.deepcopy(subList)
				subList.clear()

		# plot points
		for i in fr_result_dir.keys():
			plt.plot(dataPointRecord[i], label=i)

		plt.legend()
		plt.show()




DIRPROCESSEDWADI = "./data/processed_clean/processedWadi.csv"
DIRDIRTYPROCESSEDWADI = "./data/processed_dirty/WADI_attackdata_October.csv"

"""
Slicing out attack data on attack identifier 12-15 inclusive
"""
DIRGRAPHSLICED = "./data/misc/phase2GraphSliced.csv"
DIRGRAPHRESULT = "./data/misc/phase2GraphResult.csv"  # for dirty data
DIRGRAPHRESULTUNSQUASHED = "./data/misc/phase2GraphResultUnsquashed.csv"

DIRFR1SPLIT = "./data/misc/phase2FR1SplitData.csv"
DIRFR1STATESWADI = "./data/misc/phase2FR1States.csv"
DIRFR1RESULT = "./data/misc/phase2FR1Result.csv"
DIRFR1RESULTUNSQUASHED = "./data/misc/phase2FR1ResultUNSQUASHED.csv"

DIRFR8SPLIT = "./data/misc/phase2FR8SplitData.csv"
DIRFR8STATESWADI = "./data/misc/phase2FR8States.csv"
DIRFR8RESULT = "./data/misc/phase2FR8Result.csv"
DIRFR8RESULTUNSQUASHED = "./data/misc/phase2FR8ResultUNSQUASHED.csv"

# for storing test details
DIRFR1DETAILWRONG = "./data/misc/phase2FR1DetailWrong.csv"
DIRFR8DETAILWRONG = "./data/misc/phase2FR8DetailWrong.csv"


ATTACKTIMING = [["11/10/17 11:59:01", "11/10/17 12:05:00"],
				["11/10/17 12:07:30", "11/10/17 12:10:52"],
				["11/10/17 12:16:00", "11/10/17 12:25:36"],
				["11/10/17 15:26:30", "11/10/17 15:36:59"],]  # first attack is shifted to one second later, and last attack is shifted to one second earlier

ATTACKORDER = ["FR8", "FR7", "None", "FR2"]
FRRELATION = {"FR1":["FR1", "FR2", "FR8"], "FR2":["FR1", "FR2"], "FR3":["FR3"], "FR6":["FR6", "FR7", "FR8"], "FR7":["FR7", "FR8"], "FR8":["FR1", "FR6", "FR8"]}

# # for dirty graph
# Task5().extractDatapoints(DIRDIRTYPROCESSEDWADI, DIRGRAPHSLICED, "11/10/17 11:59:00", "11/10/19 15:37:00")

proportionForTraining = 1
proportionForTesting = 1

# # for testing FR1
# stats = Task5().calStats(DIRPROCESSEDWADI, ["1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], proportion=proportionForTraining)
# Task5().FR1stateCreation(DIRFR1SPLIT, DIRFR1STATESWADI, stats, 2)
# Task5().FR1ExpressionVerify(DIRFR1STATESWADI, DIRFR1RESULT)
# Task5().returnList(DIRFR1RESULT, DIRFR1RESULTUNSQUASHED)

# # for testing FR8
# stats = Task5().calStats(DIRPROCESSEDWADI, ["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], proportion=proportionForTraining)
# Task5().FR8stateCreation(DIRFR8SPLIT, DIRFR8STATESWADI, stats, 2)
# Task5().FR8ExpressionVerify(DIRFR8STATESWADI, DIRFR8RESULT)
# Task5().returnList(DIRFR8RESULT, DIRFR8RESULTUNSQUASHED)

# # for processing dirty data
# Task5().GraphCreateResult(DIRGRAPHSLICED, DIRGRAPHRESULT)  # create true/false results for dirty data
# Task5().returnList(DIRGRAPHRESULT, DIRGRAPHRESULTUNSQUASHED)

# # To show graph
# fr_result_dir = {"FR8":DIRFR8RESULTUNSQUASHED}
# testResult = Task5().TotalTest(DIRGRAPHRESULTUNSQUASHED, fr_result_dir)
# Task5().TotalGraphRead(DIRGRAPHRESULTUNSQUASHED, fr_result_dir, testResult)

# Task5().TotalStats(DIRGRAPHRESULTUNSQUASHED, fr_result_dir, testResult, ATTACKORDER, FRRELATION)  # To show stats
