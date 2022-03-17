from scipy.stats import poisson


def runSimulation(data, goal_dict, weight_dict, schedule, league_table):
    print(data)
    for i, row in schedule.iterrows():
        home, away = row.home, row.away
        assert home in league_table.Team.values and away in league_table.Team.values
        home_score, away_score = simulateMatchScore(
            home, away, data, goal_dict, weight_dict
        )
        if home_score > away_score:
            league_table.loc[league_table.Team == home, "Points"] += 3
        elif home_score == away_score:
            league_table.loc[league_table.Team == home, "Points"] += 1
            league_table.loc[league_table.Team == away, "Points"] += 1
        elif away_score > home_score:
            league_table.loc[league_table.Team == away, "Points"] += 3

    return league_table


def simulateMatchScore(home, away, data, goal_dict, weight_dict):
    if home in data.Team and away in data.Team:
        home_rating = (
            data.at[home, "HomeAttackStrength"]
            * data.at[away, "AwayDefenseStrength"]
            * goal_dict["total_home_scored"]
        )
        away_rating = (
            data.at[away, "AwayAttackStrength"]
            * data.at[home, "HomeDefenseStrength"]
            * goal_dict["total_away_scored"]
        )
        probH, probA, probT = 0, 0, 0
        for i in range(0, 11):
            for j in range(0, 11):
                mod = poisson.pmf(i, home_rating) * poisson.pmf(y, away_rating)
                if x == y:
                    probT += mod
                if i > j:
                    probH += mod
                if j > i:
                    probA += mod
        s_home = 3 * probH + probT
        s_away = 3 * probA + probT
        print(home, s_home, away, s_away)

    return (home, away)
