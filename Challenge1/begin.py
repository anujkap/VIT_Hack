#importing Libs
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
df = pd.read_csv('Challenge1.csv', header=None, nrows=50)
url = df.iloc[:, 1]

new = 1
WBStocks = []
for i in range(0, 50):
    DER = None
    ROE = None
    intCover = None
    base_page = url[i]
    page_main = requests.get(base_page)
    soup_main = BeautifulSoup(page_main.content, "html5lib")
    name_box = soup_main.find("h1", class_="b_42 PT20").string

    yearly = soup_main.find("a", text="Yearly Results")
    ratios = soup_main.find("a", text="Ratios")

    page_yearly = requests.get(urljoin(base_page, yearly.get("href")))
    soup_yearly = BeautifulSoup(page_yearly.content, "html5lib")
    table_yearly = soup_yearly.findAll("table", class_="table4")[2]
    netSales = table_yearly.findAll("td", class_="det")[1].string
    # print("Net Sales=", netSales)
    netSales = netSales.replace(",", "")
    if float(netSales) < 250:
        continue

    page_ratios = requests.get(urljoin(base_page, ratios.get("href")))
    soup_ratios = BeautifulSoup(page_ratios.content, "html5lib")
    table_ratios = soup_ratios.findAll("table", class_="table4")[2]
    earning = table_ratios.find("td", text="Basic EPS (Rs.)").find_next("td", class_="det").string
    DERloc = table_ratios.find("td", text="Total Debt/Equity (X)")

    old_format = soup_ratios.findAll("span", class_="UC")[1]
    link = old_format.parent.get("href")
    page_oratios = requests.get(urljoin(base_page, link))
    soup_oratios = BeautifulSoup(page_oratios.content, "html5lib")
    table_oratios = soup_oratios.findAll("table", class_="table4")[2]

    if (DERloc is None) or DERloc.find_next("td", class_="det").string == "--":
        DERloc = table_oratios.find("td", text="Debt Equity Ratio")
        new = 0
    if not((DERloc is None) or DERloc.find_next("td", class_="det").string == "--"):
        DER = DERloc.find_next("td", class_="det").string
        # print("Debt to Equity=", DER)
        if float(DER) > .3:
            continue

    if new == 1:
        ROEloc = table_ratios.find("td", text="Return on Networth / Equity (%)")
        if ROEloc is None:
            ROEloc = table_oratios.find("td", text="Return On Net Worth(%)")
            new = 0
    else:
        ROEloc = table_oratios.find("td", text="Return On Net Worth(%)")
        if ROEloc is None:
            ROEloc = table_ratios.find("td", text="Return on Networth / Equity (%)")
            new = 1
    if ROEloc is not None:
        ROE = ROEloc.find_next("td", class_="det").string
        # print("Return on Equity=", ROE)
        if float(ROE) < 15:
            continue

    intCoverloc = table_oratios.find("td", text="Interest Cover")
    if not(intCoverloc is None or intCoverloc.find_next("td", class_="det").string == "--"):
        intCover = intCoverloc.find_next("td", class_="det").string
        intCover = intCover.replace(",", "")
        # print("Interest Coverage=", intCover)
        if float(intCover) < 4:
            continue

    price = soup_ratios.find("span", id="Bse_Prc_tick").find_next("strong").string
    price = float(price.replace(",", ""))
    earning = float(earning.replace(",", ""))
    PER = price/earning
    if PER > 25:
        continue

    WBStocks.append([name_box, netSales, DER, ROE, intCover, PER])
    print(name_box)
df = pd.DataFrame(WBStocks, columns=['Name', 'NetSales', 'Debt/Equity', 'Return on Equity', 'Interest Coverage', 'Price/Earnings'])
print(df)
df.to_csv(r"D:/VITHack/WarrenBuffet.csv")
