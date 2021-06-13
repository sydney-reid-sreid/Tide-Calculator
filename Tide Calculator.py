import datetime

FULLCYCLE = 44762156    #length of a full tide cycle (high -> low -> high) in milliseconds
HALFCYCLE = 22381078    #length of a half tide cycle (high -> low) in milliseconds
FIRSTMOON = 1857600000  #first full moon after Jan 1 1970 in milliseconds
MOONCYCLE = 2551442900  #length of a full cycle of the moon in milliseconds
DAYLENGTH = 86400000    #length of a full day in milliseconds

#collects the user input needed to calculate the tides based on the method they choose
def main():
    tidePosition = getCalBy()
    if(tidePosition == "location"):
        location = getLocation()
        tidePosition = str(location[2].lower())
        currentTime = location[0]
        locationName = location[1]
    else:
        currentTime = getHighLowTime("known")
    if(tidePosition == "high"):
        tidePosition = 1
    else:
        tidePosition = 0
    requestInfo = getHighLowTime("requested")
    requestCombo = requestInfo[0]
    requestDate = requestInfo[1]
    requestTime = requestInfo[2]
    #working with the time
    timeList = requestTime.split(":")
    hour = int(timeList[0]) * 60*60*1000
    minute = int(timeList[1]) *60*1000
    #working with the date
    dateList = requestDate.split("/")
    day = int(dateList[0])
    month = int(dateList[1])
    year = int(dateList[2])
    currentDateTime = datetime.datetime(year, month, day) #from https://www.kite.com/python/answers/how-to-get-the-number-of-seconds-since-the-epoch-from-a-datetime-object-in-python
    currentTimeSince = (currentDateTime.timestamp() - 18000) * 1000
    tideList = dailyTide(tidePosition, currentTime, requestDate)
    #add for each loop for printing tide list
    springTide = springTide(requestDate)
    nextTide = nextTide(requestTime, tideList)
    print(calBy)

    
#determines which method (location or know high/low tide time) the user would like to use to calculate the tide
def getCalBy():
    flag = True
    while(flag == True):    #loops until valid input is given
        calBy = input("Would you like to calculate the tide by location or by a known high/low tide?(type \"location\", \"high\", \"low\" or \"q\" to quit): ")
        calBy = calBy.lower()
        #looks for an instance of any valid input but does not allow multiple instances of different valid inputs or q
        if((("high" in calBy) ^ ("low" in calBy) ^ ("location" in calBy)) and not ("q" in calBy)):
            if(("location" in calBy) == True):
                return "location"
            elif(("high" in calBy) == True):
                return "high"
            else:
                return "low"
        elif(("q" in calBy)):  #checking if the user wants to quit the program
            quit()
        else:  
            print("Your input was unreadable, please try again.")


#determines if the location being entered is a known location, if not ends the program
def getLocation():
    flag = True
    while(flag == True):
        location = input("Please enter the full location, do not use abbreviations. Use the format \"United States of America, Hawaii, Banzai Pipeline\", or \"q\" to quit :  ")
        if(location == "q"):
            quit()
        location = location.upper()
        location = location.strip(" ")
        location = location.split(",")
        with open ("TideData.txt", "r") as f:
            #from an old assignment
            for line in f:
                line = line.strip(" ")
                line = line.split(",")
                if((line[0] == location[0]) and (line[1] == location [1]) and (line[2] == location[2])):
                    locationData[0] = timeHelper(line[3], line[4])
                    locationData[1] = ("" + line[2] + ", " + line[1] + ", " + line[0])
                    locationData[2] = location[5]
                    return locationData
            print("It appears that it is not in our file, you can try checking your formatting or spelling and try again or quit.")
    

#gets user input for the time the user knows is a high / low tide and also used for getting requested times
def getHighLowTime(known):
    flag = True
    while(flag == True):
        date = input("Please enter the date of the " + known +" tide time (use format DD/MM/YYYY ), or enter \"q\" to quit: ")
        date = date.strip(" ")
        if((len(date) == 10) and (date[2] == "/") and (date[5] == "/")):    #checking for proper format
            flag = False
        elif(date.lower() == "q"):
            quit()
        else:
            print("The format was unreadable, please follow the instructions carefully and try again")
    flag = True
    while(flag == True):
        time = input("Please enter the time of the " + known + " tide time in UTC (use format 24 hour time, eg. 16:08 or 05:23), or \"q\" to quit: ")
        time = time.strip(" ")
        if((len(time) == 5) and (time[2]) == ":"):
            flag = False
            currentTimeSince = timeHelper(date, time)
        elif(time == "q"):
            quit()
        else:
            print("Input was unreadable, please follow the instructions carfully and try again.")
    if(known == "requested"):
        returnVals[0] = int(currentTimeSince)
        returnVals[1] = date
        returnVals[2] = time
        return returnVals
    return int(currentTimeSince)

#helps calculate the time since epoch for the given date and time
def timeHelper(date, time):
    #working with the date
    dateList = date.split("/")
    day = int(dateList[0])
    month = int(dateList[1])
    year = int(dateList[2])

    #working with the time
    timeList = time.split(":")
    hour = int(timeList[0])
    minute = int(timeList[1])

    currentDateTime = datetime.datetime(year, month, day, hour, minute) #from https://www.kite.com/python/answers/how-to-get-the-number-of-seconds-since-the-epoch-from-a-datetime-object-in-python
    currentTimeSince = (currentDateTime.timestamp() - 18000) * 1000 #-18000 for correction, 1000 for conversion to milliseconds
    return int(currentTimeSince)

################################################################################################################################################################# 

#returns a list of the high and low tides for a specified day
def dailyTide(tideVal, inputTime, reqDate):
    if(reqDate >= inputTime): #checks that the requested date is after the input time being used as a reference point
        tideTime = (reqDate - inputTime) % HALFCYCLE
        #determines the time (in ms after midnight) of the first high/low tide of the day

        tideType = int((reqDate - inputTime) / HALFCYCLE)
        tideType = bool((tideType + tideVal + 1) % 2)
        #determines if the first tide of the day is high or low

        tides = []
        tides[0][0] = tideTime
        tides[0][1] = tideType
        #defines tides[][] and writes the time and type of the first tide of the day

        tideNum = 0
        #counting variable for the upcoming loop

        while((tideTime + HALFCYCLE) < DAYLENGTH): #loop exits once the next high/low tide occurs on the following day
            tideTime += HALFCYCLE
            tideType = not tideType
            tideNum += 1
            #increments tide time and type variables and counting variable

            tides[tideNum][0] = tideTime
            tides[tideNum][1] = tideType
            #inputs incremeneted values into list

        return(tides)

    else: #error catching, will probably be removed in favour of historical tide calculations in future
        print("This time is too old, please choose a different time")
    
        return()
    
    
#determines the presence of a spring or neap tide
def springTide(reqDate):
    moonTime = (reqDate - FIRSTMOON) % MOONCYCLE
    #determines the amount of time that has elapsed since the last full moon

    moonTimeA = moonTime - 0.5 * DAYLENGTH
    moonTimeB = moonTime + 1.5 * DAYLENGTH
    #sets the upper and lower bounds for the presence of a spring/neap tide

    fullMoon = 0
    thirdQuart = MOONCYCLE * 1/4
    newMoon = MOONCYCLE * 1/2
    firstQuart = MOONCYCLE * 3/4
    #sets the times after the full moon for each relevant moon phase

    if(moonTimeA < fullMoon and moonTimeB > fullMoon): #is there a full moon?
        print("there is a spring tide in effect")
    elif(moonTimeA < thirdQuart and moonTimeB > thirdQuart): #is there a third quarter moon?
        print("there is a neap tide in effect")
    elif(moonTimeA < newMoon and moonTimeB > newMoon): #is there a new moon?
        print("there is a spring tide in effect")
    elif(moonTimeA < firstQuart and moonTimeB > firstQuart): #is there a first quarter moon?
        print("there is a neap tide in effect")
    
    return()


#determines when the next high/low tide will be
def nextTide(reqTime, tides):
    tidesLength = len(tides)
    tideCounter = 0
    #counting variables to be used in the upcoming loop

    while(tideCounter < tidesLength): #loops to find the next tide from the list tides[][]
        if (reqTime < tides[tideCounter][0]): #true if the tide in the list will occur after the requested time
            nextTideTime = tides[tideCounter][0] - reqTime
            nextTideType = bool(tides[tideCounter][1])
            #sets the values of the next tide's time and type

            break #exits the loop to prevent this if from being called again
        else: 
            tideCounter += 1
            #increments the counter

    if(tideCounter == tidesLength): #if the loop was exited without finding the next tide
        nextTideTime = tides[tideCounter - 1][0] - reqTime + HALFCYCLE
        nextTideType = bool(not tides[tideCounter][1])
        #sets the values of the next tide's time and type

    nextTideHours = int(nextTideTime / 3600000)
    nextTideMinutes = int((nextTideTime % 3600000) / 60000)
    #converts nextTideTime to hours and minutes

    if (nextTideType): #if the next tide is a high tide
        print("the next high tide is in", nextTideHours, "hours and", nextTideMinutes)
    else: #the next tide is a low tide
        print("the next low tide is in", nextTideHours, "hours and", nextTideMinutes)
    
    return()
