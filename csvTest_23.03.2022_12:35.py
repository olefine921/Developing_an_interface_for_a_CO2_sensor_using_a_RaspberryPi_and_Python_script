import csv

avPCO2 = 0
avTemp = 24
avmbar = 0
avDLI = 17

with open('/home/pi/Documents/csv_files/testCSV.csv', 'w') as file:

    writer = csv.writer(file)

    header = ["pCo2", "Temp in C", "mbar", "DLI"]
    data = []
    data.append(avPCO2)
    data.append(avTemp)
    data.append(avmbar)
    data.append(avDLI)
    

    writer.writerow(header)

    writer.writerow(data)
