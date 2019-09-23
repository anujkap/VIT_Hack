from textblob import TextBlob
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import datetime
from datetime import date
df = pd.read_csv("Challenge2.csv", header=None, nrows=50)
url = df.iloc[:, 1]
name = df.iloc[:, 0]
today = date.today()
polarity = []
for i in range(0, 50):
    base = url[i]
    page = requests.get(base)
    soup = BeautifulSoup(page.content, "html5lib")
    entry = soup.findAll("a", class_="g_14bl")
    dateAll = soup.findAll("p", class_="PT3 a_10dgry")

    pol = 0
    k = 0
    for j in entry:
        news = j.find_next("strong").string
        date = dateAll[k].getText()
        date = re.split('\|', date)[1]
        try:
            datediff = datetime.datetime.strptime(date, ' %d %b %Y ').date() - today
        except ValueError:
            datediff = datetime.datetime.strptime(date, ' %d %b %Y').date() - today
        blob = TextBlob(news)
        if abs(datediff.days) < 30:
            pol += blob.sentiment.polarity*1
        elif abs(datediff.days) > 30:
            pol += blob.sentiment.polarity * 0.8
        elif abs(datediff.days) > 60:
            pol += blob.sentiment.polarity * 0.7
        elif abs(datediff.days) > 90:
            pol += blob.sentiment.polarity * 0.5
        elif abs(datediff.days) > 120:
            pol += blob.sentiment.polarity * 0.3
        elif abs(datediff.days) > 150:
            pol += blob.sentiment.polarity * 0.1
        else:
            pol += blob.sentiment.polarity * 0

        k += 1
    polarity.append([name[i], pol])
df = pd.DataFrame(polarity, columns=['Name', 'Sentiment'])
df.to_csv(r"D:/VITHack/Sentimental.csv")