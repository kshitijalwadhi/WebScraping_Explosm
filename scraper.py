import requests
from bs4 import BeautifulSoup
import os
import urllib.request
import pandas as pd
import re
from datetime import date

#############################
# month name to number
#############################
def monthNum(month):
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    return months.index(month) + 1
#############################


#############################
# month num to name
#############################
def monthName(number):
    if number == 1:
        return "january"
    elif number == 2:
        return "february"
    elif number == 3:
        return "march"
    elif number == 4:
        return "april"
    elif number == 5:
        return "may"
    elif number == 6:
        return "june"
    elif number == 7:
        return "july"
    elif number == 8:
        return "august"
    elif number == 9:
        return "september"
    elif number == 10:
        return "october"
    elif number == 11:
        return "november"
    elif number == 12:
        return "december"
#############################


#############################
# reading input.txt file
#############################
f = open("input.txt", "r")
lines = f.readlines()
startMonth, startYear = (lines[0].split())
endMonth, endYear = (lines[1].split())
authorinput = lines[2].split()
f.close()
s1 = monthNum(startMonth)
e1 = monthNum(endMonth)
#############################


#############################
# make folder
#############################
def makeFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
#############################


#############################
# making the directories
#############################
if startYear == endYear:
    for i in range(s1, e1+1):
        namei = monthName(i)
        path = './'+startYear+'/' + namei
        makeFolder(path)
else:
    for j in range(s1, 13):
        namej = monthName(j)
        path = './'+startYear+'/' + namej
        makeFolder(path)
    for j in range(1, e1+1):
        namej = monthName(j)
        path = './'+endYear+'/' + namej
        makeFolder(path)
    for i in range(int(startYear)+1, int(endYear)):
        for j in range(1, 13):
            namej = monthName(j)
            path = './'+str(i)+'/' + namej
            makeFolder(path)
#############################


#############################
# img dl def
#############################
def dlimg(url, path, filename):
    fullPath = path+filename+'.png'
    urllib.request.urlretrieve(url, fullPath)
#############################


#############################
# img link return def
#############################
def imglink(url):
    comicpage = requests.get(url)
    soup = BeautifulSoup(comicpage.content)
    imgfile = soup.find('div', attrs={'id': 'comic-wrap'})
    newURL = 'http:' + imgfile.img['src']
    return newURL
#############################


#############################
# download comics of a particular month
#############################
def dlmonthcom(url, month, year):
    result = requests.get(url)
    soup2 = BeautifulSoup(result.content)
    rows1 = soup2.find_all(class_='small-3 medium-3 large-3 columns')
    rows3 = [imglink('http://www.explosm.net' + item.a['href'])
             for item in rows1]  # links of image
    rows2 = soup2.find_all('div', attrs={'id': 'comic-author'})
    rows4 = [item.get_text() for item in rows2]
    rows5 = [(re.split(' |/n', item))[1] for item in rows4]  # author
    rows6 = [(re.split(' |/n', item))[0][1:11] for item in rows4]  # date

    comicinfo = pd.DataFrame(
        {
            'rows3': rows3,
            'rows5': rows5,
            'rows6': rows6,
        })

    count_row = comicinfo.shape[0]
    path = './' + year + '/'+month+'/'
    k = 0

    for k in range(0, count_row):
        if rows5[k] in authorinput:
            name = str(rows6[k])+'-'+rows5[k]
            dlimg(rows3[k], path, name)
#############################


#############################
# The execution part
#############################
if startYear == endYear:
    for i in range(s1, e1+1):
        url = 'http://explosm.net/comics/archive/' + startYear+'/' + str(i)
        dlmonthcom(url, monthName(i), startYear)
else:
    for j in range(s1, 13):
        url = 'http://explosm.net/comics/archive/' + startYear+'/' + str(j)
        dlmonthcom(url, monthName(j), startYear)

    for j in range(1, e1+1):
        url = 'http://explosm.net/comics/archive/' + endYear+'/' + str(j)
        dlmonthcom(url, monthName(j), endYear)

    for i in range(int(startYear)+1, int(endYear)):
        for j in range(1, 13):
            url = 'http://explosm.net/comics/archive/' + str(i)+'/' + str(j)
            dlmonthcom(url, monthName(j), i)
#############################


#############################
#Bonus, get latest N comics
#############################
def latest(n):    
    if not os.path.exists('./latest'):
        os.makedirs('./latest')
    today = date.today()
    currentMonth = int(today.strftime("%m"))
    currentYear = today.strftime("%Y")

    while n>0:
        result = requests.get('http://explosm.net/comics/archive/'+currentYear+'/'+str(currentMonth))
        soup3 = BeautifulSoup(result.content)
        row1 = soup3.find_all(class_='small-3 medium-3 large-3 columns')
        row3 = [imglink('http://www.explosm.net' + item.a['href'])
             for item in row1]  # links of image
        row2 = soup3.find_all('div', attrs={'id': 'comic-author'})
        row4 = [item.get_text() for item in row2]
        row5 = [(re.split(' |/n', item))[1] for item in row4]  # author
        row6 = [(re.split(' |/n', item))[0][1:11] for item in row4]  # date

        comicinfon = pd.DataFrame(
            {
                'row3': row3,
                'row5': row5,
                'row6': row6,
            })

        count_rown = comicinfon.shape[0]
        path = './latest/' 
        k = 0

        for k in range(0, count_rown):
            name = str(row6[k])+'-'+row5[k]
            dlimg(row3[k], path, name)
            n-=1
            if(n==0):
                break
        
        if n!=0:
            currentMonth-=1
            if currentMonth==0:
                currentMonth=12
                currentYear-=1
#############################

latest(45)
