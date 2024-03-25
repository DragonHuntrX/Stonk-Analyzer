from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import os.path

CHROME_PATH = "C:/Users/john/drivers/chrome-win64"
CHROMEDRIVER_PATH = '"C:/Users/john/drivers/chromedriver-win64"'
WINDOW_SIZE = "1200,800"


class Analyzer:
    stonks = {}

    def __init__(self):
        """
        docstring
        """
        self.stonks = {}

    def get_stonks(self, file):
        stocks = open(file, "r").readlines()
        for line in stocks:
            self.stonks[line[:-1]] = {}

    def update_profiles(self, headless: bool = True, first: int = 0):
        if first <= 0 or first > len(self.stonks):
            first = len(self.stonks)

        print(first)

        index = 0
        while os.path.isfile("./results" + str(index) + ".csv"):
            index += 1

        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=chrome_options)

        for i, stock in enumerate(list(self.stonks.keys())[0:first]):
            print(f"{i} out of {len(self.stonks)}")
            try:
                driver.get(f"https://www.cnn.com/markets/stocks/{stock}")

                soup = bs(driver.page_source, "html.parser")

                high = soup.find_all("g", class_="high-data")[0].find_all("tspan")[2]
                median = soup.find_all("g", class_="median-data")[0].find_all("tspan")[
                    2
                ]
                low = soup.find_all("g", class_="low-data")[0].find_all("tspan")[2]

                high_txt = high.text
                median_txt = median.text
                low_txt = low.text

                if high.attrs["fill"] == "#D50000":
                    high_txt = "-" + high_txt
                if median.attrs["fill"] == "#D50000":
                    median_txt = "-" + median_txt
                if low.attrs["fill"] == "#D50000":
                    low_txt = "-" + low_txt

                with open(f"./results{index}.csv", "a") as file:
                    file.write(
                        stock
                        + ", "
                        + high_txt
                        + ", "
                        + median_txt
                        + ", "
                        + low_txt
                        + ",\n"
                    )
            except Exception:
                with open("./results" + str(index) + ".csv", "a") as file:
                    file.write(
                        stock
                        + ", "
                        + "Failed"
                        + ", "
                        + "Failed"
                        + ", "
                        + "Failed"
                        + ",\n"
                    )
        print()
        driver.close()
