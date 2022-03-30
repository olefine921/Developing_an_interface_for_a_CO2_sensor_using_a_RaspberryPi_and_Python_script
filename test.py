csvRow = ['Wed Mar 23 14:37:57 2022', 15873.0, 16827.333333333332, 16284.333333333334, 16358.0]
y = len(csvRow)
print(y)

csvRow.pop(0) #delete 1. element -> Timestamp
csvRow.pop(0) #delete 2. element -> avPCO2
csvRow.pop(0)
csvRow.pop(0)
csvRow.pop(0)

print(csvRow)
