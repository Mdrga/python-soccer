# -*- coding: utf-8 -*-
'''
Created on Aug 16, 2015
Modified on Aug 29, 2015
Version 0.03.c
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
'''
# Import Libraries needed for Scraping the various web pages
import bs4 
import datetime
import time
import requests
import webbrowser
import os
import openpyxl
import sys

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print ('Downloading %s...' % (localFileName))
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

hr = " >>> *** ====================================================== *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'Premier League Match & Stats Parser v0.01.a'
print (ds + ' :: ' + ts + ' :: ' + parseVersion)
print ('Python Version :: ' + sys.version)
print (hr)

# Define URLs for the Barclay's Premier League
espnURL = 'http://www.espnfc.us/barclays-premier-league/23/index'
espnFixtures = 'http://www.espnfc.us/barclays-premier-league/23/scores'
injuriesURL = 'http://www.fantasyfootballscout.co.uk/fantasy-football-injuries/'
teamNewsURL = 'http://www.fantasyfootballscout.co.uk/team-news/'
bbcURL = 'http://www.bbc.com/sport/0/football/premier-league/'
bbcFixturesURL = 'http://www.bbc.com/sport/football/premier-league/fixtures'

# Base Path for Output
localPath = 'D:\\ESPN-Parser\\'
baseWkBk = 'template.xlsx'
workBook = openpyxl.load_workbook(os.path.join(localPath + baseWkBk))
teamSheet = workBook.get_sheet_by_name('teams')
playerSheet = workBook.get_sheet_by_name('players')
matchSheet = workBook.get_sheet_by_name('matches')

# Create BS4 Object from ESPN Web Page
espnRes = requests.get(espnURL)
espnRes.raise_for_status()
espnSoup = bs4.BeautifulSoup(espnRes.text, "html.parser")
with open(os.path.join(localPath +'espnLanding.txt'), 'wb') as fo:
	for chunk in espnRes.iter_content(100000):
		fo.write(chunk)

espnFixRes = requests.get(espnFixtures)
espnFixRes.raise_for_status()
fixturesSoup = bs4.BeautifulSoup(espnFixRes.text, "html.parser")
with open(os.path.join(localPath + 'fixturesLanding.txt'), 'wb') as fo:
	for chunk in espnFixRes.iter_content(100000):
		fo.write(chunk)

teamListContainer = fixturesSoup.find("div", id="submenu-content")
teamList = teamListContainer.find_all("ul")
teamList = teamList[1].find_all("li")

teamCounter = 2

# Parse ESPN Team List
for i in teamList:
	teamName = i.get_text()
	teamURL = i.a['href']
	teamSheet.cell('A' + str(teamCounter)).value = teamName
	teamSheet.cell('B' + str(teamCounter)).value = teamURL
	print (teamName)
	teamCounter += 1

workBook.save(os.path.join(localPath + ds + '.xlsx'))
print (hr)

# Parse BBC Results and Fixtures
bbcFixtures = requests.get(bbcFixturesURL)
bbcFixtures.raise_for_status()

bbcFixtureSoup = bs4.BeautifulSoup(bbcFixtures.text, "html.parser")
with open(os.path.join(localPath + 'bbcLanding.html'), 'wb') as fo:
	for chunk in bbcFixtures.iter_content(100000):
		fo.write(chunk)
		print ('Writing file...')

print (hr)

fixtureContainer = bbcFixtureSoup.find('div', class_="fixtures-table full-table-medium")
fixtureRow = fixtureContainer.find_all('table', class_="table-stats")

for i in fixtureContainer:
	rowData = i
	if len(rowData) == 1:
		fixtureDate = str((rowData.string).strip())
		if len(fixtureDate) > 1:
			print (fixtureDate + '| ' + str(len(fixtureDate)))


	if len(rowData) > 1:
		# print (rowData)
		tableRow = rowData.find_all('tr')
		previewData = i.find_all('tr', class_="preview")
		for i in previewData:
			# print (i)
			print ('***========***')
	print (shr)

print (hr)