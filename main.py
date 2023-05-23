import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

years = range(2023, 2022, -1)

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
base_url = "https://fbref.com"

if __name__ == "__main__":

    all_matches = []

    for year in years:

        print(f"Processing {year}")
        data = requests.get(standings_url)

        soup = BeautifulSoup(data.text, features="html.parser")

        standings_table = soup.select('table.stats_table')[0]
        links = standings_table.find_all('a')
        links = [lnk.get("href") for lnk in links]
        links = [lnk for lnk in links if '/squads' in lnk]

        team_urls = [f"{base_url}{lnk}" for lnk in links]

        for team_url in team_urls:
            team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
            print(f"Processing {team_name}")

            data = requests.get(team_url)

            matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            matches["team"] = team_name
            matches["season"] = year

            all_matches.append(matches)

            time.sleep(10)

        time.sleep(10)

    match_df = pd.concat(all_matches)
    match_df.to_csv("matches.csv")
