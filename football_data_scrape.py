import pandas as pd


def getSomeEnglishData(year_one, last_year, league):
    if str(league) == "premier":
        league = "E0"
    elif str(league) == "championship":
        league = "E1"
    elif str(league) == "League 1":
        league = "E2"
    elif str(league) == "League 2":
        league = "E3"
    elif str(league) == "Conference":
        league = "EC"
    data = getYearlyData(year_one, last_year, league)

    return data


def getAllEnglishData(year_one, last_year):
    leagues = ["E0", "E1", "E2", "E3"]
    df_full = pd.DataFrame(
        columns={
            "game_id",
            "Date",
            "HomeTeam",
            "AwayTeam",
            "HomeGoals",
            "AwayGoals",
            "HalfTimeHomeGoals",
            "HalfTimeAwayGoals",
            "HomeShots",
            "AwayShots",
            "HomeShotsTarget",
            "AwayShotsTarget",
            "HomeFouls",
            "AwayFouls",
            "HomeYellow",
            "AwayYellow",
            "HomeRed",
            "AwayRed",
        }
    )
    for i in leagues:

        for j in range(year_one, last_year):
            df = pd.read_csv(
                f"http://www.football-data.co.uk/mmz4281/{j:02}{j+1:02}/{i}.csv"
            )
            df = df[
                [
                    "Date",
                    "HomeTeam",
                    "AwayTeam",
                    "FTHG",
                    "FTAG",
                    "HTHG",
                    "HTAG",
                    "HS",
                    "AS",
                    "HST",
                    "AST",
                    "HF",
                    "AF",
                    "HY",
                    "AY",
                    "HR",
                    "AR",
                ]
            ]
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
            data.reset_index(inplace=True)
            data = data.rename(columns={"index": "game_id"})
            data["league"] = i
            df_full = pd.concat([data, df_full])

    return df_full


def getTeams(data):
    team_list = pd.DataFrame(data["HomeTeam"].unique(), columns={"Teams"})
    team_list.reset_index(inplace=True)
    team_list = team_list.rename(columns={"index": "team_id"})
    return team_list


def getYearlyData(year_one, last_year, league):
    league = str(league)
    df_full = pd.DataFrame(
        columns={
            "game_id",
            "Date",
            "HomeTeam",
            "AwayTeam",
            "HomeGoals",
            "AwayGoals",
            "HalfTimeHomeGoals",
            "HalfTimeAwayGoals",
            "HomeShots",
            "AwayShots",
            "HomeShotsTarget",
            "AwayShotsTarget",
            "HomeFouls",
            "AwayFouls",
            "HomeYellow",
            "AwayYellow",
            "HomeRed",
            "AwayRed",
        }
    )
    for i in range(year_one, last_year):
        df = pd.read_csv(
            f"http://www.football-data.co.uk/mmz4281/{i:02}{i+1:02}/{league}.csv"
        )
        df = df[
            [
                "Date",
                "HomeTeam",
                "AwayTeam",
                "FTHG",
                "FTAG",
                "HTHG",
                "HTAG",
                "HS",
                "AS",
                "HST",
                "AST",
                "HF",
                "AF",
                "HY",
                "AY",
                "HR",
                "AR",
            ]
        ]
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
        data.reset_index(inplace=True)
        data = data.rename(columns={"index": "game_id"})
        print(data)
        # data.copy('index')
        df_full = pd.concat([data, df_full])

    return df_full




