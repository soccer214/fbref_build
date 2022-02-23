from football_data_scrape import getAllEnglishData
from football_data_scrape import getTeams

if __name__ == "__main__":
    print('well done')

data = getAllEnglishData(5,8)

teams = getTeams(data)
print(teams)

