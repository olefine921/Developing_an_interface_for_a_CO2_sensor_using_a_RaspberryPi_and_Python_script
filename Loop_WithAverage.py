from time import time, ctime, sleep

#Functions
"""
def summeOfData():
    # Write Data into Variable to prepare for calculating average

    pCO2 = res.register[0]
    temp = res.register[3]
    mbar = res.register[5]
    DLI = res.register[7]

    summePCO2 += pCO2
    summeTemp += temp
    summembar += mbar
    summeDLI += DLI"""

#Counter
counter1 = 0
counter2 = 1

#Variables
t = 0

pCO2 = 0
temp = 0
mbar = 0
DLI = 0

summePCO2 = 0
summeTemp = 0
summembar = 0
summeDLI = 0

avPCO2 = 0
avTemp = 0
avmbar = 0
avDLI = 0

#Test Data

res = [15960, 50065, 16835, 28836, 16387, 21648, 17332, 0]

#Give date + time for csv-file

t = time()
dateForCSV = ctime(t)

print(dateForCSV)
print('Start of loop')

while counter1 < 8:
 

    pCO2 = res[0]   #res.register[0]
    temp = res[3]   #res.register[3]
    mbar = res[5]    #res.register[5]
    DLI =  res[7]    #res.register[7]


    print('')
    print('pCO2 = ', pCO2)
    print(mbar)

    summePCO2 += pCO2
    summeTemp += temp
    summembar += mbar
    summeDLI += DLI

    t = time()
    dateForCSV = ctime(t)

    print(dateForCSV)


    print('summePCO2 = ', summePCO2)
    print(summembar)

    counter1 += 1

    print(counter1)

    if counter1 == 6:
        #Calculate Average for 1 Min

        avPCO2 = summePCO2 / 6
        avTemp = summeTemp / 6
        avmbar = summembar / 6
        avDLI = summeDLI / 6
        print('')
        print('avPCO2 = ', avPCO2)
        print(avmbar)

        counter1 = 0
        print(counter1)        
        print('End of Loop')

    else:

        sleep(10)  # Stops Loop for 10sec
