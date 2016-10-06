# -*- coding: utf-8 -*-
'''
Created on Jul 04, 2016
Modified on Aug 05, 2016
Version 0.01.b
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2016-07Jul-04    RWN        Initial Creation of the file to parse out league information and 
                                teams from the BBC site. 
    2016-08Aug-05    RWM        Updating to cycle through the various leagues and create them in the
                                soccer database
'''

# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import collections
import pprint
import datetime
import requests
import openpyxl
import os
import platform
import sys
import mysql.connector

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%H:%M:%S:%f")[:-3]
    return update

# Establish MySQL Connection
cnx = mysql.connector.connect(user='root', password='password',
								 host='127.0.0.1',
								 database='leagues ',
								 use_pure=False)

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print ('Downloading %s...' % (localFileName))
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

# Program Version & System Variables
parse = '0.01.a'
parseVersion = 'BBC Football League Parser ' + parse
print (ds + ' :: ' + ts + ' :: ' + parseVersion)
print ('Python Version :: ' + sys.version)

# Screen Output Dividers used for readability
hr = " >>> *** ====================================================== *** <<<"
shr = " >>> *** ==================== *** <<<"

# Establish Base URL and parse for menu links
baseURL = "http://www.bbc.com/sport/football"
leagueURL = "http://www.bbc.com/sport/football/leagues-competitions"
base = "http://www.bbc.com"

print (hr)
getLeagues = requests.get(leagueURL)
getLeagues.raise_for_status()
leagueSoup = BeautifulSoup(getLeagues.text, "html.parser")
leagueList = leagueSoup.find("div", {"class": "stats leagues-competitions"})
listOfLeagues = leagueList.find_all("ul")

leagueDct = {'name' : [], 
             'url' : []}

for i in listOfLeagues:
    # print (i)
    lists = i
    listElements = lists.find_all("li")
    for i in listElements:
        # print (i)
        leagueName = i.get_text(strip=True)
        leagueURL = i.find("a")
        leagueURL = leagueURL['href']
        # print (leagueName, '::',leagueURL)
        leagueDct['name'].append(leagueName)
        leagueDct['url'].append(leagueURL)
        # print (shr)
    # print (hr)

# pprint.pprint(leagueDct)

# Function to receive a Text Date (i.e., Saturday 16th August 2014) and return 2014-08-16
def textDate(x):
    stringDate = x
    dayOfWeek = stringDate[0:3]
    length = len(stringDate)
    output = ''
    dateSpace = stringDate.find(" ")
    # print dateSpace
    year = stringDate[length-4:length]
    monthDay = stringDate[dateSpace+1:length-4]
    monthSpace = monthDay.find(" ")
    # print monthSpace
    day = monthDay[0:monthSpace-2]
    if int(day) < 10:
        day = '0' + str(day)
    month = monthDay[monthSpace+1:len(monthDay)-1]
    month = returnMonth(month)
    output = year + '' + month + '' + day
    return output

# Function to return a two digit month for a literal Month (i.e., change "August" to "08").
def returnMonth(x):
    inputMonth = x
    inputMonth = inputMonth[0:3]
    outputMonth = ''
    # print inputMonth
    if inputMonth == 'Aug':
        outputMonth = '08'
    elif inputMonth == 'Sep':
        outputMonth = '09'
    elif inputMonth == 'Oct':
        outputMonth = '10'
    elif inputMonth == 'Nov':
        outputMonth = '11'
    elif inputMonth == 'Dec':
        outputMonth = '12'
    elif inputMonth == 'Jan':
        outputMonth = '01'
    elif inputMonth == 'Feb':
        outputMonth = '02'
    elif inputMonth == 'Mar':
        outputMonth = '03'
    elif inputMonth == 'Apr':
        outputMonth = '04'
    elif inputMonth == 'May':
        outputMonth = '05'
    elif inputMonth == 'Jun':
        outputMonth = '06'
    elif inputMonth == 'Jul':
        outputMonth = '07'
    else:
        print ('EXCEPTION: Invalid Month sent to Function.')
        outputMonth = '99'
    return outputMonth

# Parse out Fixtures 
def parseFixtures(leagueLink):
    leagueParse = base + leagueLink + '/fixtures'
    if ((leagueParse != 'http://www.bbc.com/sport/football/world-cup/2014/fixtures') or (leagueParse != 'http://www.bbc.com/sport/football/european-championship/2012/fixtures') or (leagueParse != 'http://www.bbc.com/sport/football/africa-cup-of-nations/fixtures')):
        # Parse out URLs for each leagues' fixtures
        getLeagueParse = requests.get(leagueParse)
        getLeagueParse.raise_for_status()
        parseSoup = BeautifulSoup(getLeagueParse.text, "html.parser")
        parseContent = parseSoup.find("div", {"id": "blq-content"})
        parseBody = parseContent.find("div", {"class": "stats-body"})
        blockContent = parseBody.find("div", {"class": "fixtures-table full-table-medium"})
        tableDates = blockContent.find_all ("h2")

        # Print Output for Testing
        print (blockContent)
        print (shr)
        print (leagueParse)
        print (shr)
    else:
        print (leagueParse)
    print (hr)

# Create 
maxLen = 22
count = 0

while count < maxLen:
    parseFixtures(leagueDct['url'][count])
    count += 1
