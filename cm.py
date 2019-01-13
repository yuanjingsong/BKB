import time
import re
import random
file_path = "./equinix-chicago.dirA.20140320-130000.UTC.anon.pcap.flow.txt"
#file_path = "./normal.txt"

def exeTime(func):
    def newFunc(*args, **args2) :
        t0  = time.time()
        back = func(*args, **args2)
        
        print ("time is %s" % (time.time() - t0))

        return back
    return newFunc

class Count_Min(object):
    ## using a matrix sketch[w][d]
    ## w: the hash function's output range
    ## d: the number of a set of hash function
    Max = 100000
    def __init__ (self, w=None, d=None) :
         
        self.values = []
        self.w = w
        self.d = d
        self.offset = []

        self.offset = [random.randint(0, w) for i in range(d)]
        self.sketch = [[0 for i in range(w)] for i in range(d)]
    #@exeTime
    def add(self, value) :

        if value not in self.values:
            self.values.append(value)

        for i in range(self.d):
            self.sketch[i][self.hash(value, i)] += 1

    def query(self, value):
        minimum = Count_Min.Max
        for i in range(self.d):
            minimum = min(minimum, self.sketch[i][self.hash(value, i)])
        return minimum

    def hash(self, value, i):
        # map value => [0, w - 1]
        return (hash(value) + self.offset[i]) % self.w

    def sortValue(self):
        dict = {}
        for value in self.values:
            dict[value] = self.query(value)

        list = sorted(dict.items(), key = lambda d : d[1], reverse = True)

        return list

def main():
    w = 50
    d = 20
    cm = Count_Min(w,d)
    with open(file_path) as file:
        line = file.readline()
        while (line):
            localList = re.split(r'[\t\n]', line)
            if (localList[0] < localList[1]):
                line = ",".join([localList[0], localList[1]])
            else:
                line = ",".join([localList[1], localList[0]])
            ##do cm 
            cm.add(line)
            line = file.readline()
    list = cm.sortValue()
    for i in range(10):
        print(list[i])
if __name__ == "__main__":
    main()
