import os
# from itertools import chain
import itertools
import datetime

def bedMapper(filename, outputLoc):
    bedMapper=[]
    with open(outputLoc + "/" + filename + ".bed", "r") as bed_test: ##Change to input variables
        for i in bed_test:
            sub=[]
            final=''
            for u in i:
                if((u != '\t') and (u != "\n")):
                    final = final + str(u)
                else:
                    sub.append(final)
                    final=''
                    sub.append(u)
            bedMapper.append(sub)
    return(bedMapper)

def intervalLister(bedMapper):
    masterList=[]
    for i in range(len(bedMapper)):
        temp=[]
        temp.append(int(bedMapper[i][4]))
        temp.append(int(bedMapper[i][2]))
        temp.sort()
        masterList.append(temp)
    return(masterList)

def intervalExpander(bedMapper, interval):
    masterList=intervalLister(bedMapper)
    for i in range(len(bedMapper)):
        if((bedMapper[i][2]) and (bedMapper[i][4])):
            try:
                if((type(int(bedMapper[i][2])) == int) and (type(int(bedMapper[i][4])) == int)):
                    bedMapper[i][2] = str(int(bedMapper[i][2]) - interval)
                    bedMapper[i][4] = str(int(bedMapper[i][4]) + interval)
            except:
                print("\nPython interval expanson error on line: " + i + ". Adding error notation to error logs")
                #Add stuff for logging error to text file
    expandedList=intervalLister(bedMapper)
    return(bedMapper, masterList, expandedList)

def fileSaver(bedMapper, outputLoc, filename):
    output=''.join(chain.from_iterable(bedMapper))
    with open(outputLoc + "/" + filename + "_new_interval.bed", "w") as newBed: ##Change to input variables
        newBed.write(output)

def typeOneTwo(expandedList, inputList, interval, outputLoc):
    if(id(inputList) != id(expandedList)):
        typeOT = "ONE"
    else:
        typeOT = "TWO"
    now = datetime.datetime.now()
    gate=True
    results = '\nType One and Two Check for: ' + now.strftime("%Y-%m-%d, %H:%M") + '\n---------------\n' ##ADD PROJECT NAME TO THIS
    results += 'Type One: overlap into SNP\nType Two: Window coverage overlaps.\n'
    for i in range(len(expandedList)):
        a=expandedList[i][0]
        b=expandedList[i][1]
        for j in range(len(inputList)):
            if(i != j): ##Add id() check
                subTA=inputList[j][0]
                subTB=inputList[j][1]
                binary=[0,0,0,0]
                if(a <= subTA):
                    binary[0]=1 
                if(a <= subTB):
                    binary[1]=1
                if(b >= subTA):
                    binary[2]=1
                if(b >= subTB):
                    binary[3]=1
                if((binary != [1,1,0,0]) and (binary != [0,0,1,1])):
                    gate = False
                    results+=binaryIntersect(binary, typeOT, a, b, subTA, subTB)
    if(gate):
        results+="\nNo window overlaps detected.\n"
    results += "\n\n**********************\n"
    with open(outputLoc + "/WindowOverlap.txt", 'a+') as window: ##CHANGE TO OUTPUT DIR
        window.write(results)

def binaryIntersect(BinaryNum, typeOT, a, b, subTA, subTB):
    resultsBI=''
    if(BinaryNum == [0,1,1,0]):
        print("WARNING TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is encapsulated within " + str(subTA) + "-" + str(subTB) + " window. \nNotated in overlap log in output DIR.")
        resultsBI+="\n--TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is encapsulated within " + str(subTA) + "-" + str(subTB) + " window"
    elif(BinaryNum == [1,1,1,1]):
        print("WARNING TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is equal or encapsulating " + str(subTA) + "-" + str(subTB) + " window. \nNotated in overlap log in output DIR.")
        resultsBI+="\n--TYPE " + typeOT + " on positions: " + str(a) + "-" + str(b) + " SNP window is equal or encapsulating " + str(subTA) + "-" + str(subTB) + " window"
    elif((BinaryNum == [1,1,1,0]) or (BinaryNum == [0,1,1,1])):
        if(BinaryNum == [1,1,1,0]):
            print("WARNING TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is overlapping " + str(subTA) + "-" + str(subTB) + " window." + " Overlaps occurring on the right of SNP, between " + str(b) + " and " + str(subTA) + ". \nNotated in overlap log in output DIR.")
            resultsBI+="\n--TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is overlapping " + str(subTA) + "-" + str(subTB) + " window." + "Overlaps occurring on the right of SNP, between " + str(b) + " and " + str(subTA)
        elif(BinaryNum == [0,1,1,1]):
            print("WARNING TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is overlapping " + str(subTA) + "-" + str(subTB) + " window." + " Overlaps occurring on the left of SNP, between " + str(a) + " and " + str(subTB) + ". \nNotated in overlap log in output DIR.")
            resultsBI+="\n--TYPE " + typeOT + " overlap on positions: " + str(a) + "-" + str(b) + " SNP window is overlapping " + str(subTA) + "-" + str(subTB) + " window." + "Overlaps occurring on the left of SNP, between " + str(a) + " and " + str(subTB)
    return(resultsBI)    
        
def bashInputs():
    outputLoc=str(os.environ['outputLoc'])
    filename=str(os.environ['filename'])
    windowLength=str(os.environ['windowLength'])
    inputFile=str(os.environ['inputFile'])
    return(outputLoc, filename, windowLength, inputFile)

def main():
    outputLoc, filename, interval, inputFile=bashInputs()
    bedMap=bedMapper(filename, outputLoc)
    bedMap, masterList, expandedList=intervalExpander(bedMap, interval)
    fileSaver(bedMapper, outputLoc, filename)
    typeOneTwo(expandedList, masterList, interval, outputLoc)

main()