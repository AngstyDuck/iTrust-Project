"""
README
Retrieves all values from a column, index them and saves them in
/iTrust/data/processed.

To use:
1. Fill in COLUMNNAME and run code
2. If column with that name cannot be found, error will be displayed

"""
import csv



# for i in ["2_LT_001", "2_LT_002", "2_LS_101", "2_LS_201", "2_LS_301", "2_LS_401", "2_LS_501", "2_LS_601"]:
for j in ["1_MV_001", "1_MV_002", "1_MV_003", "1_MV_004"]:
    INPUTDIR = "./data/processed/processedWadi.csv"
    COLUMNNAME = j
    NUMOFLINES = 10

    outputDir = "./data/processed/"+COLUMNNAME+"Data.csv"
    columnIndex = -1




    with open(INPUTDIR) as csvfile:
        with open(outputDir,"w+") as csvfileOut:
            spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
            spamwriter = csv.writer(csvfileOut, delimiter=" ", quotechar="|")
            counter0=0
            for row in spamreader:

                # retrieve index of column
                if counter0 == 0:
                    counter1 = 0  # to count number of columns that has the string i inside
                    for i in range(len(row)):
                        if COLUMNNAME in row[i]:
                            print("Retrieving data from column '{0}';".format(row[i]))
                            columnIndex = i
                            counter1 += 1

                            # write row and index into output file
                            spamwriter.writerow([counter0, row[i]])

                # write into file if we managed to find the correct column index
                elif counter1 > 0 and counter1 < 2:
                    print("Progress: row {0}; value {1}".format(str(counter0), row[columnIndex]))
                    spamwriter.writerow([counter0,row[columnIndex]])

                # else print eror
                else:
                    print("ERROR: Retrieving column index from .csv file")

                counter0 += 1
print("done.")








































# fin
