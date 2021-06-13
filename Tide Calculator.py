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
