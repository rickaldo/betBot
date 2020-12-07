import pandas as pd
import numpy as np
import glob
import re 
import pprint as p

class DataPrep():
    def __init__():
        return null

    #Table Generatng 
    def getGameTable():
        game_filenames = list(glob.glob("../../FootballData/Games/20*.csv"))
        gf = [pd.read_csv(filename) for filename in game_filenames]
        game_filename = [f for f in gf]
        gametables = pd.concat(game_filename, ignore_index=True)
        
        return gametables 

    def getPlacementTable():      
        placement_filenames = list(glob.glob("../../FootballData/Placement/20*.csv"))
        pf = []
        for filename in placement_filenames:
            df = pd.read_csv(filename,sep=";")
            search_year = re.search(r'\b[0-9]{4}\b',filename)
            df = df.assign(year = search_year.group())
            pf.append(df) 
        placementtables = pd.concat(pf, ignore_index=True)
        placementtables = placementtables.sort_values(by="year")

        return placementtables

        
    def getAllTimeMatchUps():
        all_time_table = getGameTable().iloc[:,1:6].copy()
        all_time_table["Date"] = pd.to_datetime(all_time_table["Date"])
        all_time_table = all_time_table.sort_values(by="Date")
        all_time_table = all_time_table.reset_index()
        del all_time_table['index']
        
        return all_time_table

    #-> sum_of_points sind die gesamt Anzahl der Punkte, die jede BL-Mannschaft in den letzten
    #-> 10 Jahren geholt hat.
    def getAllTimePointsTable():
        placementtables = getPlacementTable()
        all_teams = []
        
        for i in placementtables['Mannschaft']:
            if(i in all_teams):
                continue
            else:
                all_teams.append(i)

        listed_placements = []
        for i in all_teams:
            listed_placements.append(placementtables.loc[placementtables['Mannschaft'] == i])

        sum_of_points = {}
        for i in listed_placements:
            total = i['Punke'].sum()
            name = i['Mannschaft'].iloc[0]
            sum_of_points.update({ name : total})

        sum_of_points = sorted(sum_of_points.items(), key=lambda item: item[1])
        
        return sum_of_points

    #Return Table with All Teams and [Goals Scored, Goals Conceded, Goal Difference]

    def find_td(series):
        goals = []
        made = []
        conceded = []
        for string in series:
            tmp = string[:string.find("(")]
            goals_made = tmp[:tmp.find(":")]
            goals_conceded = tmp[tmp.find(":"):]
            made.append(goals_made)
            conceded.append(goals_conceded[1:].replace(u'\xa0', ''))
        goals.append(made)
        goals.append(conceded)
        return goals

    def getSortedPlacementTable():
        placementtables = getPlacementTable()
        all_teams = []
        for i in placementtables['Mannschaft']:
            if(i in all_teams):
                continue
            else:
                all_teams.append(i)

        listed_placements = []
        for i in all_teams:
            listed_placements.append(placementtables.loc[placementtables['Mannschaft'] == i])
            
        return listed_placements

    def getAllTimeGoalDiff():
        listed_placements = getSortedPlacementTable()
        
        goal_difference = []
        goal_diff_dic = {}
        for i in listed_placements:
            gd = i['TD']
            name = i['Mannschaft'].iloc[0]
            goal_diff_dic.update({name : gd})

        all_time_goal_dif_dic = {}

        for key, value in goal_diff_dic.items():
            #if key == "Borussia Dortmund":
            tmp = find_td(value)
            goals_made = list(map(int,tmp[0]))
            goals_conceded = list(map(int,tmp[1]))
            sm_gm = sum(goals_made)
            sm_gc = sum(goals_conceded)
            all_time_goal_dif_dic.update({key: [sm_gm,sm_gc,sm_gm-sm_gc]})
        
        return all_time_goal_dif_dic

    #Creates an function (inDepthGameResults) which needs an Table (create by func getGameResults) 
    #which Calculates the past Matches between two Teams and creates an shows how often the 
    #result was > 2.5

    def getGameResults(hometeam, awayteam):
        all_time_table = getAllTimeMatchUps()
        result = all_time_table.where((all_time_table['HomeTeam'].str.contains(hometeam)) 
                                & (all_time_table['AwayTeam'].str.contains(awayteam)) 
                                    |(all_time_table['AwayTeam'].str.contains(hometeam)) 
                                & (all_time_table['HomeTeam'].str.contains(awayteam)))
        return result.dropna()


    def inDepthGameResults(table):
        if(len(table) > 8):
            #return table.where(table["FTHG"] > table["FTAG"])
            resultlist = []
            for index, row in table.iterrows():
                homeTeam = row.loc["HomeTeam"]
                awayTeam = row.loc["AwayTeam"]
                homeGoals = row.loc["FTHG"]
                awayGoals = row.loc["FTAG"]

                if(homeGoals > awayGoals):
                    resultdict = {
                        "Mannschaft" : homeTeam,
                        "OverUnder" : homeGoals + awayGoals,
                        "Winner": True
                    }
                    resultlist.append(resultdict)
                elif(homeGoals < awayGoals):
                    resultdict = {
                        "Mannschaft" : awayTeam,
                        "OverUnder" : homeGoals + awayGoals,
                        "Winner": True
                    }
                    resultlist.append(resultdict)
                else: 
                    resultdict = {
                        "Mannschaft" : homeTeam + ";" + awayTeam,
                        "OverUnder" : homeGoals + awayGoals,
                        "Winner": False
                    }
                    resultlist.append(resultdict)
        else: 
            resultlist = "Not enough MatchUps played"
        return resultlist

    def getOverUnderResult(hometeam, awayteam):
        matchUp = getGameResults(hometeam,awayteam) 
        matchUpResult = inDepthGameResults(matchUp)

        resultTmpList = []
        if(type(matchUpResult) is str):
            return "Not enough MatchUps played"
        else:
            for i in matchUpResult: 
                if(i.get("OverUnder") > 2.5):
                    resultTmpList.append(True)
                else: 
                    resultTmpList.append(False)
                    
            length = len(resultTmpList)
            summe = sum(resultTmpList)
            result = {
                'Over' : summe,
                'Under': length - summe,
                'Total': length
            }
            return result

    def getAllTimeGamesPlayed():
        table = getSortedPlacementTable()
        gamesPlayedDict = {}
        for i in table:
            played = i['Spiele']
            team = i['Mannschaft'].iloc[0]
            gamesPlayedDict.update({ team: played})

        allTimeGamesPlayed = {}
        for key, value in gamesPlayedDict.items():
            gamesPlayed = sum(value)
            allTimeGamesPlayed.update({ key : gamesPlayed })

            
        return allTimeGamesPlayed