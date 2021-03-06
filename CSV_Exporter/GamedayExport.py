import json
import csv
import sys
import os
import pandas as pd
import re
import requests
from datetime import date
import time

# Create the python dictionaries (arrays) to store the information we get back from the API. These dicts are prefixed with an a_ to clarify they are arrays.
a_away_code = []
a_away_file_code = []
a_away_name_abbrev = []
a_away_score = []
a_away_team_id = []
a_away_team_name = []
a_calendar_event_id = []
a_double_header_sw = []
a_event_time = []
a_game_nbr = []
a_game_pk = []
a_game_type = []
a_gameday_sw = []
a_group = []
a_home_code = []
a_home_file_code = []
a_home_name_abbrev = []
a_home_score = []
a_home_team_id = []
a_home_team_name = []
a_id = []
a_ind = []
a_inning = []
a_media_state = []
a_series = []
a_series_num = []
a_status = []
a_tbd_flag = []
a_top_inning = []
a_venue = []
a_venue_id = []

def GetRequestedDate():
#   Check the python version. We need raw_input for 2.xx versions and input for 3.xx versions. Mac computers come with 2.xx versions by default.
    if (sys.version).startswith("2."):
        inputDate = raw_input("\n Please enter in a date. Format: YYYY-MM-DD. \n  Date: ")
    if (sys.version).startswith("3."):
        inputDate = input("\n Please enter in a date. Format: YYYY-MM-DD. \n  Date: ")
    # Verify the user input the date in our requested format. If true, return date as requested date.
    if ValidateDate(str(inputDate)):
        return str(inputDate)
    else:
    # If false, return GetRequestedDate() so the user has another chance to enter in a valid date. 
        return GetRequestedDate()

def ValidateDate(valDate):
# Function to validate the entered date. Uses regex pattern recognition to figure out if date is in YYYY-MM-DD format. 
# Returns true or false.
    matched = re.match("[1-2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", valDate)
    is_match = bool(matched)
    if is_match:
        return True
    else:
        print("\n Error: Please format date as YYYY-MM-DD.")
        return False      

def InvokeApiRequest(requestURL):
# Function responsible for the API request. Handles timeout exceptions from the requests module. 
    try:
        rdata = requests.get(requestURL)
#   Return the contents of the data variable from function for later use.
        return rdata
#   Catch timeout errors and give an option to retry
    except requests.exceptions.Timeout:
        while "Invalid response...":
            reply = (input("\n We are heving issues communicating with the API... \n Try again? [Y/N]")).capitalize().strip()
            if (reply == 'Y' or reply == 'YES'):
                InvokeApiRequest(requestURL)
            if (reply == 'N' or reply == 'NO'):
                print("\n Error: Could not reach API server.")
                time.sleep(5)
                sys.exit()
    except requests.exceptions.RequestException as e:
# Handles all other non-timeout related API errors. Allows retry but errors could be due to malformed URI. 
         while "Invalid response...":
            reply = (input("\n Error with web request. Try again? [Y/N]")).capitalize().strip()
            if (reply == 'Y' or reply == 'YES'):
                ExportGamedayData()
            if (reply == 'N' or reply == 'NO'):
                print("\n Error: Could not reach API server.")
                time.sleep(5)
                raise SystemExit(e)

def CreateCsvFile(requestedDate, gameday_DF):
# Create the CSV file in the script's directory. Will exit with succsess or failure. Last function run in program.
    csv_file = (os.path.dirname(os.path.realpath(__file__))) + "\\" + requestedDate + "_Gameday_Data.csv"
    try:
#       The lines below use the Pandas dataframe we create in the main function and uses the .to_csv method from Pandas to create the csv file. 
        gameday_DF.to_csv(csv_file, index=False)
        print("\n CSV Exported. Please check the working directory for your file.")
        return True
#       If the file is created, call sys.exit()
    except IOError:
#   Pandas will throw the IOError if the user has a file open with the name it wants to overwrite. This will ask them to close the file and retry the creation. 
        while "Invalid response...":
            reply = input("\n Error writing to file! You may have the file you're trying to write to open. \n Please close the file and try again. \n Try Again? [Y/N]").capitalize().strip()
            if (reply == 'Y' or reply == 'YES'):
                return CreateCsvFile(requestedDate, gameday_DF)
            if (reply == 'N' or reply == 'NO'):
                print("Could not write results to file. Exiting...")
                return False

def ExportGamedayData(requestedDate):
#   Main function which calls other functions from above. Called on last line of program.
#   Get user's requested date and parse to API request URI
    requestAPIUrl = "http://gd2.mlb.com/components/game/mlb/year_{}/month_{}/day_{}/grid.json".format(str(requestedDate[0:4]), str(requestedDate[5:7]), str(requestedDate[8:10]))
#   Receive and parse the API response. 
    apiResponse = (InvokeApiRequest(requestAPIUrl)).json()
#   Try block will except if there is no game data for that date specified. 
    try:
        gamedayDataJson = apiResponse["data"]["games"]["game"]
#   Exception asks user if they want to try another date. 
    except:
#        Capitalize and remove white spaces so the below if statements are less prone to input variance errors. 
        reply = (input("\n No game data for that date. \n Try another date? [Y/N]")).capitalize().strip()
        if (reply == 'Y' or reply == 'YES'):
#           If user wants to try another date, restart the function. 
            requestedDate = GetRequestedDate()
            return ExportGamedayData(requestedDate)
        elif (reply == 'N' or reply == 'NO'):
            sys.exit("Exiting program.")
        else:
            print("\n Please choose Y or N. (Yes or No)")        
#   Below, run the gamedayDataJson and extract values. Add them to the arrays created at top of script. 
    for game in gamedayDataJson:
        a_away_code.append(game["away_code"])
        a_away_file_code.append(game["away_file_code"])
        a_away_name_abbrev.append(game["away_name_abbrev"])
        a_away_score.append(game["away_score"])
        a_away_team_id.append(game["away_team_id"])
        a_away_team_name.append(game["away_team_name"])
        a_calendar_event_id.append(game["calendar_event_id"])
        a_double_header_sw.append(game["double_header_sw"])
        a_event_time.append(game["event_time"])
        a_game_nbr.append(game["game_nbr"])
        a_game_pk.append(game["game_pk"])
        a_game_type.append(game["game_type"])
        a_gameday_sw.append(game["gameday_sw"])
        a_group.append(game["group"])
        a_home_code.append(game["home_code"])
        a_home_file_code.append(game["home_file_code"])
        a_home_name_abbrev.append(game["home_name_abbrev"])
        a_home_score.append(game["home_score"])
        a_home_team_id.append(game["home_team_id"])
        a_home_team_name.append(game["home_team_name"])
        a_id.append(game["id"])
        a_ind.append(game["ind"])
        a_inning.append(game["inning"])
        a_media_state.append(game["media_state"])
        a_series.append(game["series"])
        a_series_num.append(game["series_num"])
        a_status.append(game["status"])
        a_tbd_flag.append(game["tbd_flag"])
        a_top_inning.append(game["top_inning"])
        a_venue.append(game["venue"])
        a_venue_id.append(game["venue_id"])
#   Combine all gameday information into a single dictionary. 
    gamedayDict = {
        "away_code": a_away_code,
        "away_file_code": a_away_file_code,
        "away_name_abbrev": a_away_name_abbrev,
        "away_score": a_away_score,
        "away_team_id": a_away_team_id,
        "away_team_name": a_away_team_name,
        "calendar_event_id": a_calendar_event_id,
        "double_header_sw": a_double_header_sw,
        "event_time": a_event_time,
        "game_nbr": a_game_nbr,
        "game_pk": a_game_pk,
        "game_type": a_game_type,
        "gameday_sw": a_gameday_sw,
        "group": a_group,
        "home_code": a_home_code,
        "home_file_code": a_home_file_code,
        "home_name_abbrev": a_home_name_abbrev,
        "home_score": a_home_score,
        "home_team_id": a_home_team_id,
        "home_team_name": a_home_team_name,
        "id": a_id,
        "ind": a_ind,
        "inning": a_inning,
        "media_state": a_media_state,
        "series": a_series,
        "series_num": a_series_num,
        "status": a_status,
        "tbd_flag": a_tbd_flag,
        "top_inning": a_top_inning,
        "venue": a_venue,
        "venue_id": a_venue_id
    }
#   Create a Pandas dataframe with the gamedayDict we created above, specify column headers. 
    gameday_DF = pd.DataFrame(gamedayDict, columns = [
        "away_code",
        "away_file_code",
        "away_name_abbrev",
        "away_score",
        "away_team_id",
        "away_team_name",
        "calendar_event_id",
        "double_header_sw",
        "event_time",
        "game_nbr",
        "game_pk",
        "game_type",
        "gameday_sw",
        "group",
        "home_code",
        "home_file_code",
        "home_name_abbrev",
        "home_score",
        "home_team_id",
        "home_team_name",
        "id",
        "ind",
        "inning",
        "media_state",
        "series",
        "series_num",
        "status",
        "tbd_flag",
        "top_inning",
        "venue",
        "venue_id"
    ])
#   Using a function we created above, export the Pandas gameday dataframe to csv.
#   Since CreateCsvFile is the last function called in the main execution function, return true or false to report succsessful or failed execution. 
#   Can be used to write automated tests later. 
    if CreateCsvFile(requestedDate, gameday_DF):
        return True
    else:
        return False
    
# Call the main function. This is what kicks off the 'script' 

try: 
#   Check if the script was launched with the date as an argument. Validate date. If date is valid, set it as requestedDate    
    if ValidateDate(sys.argv[1]):
        requestedDate = sys.argv[1]
    else:
#       if the date is not valid, run the GetRequestedDate function. 
        requestedDate = GetRequestedDate()
except IndexError:
#   IndexError is raised if there is no argument specified when script is launched. If there is no specified date, set requestedDate to GetRequestedDate()
    requestedDate = GetRequestedDate()

# Run the API function to get the data for that date. 
if ExportGamedayData(requestedDate):
    sys.exit('\n Completed Succsessfully!')
else:
    sys.exit('\n Errors during execution.')