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

        previous_season = soup.select("a.prev")[0].get("href")
        standings_url = f"{base_url}{previous_season}"

        team_urls = [f"{base_url}{lnk}" for lnk in links]

        for team_url in team_urls:
            team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
            print(f"Processing {team_name}")

            data = requests.get(team_url)

            matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
            matches["Team"] = team_name
            matches["Year"] = year
            matches["Season"] = f"{str(year - 1)}/{str(year)[-2:]}"
            matches.drop(columns=['Formation', 'Captain', 'Notes', 'Match Report'], inplace=True)

            soup = BeautifulSoup(data.text, features="html.parser")
            links = [lnk.get("href") for lnk in soup.find_all('a')]
            links = [lnk for lnk in links if lnk and 'all_comps/shooting' in lnk]
            data = requests.get(f"{base_url}{links[0]}")
            shooting = pd.read_html(data.text, match="Shooting")[0]
            shooting.columns = shooting.columns.droplevel()

            team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")

            all_matches.append(team_data)

            time.sleep(10)

        time.sleep(10)

    match_df = pd.concat(all_matches)
    match_df.to_csv("matches.csv")
