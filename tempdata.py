import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process
import datetime

def openCsv():
    gf = pd.read_csv("DataForDatabase/data.csv",sep=";")
    df = gf.drop(gf.columns[gf.columns.str.contains('^Spalte')], axis=1)
    return df

def filterTeamNames(data):
    resultHome = []
    resultAway = []
    for i in data['HomeTeam']:
        if(fuzz.token_set_ratio("Dortmund",i) == 100):
            resultHome.append(1)
        if(fuzz.token_set_ratio("Hamburg",i) == 100):
            resultHome.append(2)
        if(fuzz.token_set_ratio("Augsburg",i) == 100):
            resultHome.append(3)
        if(fuzz.token_set_ratio("Freiburg",i) == 100):
            resultHome.append(4)
        if(fuzz.token_set_ratio("Koln",i) == 100):
            resultHome.append(5)
        if(fuzz.token_set_ratio("Wolfsburg",i) == 100):
            resultHome.append(6)
        if(fuzz.token_set_ratio("Hannover",i) == 100):
            resultHome.append(7)
        if(fuzz.token_set_ratio("Hoffenheim",i) == 100):
            resultHome.append(8)
        if(fuzz.token_set_ratio("Hertha",i) == 100):
            resultHome.append(9)
        if(fuzz.token_set_ratio("Nurnberg",i) == 100):
            resultHome.append(10)
        if(fuzz.token_set_ratio("Stuttgart",i) == 100):
            resultHome.append(11)
        if(fuzz.token_set_ratio("Schalke",i) == 100):
            resultHome.append(12)
        if(fuzz.token_set_ratio("Bremen",i) == 100):
            resultHome.append(13)
        if(fuzz.token_set_ratio("Kaiserslautern",i) == 100):
            resultHome.append(14)
        if(fuzz.token_set_ratio("Munich",i) == 100):
            resultHome.append(15)
        if(fuzz.token_set_ratio("M'gladbach",i) == 100):
            resultHome.append(16)
        if(fuzz.token_set_ratio("Mainz",i) == 100):
            resultHome.append(17)
        if(fuzz.token_set_ratio("Leverkusen",i) == 100):
            resultHome.append(18)
        if(fuzz.token_set_ratio("Dusseldorf",i) == 100):
            resultHome.append(19)
        if(fuzz.token_set_ratio("Furth",i) == 100):
            resultHome.append(20)
        if(fuzz.token_set_ratio("Braunschweig",i) == 100):
            resultHome.append(21)
        if(fuzz.token_set_ratio("Paderborn",i) == 100):
            resultHome.append(22)
        if(fuzz.token_set_ratio("Darmstadt",i) == 100):
            resultHome.append(23)
        if(fuzz.token_set_ratio("Ingolstadt",i) == 100):
            resultHome.append(24)
        if(fuzz.token_set_ratio("Leipzig",i) == 100):
            resultHome.append(25)
        if(fuzz.token_set_ratio("Pauli",i) == 100):
            resultHome.append(26)
        if(fuzz.token_set_ratio("Bochum",i) == 100):
            resultHome.append(27)
        if(fuzz.token_set_ratio("Union",i) == 100):
            resultHome.append(28)
        if(fuzz.token_set_ratio("Frankfurt",i) == 100):
            resultHome.append(29)

    for i in data['AwayTeam']:
        if(fuzz.token_set_ratio("Dortmund",i) == 100):
            resultAway.append(1)
        if(fuzz.token_set_ratio("Hamburg",i) == 100):
            resultAway.append(2)
        if(fuzz.token_set_ratio("Augsburg",i) == 100):
            resultAway.append(3)
        if(fuzz.token_set_ratio("Freiburg",i) == 100):
            resultAway.append(4)
        if(fuzz.token_set_ratio("Koln",i) == 100):
            resultAway.append(5)
        if(fuzz.token_set_ratio("Wolfsburg",i) == 100):
            resultAway.append(6)
        if(fuzz.token_set_ratio("Hannover",i) == 100):
            resultAway.append(7)
        if(fuzz.token_set_ratio("Hoffenheim",i) == 100):
            resultAway.append(8)
        if(fuzz.token_set_ratio("Hertha",i) == 100):
            resultAway.append(9)
        if(fuzz.token_set_ratio("Nurnberg",i) == 100):
            resultAway.append(10)
        if(fuzz.token_set_ratio("Stuttgart",i) == 100):
            resultAway.append(11)
        if(fuzz.token_set_ratio("Schalke",i) == 100):
            resultAway.append(12)
        if(fuzz.token_set_ratio("Bremen",i) == 100):
            resultAway.append(13)
        if(fuzz.token_set_ratio("Kaiserslautern",i) == 100):
            resultAway.append(14)
        if(fuzz.token_set_ratio("Munich",i) == 100):
            resultAway.append(15)
        if(fuzz.token_set_ratio("M'gladbach",i) == 100):
            resultAway.append(16)
        if(fuzz.token_set_ratio("Mainz",i) == 100):
            resultAway.append(17)
        if(fuzz.token_set_ratio("Leverkusen",i) == 100):
            resultAway.append(18)
        if(fuzz.token_set_ratio("Dusseldorf",i) == 100):
            resultAway.append(19)
        if(fuzz.token_set_ratio("Furth",i) == 100):
            resultAway.append(20)
        if(fuzz.token_set_ratio("Braunschweig",i) == 100):
            resultAway.append(21)
        if(fuzz.token_set_ratio("Paderborn",i) == 100):
            resultAway.append(22)
        if(fuzz.token_set_ratio("Darmstadt",i) == 100):
            resultAway.append(23)
        if(fuzz.token_set_ratio("Ingolstadt",i) == 100):
            resultAway.append(24)
        if(fuzz.token_set_ratio("Leipzig",i) == 100):
            resultAway.append(25)
        if(fuzz.token_set_ratio("Pauli",i) == 100):
            resultAway.append(26)
        if(fuzz.token_set_ratio("Bochum",i) == 100):
            resultAway.append(27)
        if(fuzz.token_set_ratio("Union",i) == 100):
            resultAway.append(28)
        if(fuzz.token_set_ratio("Frankfurt",i) == 100):
            resultAway.append(29)
    
    print(len(resultAway))
    new_df = pd.DataFrame({'HomeTeam' : resultHome, 'AwayTeam' : resultAway})
    data.update(new_df)
    data.to_csv('newData.csv', index= False)
    return data




test = "08.05.2010"
datatemp = datetime.datetime.strptime(test,'%d.%m.%Y')
temp = datatemp.strftime("%Y-%m-%d")
datatemp = datetime.datetime.strptime(temp,"%Y-%m-%d")
print(type(datatemp))