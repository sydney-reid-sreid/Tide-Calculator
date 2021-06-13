import datetime

FULLCYCLE = 44762156    #length of a full tide cycle (high -> low -> high) in milliseconds
HALFCYCLE = 22381078    #length of a half tide cycle (high -> low) in milliseconds
FIRSTMOON = 1857600000  #first full moon after Jan 1 1970 in milliseconds
MOONCYCLE = 2551442900  #length of a full cycle of the moon in milliseconds
DAYLENGTH = 86400000    #length of a full day in milliseconds


#collects the user input needed to calculate the tides based on the method they choose
def main():
    calBy = getCalBy()
    if(calBy == "location"):
        location = getLocation
    else:
        currentTime = getHighLowTime
    
#determines which method (location or know high/low tide time) the user would like to use to calculate the tide
def calBy():
    flag = True
    while(flag == True):    #loops until valid input is given
        calBy = input("Would you like to calculate the tide by location or by a known high/low tide?(type \"location\", \"high\", \"low\" or \"q\" to quit): ")
        calBy = calBy.lower()
        #looks for an instance of any valid input but does not allow multiple instances of different valid inputs or q
        if(((calBy.contains("high") or calBy.contains("low")) ^ calBy.contains("location")) and not calBy.contains("q")):
            if(calBy.contains("location") == True):
                return "location"
            elif(calBy.contains("high") == True):
                return "high"
            else:
                return "low"
        elif(calBy.contains("q")):  #checking if the user wants to quit the program
            quit()
        else:  
            print("Your input was unreadable, please try again.")


#determines if the location being entered is a known location, if not ends the program
def getLocation():
    location = input("Please enter the country of the location in the form: United States  or  Australia: ")
    location = location.upper()
    placeholder = False
    if(placeholder):
        #some sort of file i/o to check if it is in the file
    else:
        quit()
    

#gets user input for the time the user knows is a high / low tide
def getHighLowTime():
    flag = True
    while(flag == True):
        time = input("Please enter the date of the known tide time (use format DD/MM/YYYY ), or enter \"q\" to quit: ")
        time = time.strip(" ")
        if((len(time) == 10) and (time[2] == "/") and (time[5] == "/")):    #checking for proper format
            flag = False
            print("we will deal with this in a minute")
        elif(time.lower() == "q"):
            quit()
        else:
            print("The format was unreadable, please follow the instructions carefully and try again, or enter \"q\" to quit")

            
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
