"""

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


DIRPROCESSEDWADI = "./data/processed_clean/processedWadi.csv"
DIRFR8DATATIMESPLIT = "./data/processed_dirty/FR8dataTimeSplit.csv"
DIRFR8SPLIT = "./data/processed_clean/FR8SplitData.csv"
DIRFR8STATESWADI = "./data/processed_clean/FR8States.csv"


class Task5:

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

						# print("Reading row {0}; writing: {1}".format(counter0, currentRow))
						spamwriter.writerow(currentRow)
						currentRow.clear()

					counter0 += 1

				print("Done. Total read rows: {0}; Total written rows: {1}".format(counter0, counter2))
				print(variables)

	def calStats(self, variables):
		"""
		Calculate mean and std dev for each variable
		"""
		counter0 = 0
		counter1 = 0
		indexList = {}
		counterDict = {}
		statsDict = {}

		for i in variables:
			statsDict[i] = [0,0,0,9999999]  # [mean, standard deviation, max, min]
			counterDict[i] = [0,0,0,0]   # [sum of all, sum of (difference with mean)^2]

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
				else:
					for i in variables:
						counterDict[i][0] += float(row[indexList[i]])

						# max and min
						if float(row[indexList[i]]) > statsDict[i][2]:
							statsDict[i][2] = float(row[indexList[i]])
						if float(row[indexList[i]]) < statsDict[i][3]:
							statsDict[i][3] = float(row[indexList[i]])

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
					for i in variables:
						counterDict[i][1] += (float(row[indexList[i]]) - statsDict[i][0])**2
				
				counter0 += 1
		for i in variables:
			statsDict[i][1] = (counterDict[i][1]/counter0)**0.5


		for i in variables:
			print("Variable:{0};Mean:{1};Standard Deviation:{2};Max:{3};Min:{4};".format(i, statsDict[i][0], statsDict[i][1], statsDict[i][2], statsDict[i][3]))

		return statsDict

	def FR8stateCreation(self, inp, statsDict):
		
		waterLevelLimit = None;  # a threshold. water level above 
		counter0 = 0
		counter1 = 0
		numberStdDev = 2
		indexList = {}
		variables = ["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"]
		outputVariables = ["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "water_level_state", "consumption_state", "mcv_state"]

		with open(inp) as csvfile0:
			with open(DIRFR8STATESWADI, "w+") as csvfile1:
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
		Will be verifying multiple logical expressions.
		
		DP8(Number of opened input valves > 0) == DP8(Number of opened input valves > 0) AND DP1(Water level of ER tank decreases) AND DP6(Total  consumption flow rate increases)

		Result:
		Clean - Number of datapoints that follow expression: 1082479, Ratio: 0.8949051010166981
		Dirty - Number of datapoints that follow expression: 0, Ratio: 0.0

		"""
		counter0 = 0
		counter1 = 0
		counter2 = 0  # counts number of datapoints that follow expression
		indexList = {}
		variables = ["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601", "water_level_state", "consumption_state", "mcv_state"]

		with open(DIRFR8STATESWADI) as csvfile0:
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
					if row[indexList["water_level_state"]]==row[indexList["consumption_state"]] and row[indexList["water_level_state"]]==row[indexList["mcv_state"]]:
						counter2 += 1

				counter0 += 1

			print("Done. Number of datapoints that follow expression: {0}, Ratio: {1}".format(counter2, counter2/counter0))

# for testing FR8
Task5().extractDatapoints("10/10/17 11:30:40", "10/10/17 11:44:50", DIRFR8DATATIMESPLIT)
stats = Task5().calStats(["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"])
Task5().splitData(["2_LT_002_PV", "2_FIT_002", "2_FIT_003", "2_MCV_101", "2_MCV_201", "2_MCV_301", "2_MCV_401", "2_MCV_501", "2_MCV_601"], 1, DIRFR8DATATIMESPLIT, DIRFR8SPLIT)
Task5().FR8stateCreation(DIRFR8SPLIT, stats)
Task5().FR8ExpressionVerify()



