"""
To do: 
- PROBLEM (9/4/19) - GraphCreateResult squashes until almost all datapoint == 1 is gone
--- consider double checking if any rounding down occured
--- consider increasing total number of datapoints to be 10000 instead
- Display dirty data on graph, noting times where attacks happen. Overlay results of 
logical expression for each FRs where it turns up true/false


Note:
850 of the dirty data points are attacked (For FR8). That only makes up 0.491% of total 
data points in dirty dataset. Measuring proportion of violating data points 
shouldn't be our metric, the number of consecutive violating datapoints should be instead.


---- FOR DIRTY DATA ----
When data is squashed into 1000 datapoints,
for original data ratio of "1" datapoints is 0.008813953488372092
for squashed data ratio of "1" datapoints is 0.008773046608256849
I ran the code
```
Task5().returnList(DIRGRAPHRESULT, DIRGRAPHRESULTSQUASHED)
Task5().ResultReader(DIRGRAPHRESULT)
```

------------------------


---- FOR FR1 ----
Segmented clean data (trained clean data):
Number of datapoints that follow expression: 450816, Ratio: 0.9317441060182994

Dirty data (trained on clean data):
Number of datapoints that follow expression: 156497, Ratio: 0.9056434532007731

Dirty data (segmented from attack indicator 5):
Number of datapoints that follow expression: 0, Ratio: 0.0


When data is squashed into 1000 datapoints,
for original data ratio of "1" datapoints is 0.9056434532007731
for squashed data ratio of "1" datapoints is 0.9052093023255818
I ran the code
```
Task5().returnList(DIRFR1RESULT, DIRFR1RESULTSQUASHED)
Task5().ResultReader(DIRFR1RESULT)
```
-----------------


---- FOR FR8 ----
Segmented clean data (trained on clean data):
Number of datapoints that follow expression: 437068, Ratio: 0.9033298128930786

Dirty data (trained on clean data):
Number of datapoints that follow expression: 152950, Ratio: 0.8851170704042778

Dirty data (segemented from attack indicator 5):
Number of datapoints that follow expression: 0, Ratio: 0.0


When data is squashed into 1000 datapoints,
for original data ratio of "1" datapoints is 0.8851170704042778
for squashed data ratio of "1" datapoints is 0.8845872093023256
I ran the code
```
Task5().returnList(DIRFR8RESULT, DIRFR8RESULTSQUASHED)
Task5().ResultReader(DIRFR8RESULT)
```

-----------------





Variable: 2_LT_002_PV; 
	Mean: 75.16463184634425; 
	Standard Deviation: 4.004997969737664; 
	Max: 83.152; 
	Min: 33.0904;
Variable: 2_FIT_002; 
	Mean: 0.28483256369156784; 
	Standard Deviation: 0.27073219527238845; 
	Max: 1.16829; 
	Min: 0.0;
Variable: 2_FIT_003; 
	Mean: 0.21117356601932516; 
	Standard Deviation: 0.5271777665017551; 
	Max: 5.14847; 
	Min: 0.0;
Variable: 2_MCV_101; 
	Mean: 10.938248349341544; 
	Standard Deviation: 15.271707695853015; 
	Max: 100.0; 
	Min: 0.0;
Variable: 2_MCV_201; 
	Mean: 12.121086169732; 
	Standard Deviation: 17.037270430123243; 
	Max: 100.0; 
	Min: 0.0;
Variable: 2_MCV_301; 
	Mean: 17.074269185758087; 
	Standard Deviation: 21.038919976481115; 
	Max: 100.0; 
	Min: 0.0;
Variable: 2_MCV_401; 
	Mean: 10.46136254010838; 
	Standard Deviation: 15.776893830293163; 
	Max: 100.0; 
	Min: 0.0;
Variable: 2_MCV_501; 
	Mean: 13.37584535434821; 
	Standard Deviation: 17.00850125136361; 
	Max: 100.0; 
	Min: 0.0;
Variable: 2_MCV_601; 
	Mean: 17.443244341194962; 
	Standard Deviation: 22.88759628318109; 
	Max: 100.0; 
	Min: 0.0;

"""

import csv
import numpy as np
import copy
import matplotlib
matplotlib.use("Qt5Agg")  # specify backend for matplotlib
import matplotlib.pyplot as plt


DIRPROCESSEDWADI = "./data/processed_clean/processedWadi.csv"
DIRDIRTYPROCESSEDWADI = "./data/processed_dirty/WADI_attackdata_October.csv"

DIRFR1DATATIMESPLIT = "./data/misc/FR1dataTimeSplit.csv"
DIRFR1SPLIT = "./data/misc/FR1SplitData.csv"
DIRFR1STATESWADI = "./data/misc/FR1States.csv"
DIRFR1RESULT = "./data/misc/FR1Result.csv"
DIRFR1RESULTSQUASHED = "./data/misc/FR1ResultSquashed.csv"

DIRFR8DATATIMESPLIT = "./data/misc/FR8dataTimeSplit.csv"
DIRFR8SPLIT = "./data/misc/FR8SplitData.csv"
DIRFR8STATESWADI = "./data/misc/FR8States.csv"
DIRFR8RESULT = "./data/misc/FR8Result.csv"
DIRFR8RESULTSQUASHED = "./data/misc/FR8ResultSQUASHED.csv"

DIRGRAPHRESULT = "./data/misc/GraphResult.csv"  # for dirty data
DIRGRAPHRESULTSQUASHED = "./data/misc/GraphResultSquashed.csv"

ATTACKTIMING = [["9/10/17 19:25:00", "9/10/17 19:50:16"],
				["10/10/17 10:24:10", "10/10/17 10:34:00"],
				["10/10/17 10:55:00", "10/10/17 11:24:00"],
				["10/10/17 11:30:40", "10/10/17 11:44:50"],
				["10/10/17 13:39:30", "10/10/17 13:50:40"],
				["10/10/17 14:48:17", "10/10/17 14:59:55"],
				["10/10/17 17:40:00", "10/10/17 17:49:40"],
				["10/10/17 10:55:00", "10/10/17 10:56:27"],
				["11/10/17 11:17:54", "11/10/17 11:31:20"],
				["11/10/17 11:36:31", "11/10/17 11:47:00"],
				["11/10/17 11:59:00", "11/10/17 12:05:00"],
				["11/10/17 12:07:30", "11/10/17 12:10:52"],
				["11/10/17 12:16:00", "11/10/17 12:25:36"],
				["11/10/17 15:26:30", "11/10/17 15:37:00"],]


class Task5:

	def csvCreate(self):
		"""
		UPDATED: 1/4/19

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


	def convertString(self, inp):
		"""
		UPDATED: 3/4/19

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


	def extractDatapoints(self, startTime, endTime, dir):
		"""
		UPDATED: 1/4/19
		"""
		# process time

		startTime = self.convertString(startTime)  # (date, time, am or pm)
		endTime = self.convertString(endTime)  # (date, time, am or pm)

		counter0 = 0
		counter1 = 0
		counter2 = 0  # number of rows added
		writeState = False
		indexList = {}
		variables = ["Date", "Time"]

		with open(DIRDIRTYPROCESSEDWADI) as csvfile0:
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


	def splitData(self, variables, interval, inputDIR, ouptutDIR, proportion=1.0):
		"""
		UPDATED: 1/4/19

		- var: a list that contains string representations of sensor data names that we want to retain
		- interval: integer interval between datapoints
		- ouputDIR: string DIR of output
		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # number of rows added
		totalRow = 0  # total number of rows in datapoints
		startRow = 0  # row to start writing data
		prevVal = 0
		indexList = {}
		currentRow = []

		# count total rows
		with open(inputDIR) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

			for row in spamreader:
				totalRow += 1

			startRow = totalRow - (totalRow*proportion)

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

						if counter1 != len(variables):
							print("ERROR: Retrieving column index from .csv file. \nNumber of variables provided: {0}; Number of variables found: {1}".format(len(variables), counter1))
							break

						# ensure that first row is added in the same column order as subsequent rows 
						for i in variables:
							currentRow.append(row[indexList[i]])

						spamwriter.writerow(currentRow)
						currentRow.clear()

					elif counter0 - prevVal >= interval and counter0 >= startRow:
						for i in variables:
							currentRow.append(row[indexList[i]])

						prevVal = counter0
						counter2 += 1

						# print("Reading row {0}; writing: {1}".format(counter0, currentRow))
						spamwriter.writerow(currentRow)
						currentRow.clear()

					counter0 += 1
					print("counter0: {0}, counter0-prevVal: {1}, startRow: {2}".format(counter0,counter0-prevVal, startRow))

				print("Done. Total read rows: {0}; Total written rows: {1}; Proportion: {2}".format(counter0, counter2, proportion))
				print(variables)


	def calStats(self, variables, proportion=1.0):
		"""
		UPDATED: 1/4/19

		Calculate mean and std dev for each variable

		proportion: proportion of datapoints that will be used to calculate the statistics. We'll be using the
		first portion of the data points for calculation.

		Documentation of output
		{"Sensor_Name":[sensor_mean_value, sensor_variance_valuee]}
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
		with open(DIRPROCESSEDWADI) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

			for row in spamreader:
				totalRow += 1

			endRow = int(totalRow * proportion)  # rounded down

		# calculate mean, max, and min
		print("Calculating mean, max and min...")
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
		with open(DIRPROCESSEDWADI) as csvfile0:
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
		Returns indexList for all functions.
		:param row: first row of csvfile
		:param variables: variables to retrieve index from
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


	def ResultReader(self, inp_dir):
		"""
		Reads csv file of all results, prints out number of datapoints that follow/dont follow
		"""
		counter0 = 0
		counter1 = 0  # for filling up index list
		counter2 = 0  # for counting number of datapoints that read "1"
		indexList = {}
		variables = ["Date", "Time", "Output"]


		with open(inp_dir) as csvfile0:
			spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

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
				else:
					if row[indexList["Output"]] == "1":
						counter2 += 1

				counter0 += 1

			print("ResultReader: Number of datapoints that follow logical expression: {0}, Ratio: {1}".format(counter2, counter2/counter0))


	def returnList(self, input_dir, output_dir, compress_length=1000):
			"""
			UPDATED: 3/4/19
			
			Reads csv and express it in ~1000 datapoints, each element ranging 0 to 1 depending on (number of datapoints with value "True")/(number of datapoints per bucket) 

			Takes buckets of size (file_length/compress_length) each bucket represents a float (number of "True"/bucket size)
			Graph is plot with value (between 0 to 1) in y-axis, and time in x-axis
			"""
			variables = ["Date", "Time", "Output"]
			indexList = {}
			output = []
			startDataPoint = 1  # inclusive of this point
			file_length = 0  # number of datapoints in a file
			counter0 = 0
			counter1 = 0  # count number of datapoints in the bucket
			counter2 = 0  # count number of true datapoints in a bucket
			bucketSize = None  # rounded down (excess datapoints at the back will be cut off)
			numberOfBuckets = None  # expected to be at most 1000 otherwise slightly smaller (cos bucketSize is rounded down)

			testCounter = 0

			# instantiate file_length, assuming all files have same number of datapoints
			with open(input_dir) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

				for row in spamreader:
					file_length += 1

			bucketSize = int(file_length/compress_length)
			# numberOfBuckets = file_length//bucketSize
			numberOfBuckets = compress_length  # note that ^^ the numberOfBuckets initially turned out to be more than compress_length, so expect some inaccuracies from the missing datapoints

			with open(input_dir) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)

					# if datapoint is still within bucket
					elif counter0 - startDataPoint < bucketSize:
						if row[indexList["Output"]] == "1":
							counter1 += 1

					# once datapoint exceeds bucket
					else:
						# check if we've filled total number of buckets, if so end code
						if len(output) == numberOfBuckets:
							break

						# if not
						startDataPoint = counter0  # update startDataPoint
						output.append(counter1/bucketSize)  # append float ratio into output
						counter2 += counter1/bucketSize

						# print number of 'slopes' in the graph - indication that graph value changed from '0' to '1' or vice versa
						if counter1/bucketSize > 0 and counter1/bucketSize < 1:
							testCounter += 1 
						
						# reset counter1 to 1 or 0 depending on value of current datapoint
						if row[indexList["Output"]] == "1":
							counter1 = 1
						else:
							counter1 = 0

					counter0 += 1

			# write output into output_dir as one row
			with open(output_dir, "w+") as csvfile1:
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				spamwriter.writerow(output)

			print("ReturnList (squashed list): Ratio of (number of True)/(total number of datapoints): {0}; length of output list: {1}".format(counter2/1000, len(output)))
			print("testCounter: {0}".format(testCounter))


	def FR1stateCreation(self, inp, statsDict):
		"""
		UPDATED: 1/4/19

		"""
		counter0 = 0
		counter1 = 0
		numberStdDev = 2
		indexList = {}
		variables = ["Date", "Time", "1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"]


		with open(inp) as csvfile0:
			with open(DIRFR1STATESWADI, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						row += ["water_pump_state", "water_level_state", "mcv_state"]
						spamwriter.writerow(row)
					else:
						addToWrite = [0,0,0]

						if float(row[indexList["1_P_005"]]) < statsDict["1_P_005"][0]-(numberStdDev*statsDict["1_P_005"][1]):
							addToWrite[0] = 0
						elif float(row[indexList["1_P_005"]]) < statsDict["1_P_005"][0]+(numberStdDev*statsDict["1_P_005"][1]):
							addToWrite[0] = 1
						else:
							addToWrite[0] = 2

						if float(row[indexList["2_LT_002_PV"]]) < statsDict["2_LT_002_PV"][0]-numberStdDev*statsDict["2_LT_002_PV"][1]:
							addToWrite[1] = 0
						elif float(row[indexList["2_LT_002_PV"]]) < statsDict["2_LT_002_PV"][0]+numberStdDev*statsDict["2_LT_002_PV"][1]:
							addToWrite[1] = 1
						else:
							addToWrite[1] = 2

						mcvMean = (statsDict["2_MCV_101"][0] + statsDict["2_MCV_201"][0] + statsDict["2_MCV_301"][0] + statsDict["2_MCV_401"][0] + statsDict["2_MCV_501"][0] + statsDict["2_MCV_601"][0])
						mcvStdDev = (statsDict["2_MCV_101"][1]**2 + statsDict["2_MCV_201"][1]**2 + statsDict["2_MCV_301"][1]**2 + statsDict["2_MCV_401"][1]**2 + statsDict["2_MCV_501"][1]**2 + statsDict["2_MCV_601"][1]**2)**0.5
						if (float(row[indexList["2_MCV_101"]]) + float(row[indexList["2_MCV_201"]]) + float(row[indexList["2_MCV_301"]]) + float(row[indexList["2_MCV_401"]]) + float(row[indexList["2_MCV_501"]]) + float(row[indexList["2_MCV_601"]]) < mcvMean - 2*mcvStdDev):
							addToWrite[2] = 0
						elif (float(row[indexList["2_MCV_101"]]) + float(row[indexList["2_MCV_201"]]) + float(row[indexList["2_MCV_301"]]) + float(row[indexList["2_MCV_401"]]) + float(row[indexList["2_MCV_501"]]) + float(row[indexList["2_MCV_601"]]) < mcvMean + 2*mcvStdDev):
							addToWrite[2] = 1
						else:
							addToWrite[2] = 2

						row += addToWrite
						spamwriter.writerow(row)

					counter0 += 1
				print("state creation done")


	def FR1ExpressionVerify(self):
		"""
		UPDATED: 1/4/19		


		Note about datapoints written to DIRFR8RESULT:
		1 means an attack is not happening
		0 mean an attack is happening

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of datapoints that are relevant and follow expression
		indexList = {}
		variables = ["Date", "Time", "1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "water_pump_state", "water_level_state", "mcv_state"]
		output_variables = ["Date", "Time", "Output"]

		with open(DIRFR1STATESWADI) as csvfile0:
			with open(DIRFR1RESULT, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						spamwriter.writerow(output_variables)  # for first row in output csv file

					else:
						if row[indexList["water_pump_state"]]==row[indexList["water_level_state"]] and row[indexList["water_pump_state"]]==row[indexList["mcv_state"]]:
							counter2 += 1
							spamwriter.writerow([row[indexList["Date"]], row[indexList["Time"]], "1"])
						else:
							spamwriter.writerow([row[indexList["Date"]], row[indexList["Time"]], "0"])

					counter0 += 1

				print("Done. Number of datapoints that follow expression: {0}, Ratio: {1}".format(counter2, counter2/counter0))


	def FR8stateCreation(self, inp, statsDict):
		"""
		UPDATED: 1/4/19
		"""
		waterLevelLimit = None;  # a threshold. water level above 
		counter0 = 0
		counter1 = 0
		numberStdDev = 2
		indexList = {}
		variables = ["Date", "Time", "2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"]

		with open(inp) as csvfile0:
			with open(DIRFR8STATESWADI, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						row += ["water_level_state", "consumption_state", "mcv_state"]
						spamwriter.writerow(row)

					else:
						addToWrite = [0,0,0]

						if float(row[indexList["2_LT_002_PV"]]) < statsDict["2_LT_002_PV"][0]-(2*statsDict["2_LT_002_PV"][1]):
							addToWrite[0] = 0
						elif float(row[indexList["2_LT_002_PV"]]) < statsDict["2_LT_002_PV"][0]+(2*statsDict["2_LT_002_PV"][1]):
							addToWrite[0] = 1
						else:
							addToWrite[0] = 2

						if (float(row[indexList["2_FIT_002"]]) + float(row[indexList["2_FIT_003"]])) < (statsDict["2_FIT_002"][0]+statsDict["2_FIT_003"][0])-2*(((statsDict["2_FIT_002"][1]**2)+(statsDict["2_FIT_003"][1]**2))**0.5):
							addToWrite[1] = 0
						elif (float(row[indexList["2_FIT_002"]]) + float(row[indexList["2_FIT_003"]])) < (statsDict["2_FIT_002"][0]+statsDict["2_FIT_003"][0])+2*(((statsDict["2_FIT_002"][1]**2)+(statsDict["2_FIT_003"][1]**2))**0.5):
							addToWrite[1] = 1
						else:
							addToWrite[1] = 2

						mcvMean = (statsDict["2_MCV_101"][0] + statsDict["2_MCV_201"][0] + statsDict["2_MCV_301"][0] + statsDict["2_MCV_401"][0] + statsDict["2_MCV_501"][0] + statsDict["2_MCV_601"][0])
						mcvStdDev = (statsDict["2_MCV_101"][1]**2 + statsDict["2_MCV_201"][1]**2 + statsDict["2_MCV_301"][1]**2 + statsDict["2_MCV_401"][1]**2 + statsDict["2_MCV_501"][1]**2 + statsDict["2_MCV_601"][1]**2)**0.5
						if (float(row[indexList["2_MCV_101"]]) + float(row[indexList["2_MCV_201"]]) + float(row[indexList["2_MCV_301"]]) + float(row[indexList["2_MCV_401"]]) + float(row[indexList["2_MCV_501"]]) + float(row[indexList["2_MCV_601"]]) < mcvMean - 2*mcvStdDev):
							addToWrite[2] = 0
						elif (float(row[indexList["2_MCV_101"]]) + float(row[indexList["2_MCV_201"]]) + float(row[indexList["2_MCV_301"]]) + float(row[indexList["2_MCV_401"]]) + float(row[indexList["2_MCV_501"]]) + float(row[indexList["2_MCV_601"]]) < mcvMean + 2*mcvStdDev):
							addToWrite[2] = 1
						else:
							addToWrite[2] = 2

						row += addToWrite
						spamwriter.writerow(row)

					counter0 += 1
					# print("Progress: {0}".format(counter0))
				print("State Creation done")


	def FR8ExpressionVerify(self):
		"""
		UPDATED: 1/4/19
		Will be verifying multiple logical expressions.
		
		DP8(Number of opened input valves > 0) == DP8(Number of opened input valves > 0) AND DP1(Water level of ER tank decreases) AND DP6(Total  consumption flow rate increases)

		Result:
		Clean - Number of datapoints that follow expression: 1082479, Ratio: 0.8949051010166981
		Dirty - Number of datapoints that follow expression: 0, Ratio: 0.0

		Note about datapoints written to DIRFR8RESULT:
		1 means an attack is not happening
		0 mean an attack is happening

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of datapoints that follow expression
		indexList = {}
		variables = ["Date", "Time", "2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "water_level_state", "consumption_state", "mcv_state"]
		output_variables = ["Date", "Time", "Output"]

		with open(DIRFR8STATESWADI) as csvfile0:
			with open(DIRFR8RESULT, "w+") as csvfile1:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")
				spamwriter = csv.writer(csvfile1, delimiter=" ", quotechar="|")

				for row in spamreader:
					if counter0 == 0:
						indexList = self.createIndexList(row, variables)
						spamwriter.writerow(output_variables)  # for first row of output csv file

					else:
						if row[indexList["water_level_state"]]==row[indexList["consumption_state"]] and row[indexList["water_level_state"]]==row[indexList["mcv_state"]]:
							counter2 += 1
							spamwriter.writerow([row[indexList["Date"]], row[indexList["Time"]], "1"])
						else:
							spamwriter.writerow([row[indexList["Date"]], row[indexList["Time"]], "0"])

					counter0 += 1

				print("Done. Number of datapoints that follow expression: {0}, Ratio: {1}".format(counter2, counter2/counter0))


	def GraphCreateResult(self):
		"""
		UPDATED: 1/4/19
		Returns csv file, where each datapoint indicates True under "Output" when an attack is happening, False otherwise

		1 means True means attack is happening
		0 means False means attack is not happening

		Tests done:
		- Tested that there are 32 instances where datapoint is start/end point
		- Visually test that list values are 1 or 0

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

		with open(DIRDIRTYPROCESSEDWADI) as csvfile0:
			with open(DIRGRAPHRESULT, "w+") as csvfile1:
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


	def GraphTest(self, dirty_data_dir, fr_result_dir):
		"""
		UPDATED: 3/4/19
		Checks that all csv files contain same number of datapoints, returns True if this test passes, False otherwise
		:param dirty_data_dir: String of dir of DIRGRAPHRESULT
		:param fr_result_dir: a dictionary that contains {name of FR:string value of dir of result}. All csv files are expected to have same number of datapoints
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

			# if all elements in counterList is the same, output remains True
			for i in range(len(counterList)):
				output  = output and (counterList[0] == counterList[i])

			return output

		else:
			print("There're less than 2 dirs provided in total")
			return


	def GraphRead(self, dirty_data_dir, fr_result_dir, testPass):
		"""
		UPDATED: 3/4/19

		Expresses DIRGRAPHRESULT, as well as results of all FRs as a graph normalised to 1000 points
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

		
		if not testPass:
			print("GraphTest did not pass")
			return

		fr_result_dir[nameDirtyData] = dirty_data_dir  # append dirty data dir into dictionary so we can onvert everything at one go

		# fill up dataPointRecord with key:value pairs where key=name of DR/dirty data; value=list of float elements
		for i in fr_result_dir.keys():
			with open(fr_result_dir[i]) as csvfile0:
				spamreader = csv.reader(csvfile0, delimiter=" ", quotechar="|")

				# convert list element into float objects
				for row in spamreader:
					subList = []
					for j in row:
						subList.append(float(j))
					dataPointRecord[i] = copy.deepcopy(subList)
				subList.clear()

		# plot points
		for i in dataPointRecord.keys():
			plt.plot(dataPointRecord[i], label=i)

		plt.legend()
		plt.show()





		


		















# for testing FR1
# proportionForTraining = 0.6
# proportionForTesting = 1
# Task5().extractDatapoints("10/10/17 11:30:40", "10/10/17 11:44:50", DIRFR1DATATIMESPLIT)
# stats = Task5().calStats(["1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], proportion=proportionForTraining)
# Task5().splitData(["Date", "Time", "1_P_005", "2_LT_002_PV", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], 1, DIRDIRTYPROCESSEDWADI, DIRFR1SPLIT, proportion=proportionForTesting)
# Task5().FR1stateCreation(DIRFR1SPLIT, stats)
# Task5().FR1ExpressionVerify()

# for testing FR8
# proportionForTraining = 0.6
# proportionForTesting = 1
# Task5().extractDatapoints("10/10/17 11:30:40", "10/10/17 11:44:50", DIRFR8DATATIMESPLIT)
# stats = Task5().calStats(["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], proportion=proportionForTraining)
# Task5().splitData(["Date", "Time", "2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], 1, DIRDIRTYPROCESSEDWADI, DIRFR8SPLIT, proportion=proportionForTesting)
# Task5().FR8stateCreation(DIRFR8SPLIT, stats)
# Task5().FR8ExpressionVerify() 

# To create squashed results and test them
# Task5().returnList(DIRFR8RESULT, DIRFR8RESULTSQUASHED)  # create squashed results and produce ratio
# Task5().ResultReader(DIRFR8RESULT)  # produce ratio for original data
# Task5().GraphCreateResult()  # create squashed results for dirty data
# Task5().returnList(DIRGRAPHRESULT, DIRGRAPHRESULTSQUASHED)

# To show graph
fr_result_dir = {"FR1":DIRFR1RESULTSQUASHED, "FR8":DIRFR8RESULTSQUASHED}
testResult = Task5().GraphTest(DIRGRAPHRESULTSQUASHED, fr_result_dir)
Task5().GraphRead(DIRGRAPHRESULTSQUASHED, fr_result_dir, testResult)