import json
import csv
import sys
import os
import pandas as pd
import re
import requests
from datetime import date

# Create our "Static" variables. 
today = (date.today()).strftime("%Y-%m-%d")
filepath = os.path.dirname(os.path.realpath(__file__))

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
    requestedDate = input("Please enter in a date. Format: YYYY-MM-DD. Leave blank for today. \n  Date: ")
    if not requestedDate:
        requestedDate = today
    if requestedDate:
        matched = re.match("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]", requestedDate)
        is_match = bool(matched)
        if is_match:
            return(requestedDate)
        else:
            print("Error: Please format date as YYYY-MM-DD.")
            GetRequestedDate()

def InvokeApiRequest(requestURL):
    try:
        data = requests.get(requestURL)
        return data
    except requests.exceptions.Timeout:
        print("We are heving issues communicating with the API... \n Trying again...")
        InvokeApiRequest(requestURL)
    except requests.exceptions.RequestException as e:
        print("Error with web request.")
        raise SystemExit(e)

def CreateCsvFile(requestedDate, gameday_DF):
    csv_file = filepath + "\\" + requestedDate + "_Gameday_Data.csv"
    try:
        gameday_DF.to_csv(csv_file, index=False)
        print("CSV Exported. Please check the working directory for your file.")
        sys.exit()
    except IOError:
        while "Invalid response...":
            reply = input("Error writing to file! You may have the file you're trying to write to open. \n Please close the file and try again. \n Try Again? [Y/N]").capitalize().strip()
            if (reply == 'Y' or reply == 'YES'):
                CreateCsvFile(requestedDate, gameday_DF)
            if (reply == 'N' or reply == 'NO'):
                sys.exit("Could not export to file.")

def GetGamedayData():
    requestedDate = GetRequestedDate()
    requestAPIUrl = "http://gd2.mlb.com/components/game/mlb/year_{}/month_{}/day_{}/grid.json".format(str(requestedDate[0:4]), str(requestedDate[5:7]), str(requestedDate[8:10]))

    apiResponse = (InvokeApiRequest(requestAPIUrl)).json()
    
    try:
        gamedayDataJson = apiResponse["data"]["games"]["game"]
    except:
        reply = (input("No game data for that date. \n Try another date? [Y/N]")).capitalize().strip()
        if (reply == 'Y' or reply == 'YES'):
            GetGamedayData()
        elif (reply == 'N' or reply == 'NO'):
            sys.exit("Could not find data for requested day.")
        else:
            print("Please choose Y or N. (Yes or No)")        
        
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
    CreateCsvFile(requestedDate, gameday_DF)
    
GetGamedayData()