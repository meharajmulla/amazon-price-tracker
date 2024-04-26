import csv
import time

import requests
from bs4 import BeautifulSoup

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, close

from data import ItemData

import settings
from settings import CSV_ITEM_FILE, ITEM_NUM_FILE


class Tracker(ItemData):
    
    def __init__(self, URL):
        page = requests.get(URL, headers={"User-Agent": settings.user_agent})
        soup0 = BeautifulSoup(page.content, "html.parser")
        soup = BeautifulSoup(soup0.prettify(), "html.parser")
        print(soup)
        self.URL = URL
        self.soup = soup
        self.target_price = self.findTargetPrice()

    def title(self):
        productTitle = self.soup.find(id="productTitle").get_text()
        return productTitle

    def price(self): 
        try:
           productPrice = self.soup.find(class_="a-price-whole").get_text().replace(",","").replace(".","")
           return productPrice
        except AttributeError:
           print("Price element not found or HTML structure changed.")
           return None


    def int_price(self):
        try:
            
            return float(self.price())
        
        except TypeError:
            pass

    def compare_prices(self):
        try:
            if self.int_price() <= float(self.target_price):
                return 'below'
            elif self.int_price() >= float(self.target_price):
                return 'above'
        
        except Exception:
            return 'out-of-stock'

    def graph(self):
        csv_file, png_file = self.filesNames()

        try:
            with open(csv_file, "a") as f:
                f.write(f"{int(time.time() - 14400)}, {self.int_price()}, {self.target_price}\n")

            figure(num=None, figsize=(9, 6), dpi=120, facecolor='w', edgecolor='k')

            plt.clf()

            df = pd.read_csv(csv_file, names=['Time', 'Price', 'Target Price'])
            df['Date'] = pd.to_datetime(df['Time'],unit='s')
            df.drop("Time", 1,  inplace=True)
            df.set_index("Date", inplace=True)

            df['Price'].plot()
            df['Target Price'].plot()

            plt.legend()

            plt.savefig(png_file)  
            close()

        except Exception:
            pass

