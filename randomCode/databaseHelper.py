import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime

class DatabaseHelper():
    def __init__(self):
        return None

    @classmethod
    def test(self):
        print("Test")

    def createServerConnection(self,host_name, user_name, user_password):
        connection = None
        try:
            connection = mysql.connector.connect(
                host= host_name,
                user= user_name,
                passwd= user_password
            )
            print("Connection Succesful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection

    def createDbConnection(self,host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host = host_name,
                user = user_name,
                passwd = user_password,
                database = db_name
            )
            print("Database Connection Succesful")

        except Error as err:
            print(f"Error: '{err}'")

        return connection

    def executeQuery(self,connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query succesful")

        except Error as err:
            print(f"Error: '{err}'")

    def getTeamnames(self,connection):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute("""SELECT * FROM tamenames""")
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")

    #Query to add single match 
    def insertMatch(self,connection,index,division,date,hid,aid,fthg,ftag,ftr,hthg,athg,htr,hss,ass,hst,ast,hf,af,hc,ac,hy,ay,hr,ar):
        insert_matche = """ 
        INSERT INTO matches VALUES
            (%s, '%s', '%s', %s, %s, %s, %s, '%s', %s, %s, '%s', %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """%(index,division,date,hid,aid,fthg,ftag,ftr,hthg,athg,htr,hss,ass,hst,ast,hf,af,hc,ac,hy,ay,hr,ar)
        self.executeQuery(connection,insert_matche)

    def insertMatches(self,connection,data):
        for index,row in data.iterrows():
            self.insertMatch(connection,index,row['Div'],
            datetime.datetime.strptime(row['Date'],"%d.%m.%Y"),row['HomeTeam'],row['AwayTeam'],
            row['FTHG'],row['FTAG'],row['FTR'],
            row['HTHG'],row['HTAG'],row['HTR'],row['HS'],row['AS'],
            row['HST'],row['AST'],row['HF'],row['AF'],row['HC'],row['AC'],
            row['HY'],row['AY'],row['HR'],row['AR'])

    def updateHomeMatches(self, connection, data):
        for i in data:
            form = (i[1] / 91) * 100
            insert = """
            UPDATE `matches` SET `hometeamform` = %s WHERE `date` >= "2011-08-05" 
            AND `date` <= "2011-05-14" AND `hometeamid` = %s
            """%(form, i[0])
            self.executeQuery(connection, insert)
            
    def updateAwayMatches(self, connection, data):
        for i in data:
            form = (i[1] / 91) * 100
            second = """
            UPDATE `matches` SET `awayteamform` = %s WHERE `date` >= "2011-08-05" 
            AND `date` <= "2011-05-14" AND `awayteamid` = %s
            """%(form, i[0])
            self.executeQuery(connection, second)

    def openCsv(self):
        gf = pd.read_csv("newData.csv",sep=";")
        df = gf.drop(gf.columns[gf.columns.str.contains('^Spalte')], axis=1)
        return df


# init_pop_teamnames = """
# INSERT INTO tamenames VALUES
#     (1,'Dortmund'),
#     (2,'Hamburg'),
#     (3,'Augsburg'),
#     (4,'Freiburg'),
#     (5,'Koln'),
#     (6,'Wolfsburg'),
#     (7,'Hannover'),
#     (8,'Hoffenheim'),
#     (9,'Hertha'),
#     (10,'Nurnberg'),
#     (11,'Stuttgart'),
#     (12,'Schalke'),
#     (13,'Bremen'),
#     (14,'Kaiserslautern'),
#     (15,'Munich'),
#     (16,'Gladbach'),
#     (17,'Mainz'),
#     (18,'Leverkusen'),
#     (19,'Dusseldorf'),
#     (20,'Furth'),
#     (21,'Braunschweig'),
#     (22,'Paderborn'),
#     (23,'Darmstadt'),
#     (24,'Ingolstadt'),
#     (25,'Leipzig'),
#     (26,'Pauli'),
#     (27,'Bochum'),
#     (28,'Union'),
#     (29,'Frankfurt');
# """


# conn = create_db_connection("localhost", "root", "password", "bot")
# data = openCsv()
# insert_matches(conn,data)
#execute_query(conn, init_pop_teamnames) <- Used to initaly insert Teamnames into Database
# names = getTeamnames(conn)
# for result in names:
#     #TeamID
#     print(result[0])
#     #TeamName
#     print(result[1])