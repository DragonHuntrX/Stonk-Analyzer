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

    def update_profiles(self, headless: bool = True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

        driver = webdriver.Chrome(options=chrome_options)
        index = 0
        while os.path.isfile("./results" + str(index) + ".csv"):
            index += 1

        for stock in self.stonks.keys():
            try:
                driver.get("https://www.cnn.com/markets/stocks/" + stock)

                soup = bs(driver.page_source, "html.parser")
                with open("./results" + str(index) + ".csv", "a") as file:
                    file.write(
                        stock
                        + ", "
                        + soup.find_all("g", class_="high-data")[0]
                        .find_all("tspan")[2]
                        .text
                        + ", "
                        + soup.find_all("g", class_="median-data")[0]
                        .find_all("tspan")[2]
                        .text
                        + ", "
                        + soup.find_all("g", class_="low-data")[0]
                        .find_all("tspan")[2]
                        .text
                        + ",\n"
                    )
            except Exception:
                pass

        driver.close()
