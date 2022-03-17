import pandas as pd
import numpy as np
import random
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import lxml
from os.path import exists
from fuzzywuzzy import fuzz
import itertools
from fuzzywuzzy import process


def getSomeEnglishData(year_one, last_year):
    prem = getAllEnglishData(year_one, last_year, "E0")
    champ = getAllEnglishData(year_one, last_year, "E1")
    l1 = getAllEnglishData(year_one, last_year, "E2")
    l2 = getAllEnglishData(year_one, last_year, "E3")

    return prem, champ, l1, l2


def getCurrentTeams():
    prem_list = []
    url = "https://www.skysports.com/premier-league-table"
    response = requests.get(url)
    page = response.text
    soup = bs(page, "html.parser")
    test = soup.find_all("a", class_="standing-table__cell--name-link")
    # print(len(test))
    for i in test:
        i = str(i.text)
        i = i.replace("*", "")
        prem_list.append(i)
    prem_table = pd.DataFrame(prem_list, columns={"Team"})

    champ_list = []
    url = "https://www.skysports.com/championship-table"
    response = requests.get(url)
    page = response.text
    soup = bs(page, "html.parser")
    test = soup.find_all("a", class_="standing-table__cell--name-link")
    # print(len(test))
    for i in test:
        i = str(i.text)
        i = i.replace("*", "")
        champ_list.append(i)
    champ_table = pd.DataFrame(champ_list, columns={"Team"})

    l1_list = []
    url = "https://www.skysports.com/league-1-table"
    response = requests.get(url)
    page = response.text
    soup = bs(page, "html.parser")
    test = soup.find_all("a", class_="standing-table__cell--name-link")
    # print(len(test))
    for i in test:
        i = str(i.text)
        i = i.replace("*", "")
        l1_list.append(i)
    l1_table = pd.DataFrame(l1_list, columns={"Team"})

    l2_list = []
    url = "https://www.skysports.com/league-2-table"
    response = requests.get(url)
    page = response.text
    soup = bs(page, "html.parser")
    test = soup.find_all("a", class_="standing-table__cell--name-link")
    # print(len(test))
    for i in test:
        i = str(i.text)
        i = i.replace("*", "")
        l2_list.append(i)
    l2_table = pd.DataFrame(l2_list, columns={"Team"})

    return prem_table, champ_table, l1_table, l2_table


def getAllEnglishData(year_one, last_year, league):
    print("league: ", league)
    # leagues = ["E0", "E1", "E2", "E3"]
    df_full = pd.DataFrame()

    for j in range(year_one, last_year):
        df = pd.read_csv(
            f"https://www.football-data.co.uk/mmz4281/{j:02}{j+1:02}/{league}.csv",
        )
        df = df.rename(
            columns={
                "FTHG": "HomeGoals",
                "FTAG": "AwayGoals",
                "HTHG": "HalfTimeHomeGoals",
                "HTAG": "HalfTimeAwayGoals",
                "HS": "HomeShots",
                "AS": "AwayShots",
                "HST": "HomeShotsTarget",
                "AST": "AwayShotsTarget",
                "HF": "HomeFouls",
                "AF": "AwayFouls",
                "HY": "HomeYellow",
                "AY": "AwayYellow",
                "HR": "HomeRed",
                "AR": "AwayRed",
            }
        )
        data = pd.DataFrame(df)
        data["league"] = league
        df_full = pd.concat([data, df_full])
        # df_full = df_full.reset_index(inplace=True)
    df_full["game_id"] = np.random.randint(100000, 999999, size=len(df_full))
    df_full.reset_index(drop=True)

    return df_full


def getTeams(prem, champ, l1, l2):
    if (
        exists("prem_teams.csv")
        & exists("champ_teams.csv")
        & exists("l1_teams.csv")
        & exists("l2_teams.csv")
    ):
        prem_teams = pd.read_csv("prem_teams.csv")
        champ_teams = pd.read_csv("champ_teams.csv")
        l1_teams = pd.read_csv("l1_teams.csv")
        l2_teams = pd.read_csv("l2_teams.csv")

        return prem_teams, champ_teams, l1_teams, l2_teams

    prem_teams = pd.DataFrame(prem["HomeTeam"].unique(), columns={"Team"})

    champ_teams = pd.DataFrame(champ["HomeTeam"].unique(), columns={"Team"})

    l1_teams = pd.DataFrame(l1["HomeTeam"].unique(), columns={"Team"})

    l2_teams = pd.DataFrame(l2["HomeTeam"].unique(), columns={"Team"})

    full_team_df = prem_teams.merge(champ_teams, how="outer")
    full_team_df = full_team_df.merge(l1_teams, how="outer")
    full_team_df = full_team_df.merge(l2_teams, how="outer")
    full_team_df["team_id"] = np.random.randint(100, 999, size=len(full_team_df))

    prem_teams = prem_teams.merge(full_team_df)
    champ_teams = champ_teams.merge(full_team_df)
    l1_teams = l1_teams.merge(full_team_df)
    l2_teams = l2_teams.merge(full_team_df)

    return prem_teams, champ_teams, l1_teams, l2_teams, full_team_df


def teamGoals(data, teamList):
    total_home_scored = data["HomeGoals"].sum()
    total_away_scored = data["AwayGoals"].sum()
    # Home Goals mean
    dfHomeGoals = pd.DataFrame(data[["HomeTeam", "HomeGoals"]])
    dfHomeGoals = dfHomeGoals.rename(
        columns={"HomeTeam": "Team", "HomeGoals": "HomeScored"}
    )
    dfHomeGoals = dfHomeGoals.groupby(["Team"]).agg({"HomeScored": "mean"})

    # Home concended mean
    dfHomeConced = pd.DataFrame(data[["HomeTeam", "AwayGoals"]])
    dfHomeConced = dfHomeConced.rename(
        columns={"HomeTeam": "Team", "AwayGoals": "HomeConceded"}
    )
    dfHomeConced = dfHomeConced.groupby(["Team"]).agg({"HomeConceded": "mean"})

    # Away goals mean
    dfAwayGoals = pd.DataFrame(data[["AwayTeam", "AwayGoals"]])
    dfAwayGoals = dfAwayGoals.rename(
        columns={"AwayTeam": "Team", "AwayGoals": "AwayScored"}
    )
    dfAwayGoals = dfAwayGoals.groupby(["Team"]).agg({"AwayScored": "mean"})

    # Away conceded mean
    dfAwayConced = pd.DataFrame(data[["AwayTeam", "HomeGoals"]])
    dfAwayConced = dfAwayConced.rename(
        columns={"AwayTeam": "Team", "HomeGoals": "AwayConceded"}
    )
    dfAwayConced = dfAwayConced.groupby(["Team"]).agg({"AwayConceded": "mean"})

    # merge tables
    dfGoalRatings = dfHomeGoals.merge(dfHomeConced, right_on="Team", left_on="Team")
    dfGoalRatings = dfGoalRatings.merge(dfAwayGoals, right_on="Team", left_on="Team")
    dfGoalRatings = dfGoalRatings.merge(dfAwayConced, right_on="Team", left_on="Team")
    dfGoalRatings = dfGoalRatings.merge(teamList, right_on="Team", left_on="Team")

    # build team ratings
    home_scored_rat = data["HomeGoals"].sum()
    home_conceded_rat = data["AwayGoals"].sum()
    away_scored_rat = data["AwayGoals"].sum()
    away_conceded_rat = data["AwayGoals"].sum()

    dfGoalRatings["HomeAttackStrength"] = dfGoalRatings["HomeScored"] / home_scored_rat
    dfGoalRatings["HomeDefenseStrength"] = (
        dfGoalRatings["HomeConceded"] / home_conceded_rat
    )
    dfGoalRatings["AwayAttackStrength"] = dfGoalRatings["AwayScored"] / away_scored_rat
    dfGoalRatings["AwayDefenseStrength"] = (
        dfGoalRatings["AwayConceded"] / away_conceded_rat
    )

    dfGoalRatings = dfGoalRatings.reset_index(drop=True)

    total_dict = {
        "total_home_scored": total_home_scored,
        "total_away_scored": total_away_scored,
    }

    return dfGoalRatings, total_dict


def getWeights(league_to, league_from):
    pd.set_option("display.max_columns", None)
    league_to["HomeScoredWeight"] = league_to["HomeScored"] / league_from["HomeScored"]
    league_to["HomeConcededWeight"] = (
        league_to["HomeConceded"] / league_from["HomeConceded"]
    )
    league_to["AwayScoredWeight"] = league_to["AwayScored"] / league_from["AwayScored"]
    league_to["AwayConcededWeight"] = (
        league_to["AwayConceded"] / league_from["AwayConceded"]
    )
    league_to["HomeAttackStrength"] = (
        league_to["HomeAttackStrength"] / league_from["HomeAttackStrength"]
    )
    league_to["HomeDefenseStrength"] = (
        league_to["HomeDefenseStrength"] / league_from["HomeDefenseStrength"]
    )
    league_to["AwayAttackStrength"] = (
        league_to["AwayAttackStrength"] / league_from["AwayAttackStrength"]
    )
    league_to["AwayDefenseStrength"] = (
        league_to["AwayDefenseStrength"] / league_from["AwayDefenseStrength"]
    )
    league_to.reset_index(drop=True)
    league_to.dropna(inplace=True)

    weight_dict = {}

    weight_dict["hg_weight"] = league_to["HomeScoredWeight"].mean()
    weight_dict["hc_weight"] = league_to["HomeConcededWeight"].mean()
    weight_dict["as_weight"] = league_to["AwayScoredWeight"].mean()
    weight_dict["ac_weight"] = league_to["AwayConcededWeight"].mean()
    weight_dict["has_weight"] = league_to["HomeAttackStrength"].mean()
    weight_dict["hds_weight"] = league_to["HomeDefenseStrength"].mean()
    weight_dict["aas_weight"] = league_to["AwayAttackStrength"].mean()
    weight_dict["ads_weight"] = league_to["AwayDefenseStrength"].mean()

    return (league_to, weight_dict)


def updateTables(teams, current_teams):
    n = 0
    for i in teams.Team:
        print(f"\n name: {i} ##### num: {n}")
        i = str(i)
        replacement = process.extractOne(i, current_teams.Team)
        if replacement[1] > 89:
            print(replacement[0:2])
            print("#########: ", i)
            current_teams["Team"].replace(replacement, i, inplace=True)
        elif replacement[1] > 60 & replacement[1] < 89:
            print(replacement[0:2])
            print("#########: ", i)
            replace = input("replace: ")
            if replace:
                current_teams["Team"].replace(replacement, i, inplace=True)
        else:
            continue
        n += 1

    current_teams = current_teams.merge(teams, how="inner")

    return current_teams


def checkTable(teams, current_teams):
    print(current_teams)
    check = input("if done enter 'y'")
    if check:
        return current_teams
    current_teams = appendByID(teams, current_teams)
    return current_teams


def appendByID(teams, current_teams):
    pd.set_option("display.max_rows", None)
    while True:
        print(teams)
        print(current_teams)

        team_id = int(input("enter team id: "))
        print(type(team_id))
        team_location = teams.loc[teams["team_id"] == team_id]
        print(team_location)
        current_teams = pd.concat([current_teams, team_location])

        done = input("if done, enter 'y'")
        if done == "y":
            return current_teams

    return


def buildSchedule(current_teams):
    num = 0
    teams = current_teams["Team"].unique()
    season = pd.DataFrame()
    for pair in itertools.permutations(teams, 2):
        dummy = pd.DataFrame([[pair[0], pair[1]]])
        season = pd.concat([season, dummy], ignore_index=True)
        num += 1
    season = season.rename(columns={0: "home", 1: "away"})
    return season


def createLeagueTable(current_teams):
    columns = ["Team", "Points"]
    current_table = pd.DataFrame(columns=columns)
    current_table["Team"] = current_teams["Team"].unique()
    current_table["Points"] = current_table["Points"].fillna(0)
    current_table.index += 1
    return current_table
