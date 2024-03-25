from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import os.path

CHROME_PATH = "C:/Users/john/drivers/chrome-win64"
CHROMEDRIVER_PATH = '"C:/Users/john/drivers/chromedriver-win64"'
WINDOW_SIZE = "1200,800"


class Analyzer:
    stonks = {}

    # Constructor for class: a = Analyzer()
    def __init__(self):
        # Init stonks
        self.stonks = {}

    # Loads list of stonk names from file with only stonk name on each line.
    def get_stonks(self, file):
        stocks = open(file, "r").readlines()
        for line in stocks:
            self.stonks[line[:-1]] = {}

    # Update the profiles
    def update_profiles(self, headless: bool = True, first: int = 0):
        # Update first to appropriate value
        if first <= 0 or first > len(self.stonks):
            first = len(self.stonks)

        # Set index for the file name
        index = 0
        while os.path.isfile("./results" + str(index) + ".csv"):
            index += 1

        # Initialize chrome options for headless (if set), and minimal logging
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.add_argument("--log-level=3")

        # Start the web driver
        driver = webdriver.Chrome(options=chrome_options)

        # Loop through all the stocks
        for i, stock in enumerate(list(self.stonks.keys())[0:first]):
            # Print status
            print(f"{i} out of {first}")

            # Try to send request
            try:
                # Get webpage
                driver.get(f"https://www.cnn.com/markets/stocks/{stock}")

                # Serialize webpage
                soup = bs(driver.page_source, "html.parser")

                # Get high, median, and low
                high = soup.find_all("g", class_="high-data")[0].find_all("tspan")[2]
                median = soup.find_all("g", class_="median-data")[0].find_all("tspan")[
                    2
                ]
                low = soup.find_all("g", class_="low-data")[0].find_all("tspan")[2]

                # Extract the text
                high_txt = high.text
                median_txt = median.text
                low_txt = low.text

                # Add negative if number is red
                if high.attrs["fill"] == "#D50000":
                    high_txt = "-" + high_txt
                if median.attrs["fill"] == "#D50000":
                    median_txt = "-" + median_txt
                if low.attrs["fill"] == "#D50000":
                    low_txt = "-" + low_txt

                self.stonks[stock]["high"] = high_txt
                self.stonks[stock]["median"] = median_txt
                self.stonks[stock]["low"] = low_txt

                # Write results to csv
                with open(f"./results{index}.csv", "a") as file:
                    file.write(
                        stock
                        + ", "
                        + high_txt
                        + ", "
                        + median_txt
                        + ", "
                        + low_txt
                        + "\n"
                    )
            # Except error
            except Exception:
                # Write failed result
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
        # Print line
        print()
        # Close driver
        driver.close()

    # WIP Will write to file
    def save_to_file(self):
        pass
