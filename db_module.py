import os
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

import platform

whatos = platform.system()
print(whatos)

global USER, PASSWORD, engine, conn, cursor
USER = os.environ["USERNAME"] = "postgres"
PASSWORD = os.environ["PASSWORD"] = "aaronwise"
conn_string = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@localhost:5432/English Football Data"
)
engine = create_engine(conn_string, echo=True)

# try:
#    conn = psycopg2.connect(
#        database="Football_Data", user=USER, password=PASSWORD, port=5432
#    )
# except psycopg2.OperationalError as err:
#    print(err)
#    conn = None


# addToDB needs to be able to create new tables based on varying number of columns-
# def addToDB(data, league):
#    league = str(league)
#    sql_string = f"drop table if exists {league}  \n"
#    sql_string += f"create table {league}   \n"

#    for colname in data.columns:
#        dataType = input(f"enter dtype for {colname}: ")
#        sql_string += f"{colname} {dataType}   \n"

#    print(sql_string)
#    primary = input("enter primary key: ")

#    sql_string += f"PRIMARY KEY {primary}"

#    print(sql_string)
#    cursor.execute(sql_string)

#    data.to_sql("data", con=engine, if_exists="replace", index=False, method="multi")
#    return


def addAllData(data, league):
    if league == "E0":
        league = "prem"
    elif league == "E1":
        league = "champ"
    elif league == "E2":
        league = "L1"
    elif league == "E3":
        league = "L2"
    elif league == "EC":
        league = "Conf"
    data.to_sql(
        f"{league}_full_league_data",
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
    )
    return print("it worked...?")


def grabData(sql_string):
    data = pd.read_sql(sql_string, engine)
    print(sql_string)
    return data


def pullAllData():
    data = pd.read_sql_query("select * from all_leagues", con=engine)
    teams = pd.read_sql_query("select * from all_teams", con=engine)
    return data, teams


def buildTeamTable(data, team):
    title = team.replace("'", "")
    title = title.replace(" ", "_")
    title = title.lower()
    dum = data.loc[data["HomeTeam"] == team]
    dum2 = data.loc[data["AwayTeam"] == team]
    dum = pd.concat([dum, dum2])
    dum.to_sql(
        f"{title}_game_data",
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
    )
    return
