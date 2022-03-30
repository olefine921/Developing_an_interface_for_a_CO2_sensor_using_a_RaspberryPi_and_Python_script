def setVariablesForAverage(counter1, pCO2, temp, mbar, DLI, summePCO2, summeTemp, summembar, summeDLI, avPCO2, avTemp, avmbar, avDLI, csvRow, loopedTime, csvTimeCounter, date, x, plotAvPCO2, plotAvTemp):
    counter1 = 0
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

    # clear csvRow-List
    csvRow = []

    # clear time variables for difference
    loopedTime = 0
    csvTimeCounter = 0

    # clear arrays for plotting
    date = []
    x = []
    plotAvPCO2 = []
    plotAvTemp = []

    return counter1, pCO2, temp, mbar, DLI, summePCO2, summeTemp, summembar, summeDLI, avPCO2, avTemp, avmbar, avDLI, csvRow, loopedTime, csvTimeCounter, date, x, plotAvPCO2, plotAvTemp

def startNewTimedLoop(a, b, realTemp, counter2, adresse):
    a = 0
    b = 0
    counter2 = 0

    now = datetime.now()
    adresseDate = now.strftime("%d.%m.%Y_%H.%M")
    adresse = '/media/pi/boot/pCO2_Sensor_Data/' + adresseDate

    with open(adresse + '.csv', w) as file:
        writer = csv.writer(file)

    realTemp = float(input())
    print('')
    a = float(input())
    a = float(input())

    return a, b, realTemp, counter2, adresse

def writeInCSVFile(summePCO2, summeTemp, summembar, summeDLI, startTime, adresse, csvRow):
    avPCO2 = summePCO2 / 6
    avTemp = summeTemp / 6
    avmbar = summembar / 6
    avDLI = summeDLI / 6

    t = time()
    dateForCSV = ctime(t)

    loopedTime = datetime.now()
    csvTimeCounter = loopedTime - startTime

    csvRow.append(dateForCSV)
    csvRow.append(csvTimeCounter)
    csvRow.append(avPCO2)
    csvRow.append(avTemp)
    csvRow.append(avmbar)
    csvRow.append(avDLI)

    print(csvRow)

    with open(adresse + '.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow(csvRow)

    counter2 += 1


    return counter2

def plotFromCSV(a, b, adresse, x, plotAvPCO2, plotAvTemp, date):
    with open(adresse, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')

        for row in plots:
            x.append(row[1])
            plotAvPCO2.append(float(row[2]))
            plotAvTemp.append(float(row[3]))
            date.append(row[0])

    fig, ax1 = plt.subplots(figsize=(25, 15))

    plt.suptitle("Average pCO2 and Temp starting by " + date[0])

    print(x)
    print(plotAvPCO2)
    print(plotAvTemp)

    print(counter2)

    color = 'tab:red'
    ax1.set_xlabel('time (min)')
    ax1.set_xticks(np.arange(0, len(x) + 1, 10))
    ax1.set_ylabel('pCO2 in %', color=color)
    ax1.plot(x, plotAvPCO2, color=color)
    plt.xticks(rotation=25)

    ax2 = ax1.twinx()
    ax2.set_ylim([a,b])

    color = 'tab:blue'
    ax2.set_ylabel('avTemp in °C', color=color)
    ax2.plot(plotAvTemp, color=color)

    fig.tight_layout()

    fig.savefig(adresse + '.png')

    plt.show(block=False)

    sleep(10)  # Stops Loop for 10sec

    plt.close('all')
    fig.clear()

    return

