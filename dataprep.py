from randomCode import databaseHelper as dbhelper
from fuzzywuzzy import fuzz, process

class Datapreperation():
    def __init__(self, hostname, username, password, dbName):
        self.dbh = dbhelper.DatabaseHelper()
        self.connection = self.dbh.createDbConnection(hostname, username, password,dbName)

    #Fetch TeamID from Database, needs the Teams already fetched; 
    #Optional Teams could be fetched in Method depends on Classstructure later;
    #Home and Awayteam will Come from API or is entered via User
    #TeamIds will be returned in Array, [0] == Hometeam [1] == Awayteam
    def getTeamIDs(self,hometeam,awayteam):
        teams = self.dbh.getTeamnames(self.connection)
        homeTeamID = ""
        awayTeamID = ""

        for i in teams:
            if(fuzz.token_set_ratio(hometeam,i[1]) == 100):
                homeTeamID = i[0]
            elif(fuzz.token_set_ratio(awayteam,i[1]) == 100):
                awayTeamID = i[0]
        
        if(homeTeamID == ""):
            print("No HomeTeam found")
            return None
        if(awayTeamID == ""):
            print("No AwayTeam found")
            return None

        return [homeTeamID,awayTeamID]
    
    #returns the Matches that the Teams played against each other.;
    #needs the Connection to the Database and the TeamIDArray
    def getMatchesOfTeams(self, teamIDArray):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute("""SELECT * FROM matches WHERE hometeamid=%s and awayteamid=%s or hometeamid=%s and awayteamid=%s"""%(teamIDArray[0],teamIDArray[1],teamIDArray[1],teamIDArray[0]))
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")

    #Sorts the Data. Returns a Dict with Arrays
    def sortDataForCalculation(self, matches, team1, team2):
        if(len(matches) < 8):
            return None
        #All Goals for Goals
        totalGoal = []    
        #Team1 Goals
        team1HomeGoalsFT = []
        team1AwayGoalsFT = []
        team1HomeGoalsHT = []
        team1AwayGoalsHT = []
        team1TotalGoals = []
        #Team1 Cards
        team1YellowCards = []
        team1RedCards = []
        #Team1 Corners
        team1Corners = []
        #Team1 Fouls
        team1Fouls = []
        #Team1 Shots
        team1Shots = []
        team1ShotsOnTarget = []

        #Team2 Goals
        team2HomeGoalsFT = []
        team2AwayGoalsFT = []
        team2HomeGoalsHT = []
        team2AwayGoalsHT = []
        teams2TotalGoals = []
        #Team2 Cards
        team2YellowCards = []
        team2RedCards = []
        #Team2 Corners
        team2Corners = []
        #Team2 Fouls
        team2Fouls = []
        #Team2 Shots
        team2Shots = []
        team2ShotsOnTarget = []
        
        for match in matches:
            #Fulltime Home- and Awaygoal added for later Calculation
            totalGoal.append(match[5])
            totalGoal.append(match[6])
            
            #Team1 is HomeTeam
            if(match[3] == team1 and match[4] == team2):
                team1HomeGoalsFT.append(match[5])
                team1HomeGoalsHT.append(match[8])
                team1YellowCards.append(match[19])
                team1RedCards.append(match[21])
                team1Corners.append(match[17])
                team1Fouls.append(match[15])
                team1Shots.append(match[11])
                team1ShotsOnTarget.append(match[13])
                team2AwayGoalsFT.append(match[6])
                team2AwayGoalsHT.append(match[9])
                team2YellowCards.append(match[20])
                team2RedCards.append(match[22])
                team2Corners.append(match[18])
                team2Fouls.append(match[16])
                team2Shots.append(match[12])
                team2ShotsOnTarget.append(match[14])
            #Team2 is HomeTeam
            elif(match[3] == team2 and match[4] == team1):
                team2HomeGoalsFT.append(match[5])
                team2HomeGoalsHT.append(match[8])
                team2YellowCards.append(match[19])
                team2RedCards.append(match[21])
                team2Corners.append(match[17])
                team2Fouls.append(match[15])
                team2Shots.append(match[11])
                team2ShotsOnTarget.append(match[13])
                team1AwayGoalsFT.append(match[6])
                team1AwayGoalsHT.append(match[9])
                team1YellowCards.append(match[20])
                team1RedCards.append(match[22])
                team1Corners.append(match[18])
                team1Fouls.append(match[16])
                team1Shots.append(match[12])
                team1ShotsOnTarget.append(match[14])

        return {
        'team1': team1,
        'team2': team2,
        'totalGoals': totalGoal,
        'team1HomeGoalsFT': team1HomeGoalsFT,
        'team1HomeGoalsHT': team1HomeGoalsHT,
        'team1AwayGoalsFT': team1AwayGoalsFT,
        'team1AwayGoalsHT': team1AwayGoalsHT,
        'team1YellowCard': team1YellowCards,
        'team1RedCard': team1RedCards,
        'team1Fouls': team1Fouls,
        'team1Corners': team1Corners,
        'team1Shots': team1Shots,
        'team1ShotsOnTarget': team1ShotsOnTarget,
        'team2HomeGoalsFT': team2HomeGoalsFT,
        'team2HomeGoalsHT': team2HomeGoalsHT,
        'team2AwayGoalsFT': team2AwayGoalsFT,
        'team2AwayGoalsHT': team2AwayGoalsHT,
        'team2YellowCard': team2YellowCards,
        'team2RedCard': team2RedCards,
        'team2Fouls': team2Fouls,
        'team2Corners': team2Corners,
        'team2Shots': team2Shots,
        'team2ShotsOnTarget': team2ShotsOnTarget,
    }

#Calculates the Average of the given Array
def calculateAverage(self, array):
    ArraySum = sum(c for c in array)
    return ArraySum / len(array)