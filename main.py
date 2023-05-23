import requests
from bs4 import BeautifulSoup
import pandas as pd

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

if __name__ == "__main__":
    data = requests.get(standings_url)

    soup = BeautifulSoup(data.text, features="html.parser")

    standings_table = soup.select('table.stats_table')[0]
    links = standings_table.find_all('a')
    links = [lnk.get("href") for lnk in links]
    links = [lnk for lnk in links if '/squads' in lnk]

    team_urls = [f"https://fbref.com{lnk}" for lnk in links]

    team_url = team_urls[6]
    data = requests.get(team_url)

    matches = pd.read_html(data.text, match="Scores & Fixtures")
    print(matches)