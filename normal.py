import re
file_path = "./equinix-chicago.dirA.20140320-130000.UTC.anon.pcap.flow.txt"
#file_path = "./test.txt"

mainDict = {}

def main():
    with open(file_path) as file:
        line = file.readline()
        while line:
            localList = re.split(r'[\t\n]', line)
            if (localList[0] < localList[1]):
                line=",".join([localList[0], localList[1]])
            else :
                line = ",".join([localList[1], localList[0]])
            
            if (line in mainDict):
                mainDict[line] += 1;
            else :
                mainDict[line] = 1;
            line = file.readline()    

if __name__ == "__main__":
    main()

    list = sorted(mainDict.items(), key = lambda d: d[1], reverse = True)

    for i in range(10):
        print (list[i])
