import time
from datetime import datetime, date, timedelta

start = datetime.now()
time.sleep(62)
end = datetime.now()

#t1 = timedelta(hours = start.hour, minutes = start.minute, seconds = start.sec)
#t2 = timedelta(hours = end.hour, minutes = end.minute, seconds = end.sec)

duration = end - start

print(start)
print(end)
print(duration)

"""
counterCSV = []
c = 0

epoch = time.gmtime(0)
baseline 
print(epoch)

while c <= 60:
    t = time.localtime()
    current=time.strftime("%H:%M:%S",t)

    counterCSV.append(current)
    c+=1

print(counterCSV)"""