from bs4 import BeautifulSoup
import requests
import urllib
import math
import csv
import time
import os
import json
from datetime import datetime
import smtplib

senderEmail = ''
senderPassword = ''
today = datetime.now()
year = today.year
month = today.month
day = today.day
defaced = []
cookies = {
    'ZHE': 'ea8495ffc2af171c6f9ee683323f334c',
    'PHPSESSID': 'ul1l047q31ccn7edasmak9p497'
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.zone-h.org/archive/special=1',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
}


def getEmail(domain):
    url = "https://api.hunter.io/v2/domain-search?domain=" + \
        domain+"&api_key=a435c665ca5965b46151a3b40b5e6729efd450e1"
    response = requests.request("GET", url).text
    for element in json.loads(response)['data']["emails"]:
        return element["value"]


def getDomain(url):
    return


def byPassTestCookies():
    return


def bypassCaptcha():
    return


def send_mail(senderEmail, senderPassword, receiverEmail, messsage):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(senderEmail, receiverEmail, messsage.encode("utf8"))
    server.quit()


def crawlEachPage(pageNumber):
    urlPage = url+'/page='+pageNumber
    response = requests.get(urlPage, headers=headers,
                            cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser")
    rowAll = soup.find_all('tr')
    for row in range(1, len(rowAll)-2):
        tdAll = rowAll[row].find_all('td')
        try:
            location = tdAll[5].find('img').get('title')
        except:
            localtion = ""
        try:
            i = tdAll[6].find('img').get('src')
            i = "yes"
        except:
            i = ""
        try:
            view = originUrl+tdAll[9].find('a').get('href')
        except:
            view = ""
        if location == "Viet Nam":
            r = tdAll[0].text, tdAll[1].text, tdAll[2].text, tdAll[3].text, tdAll[4].text, location, i, tdAll[7].text.strip(
            ), tdAll[8].text, view
            if r not in defaced:
                # Write to csv file
                with open('output/zoneH-{}-{}-{}-{}.csv'.format(year, month, day, 'output'), 'a') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([tdAll[0].text, tdAll[1].text, tdAll[2].text, tdAll[3].text,
                                     tdAll[4].text, location, i, tdAll[7].text.strip(), tdAll[8].text, view])
                # Send mail to alert here
                    receiverEmail = getEmail(getDomain(tdAll[7].text.strip()))
                    message = ''
                    send_mail(senderEmail, senderPassword,
                              receiverEmail, message)


def crawlPageInRange(startPage, endPage):
    for page in range(startPage, endPage+1):
        crawlEachPage(str(page))


if __name__ == "__main__":
    originUrl = 'http://www.zone-h.org'
    url = 'http://www.zone-h.org/archive'
    response = requests.get(url, headers=headers,
                            cookies=cookies, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    total = soup.find('b')
    totalPage = int(total.text.replace(",", ""))
    numOfPage = math.ceil(totalPage/25)
    if os.path.exists(('output/zoneH-{}-{}-{}-{}.csv'.format(year, month, day, 'output'))) == False:
        with open('output/zoneH-{}-{}-{}-{}.csv'.format(year, month, day, 'output'), 'w+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Date', 'Notifier', 'H', 'M', 'R',
                             'L', 'Special defacement', 'Domain', 'OS', 'View'])
    else:
        with open('output/zoneH-{}-{}-{}-{}.csv'.format(year, month, day, 'output'), 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                if row:
                    time = '0'*(-len(row[0])) + row[0],
                    r = time, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
                    defaced.append(r)
    crawlPageInRange(1, numOfPage+1)
