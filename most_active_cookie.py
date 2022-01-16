import sys
import re
from datetime import datetime
from datetime import timedelta
import heapq
class LogData:
    def __init__(self, infile):
        try:
            f = open(infile)
            #read data in
            self.data = f.readlines()
            f.close()
        except:
            print("Fail to open file ", infile)
            sys.exit(-1)
        #store data, the structure is {year: {month : {day : {log : count}}}}
        self.dic = {}
        
    #process data   
    def storedata(self):
        for line in self.data:
            #check input format, if the line is not in "log,time" format, skip the line
            ls = line.strip().split(",")
            if len(ls) != 2:
                continue
            log = ls[0].strip()
            stime = ls[1].split("+")
            if len(stime) != 2:
                continue
            try:
                #change time from string to datatime type
                time = datetime.strptime(stime[0], "%Y-%m-%dT%H:%M:%S")
            except:
                continue
            #if the time system does not start at 00:00, adjust the time
            if stime[1] != "00:00":
                try:
                    tmpl = stime[1].strip().split(":")
                    delta = timedelta(hours = int(tmpl[0]), minutes = int(tmpl[1]))
                    time = time + delta
                except:
                    continue
            #if year not in dictionary, add the year
            if time.year not in self.dic.keys():
                self.dic[time.year] = {}
            #if month not in the dictionary, add the month
            if time.month not in self.dic[time.year].keys():
                self.dic[time.year][time.month] = {}
            #if day not in the dictionary
            if time.day not in self.dic[time.year][time.month].keys():
                self.dic[time.year][time.month][time.day] = {}
            #if log not in the dictionary
            if log not in self.dic[time.year][time.month][time.day].keys():
                self.dic[time.year][time.month][time.day][log] = 0
            #add the count the log at that day
            self.dic[time.year][time.month][time.day][log] = self.dic[time.year][time.month][time.day][log] + 1

    def findmax(self, target):
        #if the year not in the data, return
        if target.year not in self.dic.keys():
            return
        #if the month not in the data, return
        if target.month not in self.dic[target.year].keys():
            return
        #if the day not in the data, return
        if target.day not in self.dic[target.year][target.month].keys():
            return
        h = []
        #push all the logs of the day into a heap
        for log in self.dic[target.year][target.month][target.day].keys():
            heapq.heappush(h, (-self.dic[target.year][target.month][target.day][log], log))
        #if no log data, return
        if not h:
            return
        maxcount = h[0][0]
        #print all the logs with the most activity
        while h and h[0][0] == maxcount:
            tmp = heapq.heappop(h)
            print(tmp[1])          


def printusage():
    print("Usage: most_active_cookie log_csv_file -d date(YYYY-MM-DD)")
    sys.exit(-1)
    
def main():
    #Check arguments number
    if len(sys.argv) != 4:
        printusage()
    #Check arguments format
    if sys.argv[2] != "-d":
        printusage()
    fdate = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    if re.match(fdate, sys.argv[3]) == None:
        printusage()
    target = datetime.strptime(sys.argv[3], "%Y-%m-%d")
    #init a LogData class
    ld = LogData(sys.argv[1])
    #read the input file and store the data
    ld.storedata()
    #find the most active cookie of the day
    ld.findmax(target)

main()
            
        
