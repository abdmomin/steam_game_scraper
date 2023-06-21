import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


headers = {
    "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Referer": "https://store.steampowered.com/search/?filter=globaltopsellers",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "X-Prototype-Version": "1.7",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


def get_data(url):
    response = requests.get(url, headers=headers)
    data = response.json()
    return data["results_html"]


def total_results(url):
    response = requests.get(url, headers=headers)
    data = response.json()
    return int(data["total_count"])


def parse_data(data):
    games_list = []
    soup = BeautifulSoup(data, "html.parser")
    games = soup.select("a")
    for game in games:
        title = game.select_one("span.title").text.strip()
        try:
            price = game.select_one("div.search_price").text.strip().split("$")[1]
        except IndexError:
            price = game.select_one("div.search_price").text.strip().split("$")[0]
        try:
            discount = game.select_one("div.search_price").text.strip().split("$")[2]
        except IndexError:
            discount = 0

        game_dict = dict(title=title, price=price, discount=discount)
        games_list.append(game_dict)
    return games_list


def output_data(results):
    df = pd.DataFrame(results)
    print(df.head(10))
    print(df.shape)
    df.to_csv("steam_games_data.csv", index=False)
    print("Saved to CSV file")


if __name__ == "__main__":
    url = "https://store.steampowered.com/search/results/?query&start=200&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_globaltopsellers_7&filter=globaltopsellers&supportedlang=english&infinite=1"
    results = []
    for x in range(0, total_results(url), 50):
        print(f"Scraping page {x}")
        data = get_data(
            f"https://store.steampowered.com/search/results/?query&start={x}&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_globaltopsellers_7&filter=globaltopsellers&supportedlang=english&infinite=1"
        )
        games = parse_data(data)
        results += games
        time.sleep(1.5)
    # print(total_results(url))
    output_data(results)
