import csv

def convertCSV(csvpath: str):
    histTable = []
    firstLine = True
    # open csv
    with open(csvpath) as csvfile:
        csvread = csv.reader(csvfile)
        # check each row of csv
        for row in csvread:
            # prevent first line from being read
            if firstLine:
                firstLine = False
                continue
            tableRow = []
            for x in row:
                try:
                    tempX = float(x)
                    tableRow.append(tempX)
                except ValueError:
                    tableRow.append(x)
            histTable.append(tableRow)

    return histTable

def getBalanceSeries(csvList:list, feesOn:bool=True, startDate:str="", endDate:str=""):
    balance = 0
    balanceList = []
    for row in reversed(csvList):
        # ensure each row of csv is in correct date range, or 
        # otherwise handle unspecified dates.
        if (row[0] >= startDate or not startDate) and (row[0] <= endDate or not endDate):
            if "Transfer in" in row[3]:
                balance+=row[4]
            if "Trial" in row[3]:
                balance+=row[4]

            #untested
            if "Transfer out" in row[3]:
                balance+=row[4]
        
            if "Close" in row[3]:
                if feesOn:
                    balance+=(row[4]+row[5])
                else:
                    balance+=row[4]
            if ("Open" in row[3]) and feesOn:
                balance+=row[5]
            if ("Fees" in row[3]) and feesOn:
                balance+=row[4]
            balanceList.append([row[0],balance])
    return balanceList

def getBalance(csvList:list, feesOn:bool=True, startDate:str="", endDate:str=""):
    return getBalanceSeries(csvList, feesOn, startDate, endDate)

def getFeesPaid(csvList:list, startDate:str="", endDate:str=""):
    fees = 0
    for row in csvList:
        if (row[0] >= startDate or not startDate) and (row[0] <= endDate or not endDate):
            if "Close" in row[3]:
                fees+=row[5]
            if ("Open" in row[3]):
                fees+=row[5] 
            if ("Fees" in row[3]):
                fees+=row[4]
    return fees

def getMaxBalance(csvList:list, feesOn:bool=True, startDate:str="", endDate:str=""):
    return