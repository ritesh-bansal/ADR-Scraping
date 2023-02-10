import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime


def adrScraping():

    def isTimeFormat(timeFormat):
        try:
            time.strptime(timeFormat, '%H:%M:%S')
            return True
        except ValueError:
            return False

    try:
        name = []
        last = []
        chgPct = []
        vol = []
        dateTime = []
        date = []
        url = "https://in.investing.com/equities/india-adrs"
        headers = {"User-Agent": "*"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content.decode('UTF-8'), 'html.parser')
        table = soup.find('table', class_="common-table medium js-table js-streamable-table")

        rows = table.find_all('tr')

        for row in rows[1:]:
            name.append(str(row.find_all('td')[2].text.replace('\n', '').replace('ADR', '').replace(' ', '')).upper())
            last.append(str(row.find_all('td')[3].text.replace('\n', '')))
            # high.append(str(row.find_all('td')[4].text.replace('\n', '')))
            # low.append(str(row.find_all('td')[5].text.replace('\n', '')))
            # chg.append(str(row.find_all('td')[6].text.replace('\n', '')))
            chgPct.append(str(row.find_all('td')[7].text.replace('\n', '')))
            vol.append(str(row.find_all('td')[8].text.replace('\n', '')))
            dateTime.append(str(row.find_all('td')[9].text.replace('\n', '').replace(' ', '')))

        for t in dateTime:
            if isTimeFormat(t):
                date.append(datetime.today().strftime("%d-%b-%Y"))
            else:
                date.append(datetime.strptime(t + '/' + str(datetime.today().strftime("%y")), "%d/%m/%y").strftime("%d-%b-%Y"))

        adrs = []
        for i, j, n, o, p in zip(name, last, chgPct, vol, date):
            myDict = {'Symbol': i, 'Date': p, 'LTP ($)': j, 'Volume': o, 'Chg%': n}
            adrs.append(myDict)

        with open('ADR.csv', 'w', newline='') as f:
            keys = adrs[0].keys()
            csvWriter = csv.DictWriter(f, keys)
            csvWriter.writeheader()
            csvWriter.writerows(adrs)
            f.close()

    except Exception as e:
        # print(e)
        try:
            name = []
            symbol = []
            date = []
            ltp = []
            chgPct = []
            vol = []
            url = "https://www.financialexpress.com/market/stock-market/adr-prices/"
            headers = {"User-Agent": "*"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content.decode('UTF-8'), 'html.parser')
            table = soup.find('table', class_="table-databox footable")
            # print(soup)
            rows = table.find_all('tr')

            for row in rows[1:]:
                symbol.append(str(row.find_all('td')[0].text.replace('\n', '')))
                name.append(str(row.find_all('td')[1].text.replace('\n', '')))
                date.append(str(row.find_all('td')[2].text.replace('\n', '')))
                ltp.append(str(row.find_all('td')[3].text.replace('\n', '')))
                vol.append(str(row.find_all('td')[4].text.replace('\n', '')))
                chgPct.append(str(row.find_all('td')[5].text.replace('\n', '')))

            adrs = []
            for i, k, l, m, n in zip(symbol, date, ltp, vol, chgPct):
                myDict = {'Symbol': i, 'Date': k, 'LTP ($)': l, "Volume (000's)": m, 'Chg%': n}
                adrs.append(myDict)

            # print(indices)

            with open('ADR.csv', 'w', newline='') as f:
                keys = adrs[0].keys()
                csvWriter = csv.DictWriter(f, keys)
                csvWriter.writeheader()
                csvWriter.writerows(adrs)
                f.close()
        except Exception as e:
            raise e


adrScraping()