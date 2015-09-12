# -*- coding: utf-8 -*-
'''
Created on Aug 16, 2015
Modified on Sep 12, 2015
Version 0.03.d
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
'''
# Import Libraries needed for Scraping the various web pages
import bs4 
import re
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
bbcResultsURL = 'http://www.bbc.com/sport/football/premier-league/results'

# Base Path for Output
localPath = 'D:\\ESPN-Parser\\'
localimgPath = 'D:\\ESPN-Parser\\img\\'
baseWkBk = 'template.xlsx'
workBook = openpyxl.load_workbook(os.path.join(localPath + baseWkBk))
teamSheet = workBook.get_sheet_by_name('teams')
playerSheet = workBook.get_sheet_by_name('players')
matchSheet = workBook.get_sheet_by_name('matches')
fixtureSheet = workBook.get_sheet_by_name('fixtures')

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
	# print (teamName)
	teamCounter += 1

workBook.save(os.path.join(localPath + ds + '.xlsx'))
print ('Teams Saved...')
print (hr)

# Parse BBC Fixtures and Results
bbcFixtures = requests.get(bbcFixturesURL)
bbcFixtures.raise_for_status()

bbcResults = requests.get(bbcResultsURL)
bbcResults.raise_for_status()

bbcFixtureSoup = bs4.BeautifulSoup(bbcFixtures.text, "html.parser")
with open(os.path.join(localPath + 'bbcFixtures.html'), 'wb') as fo:
	for chunk in bbcFixtures.iter_content(100000):
		fo.write(chunk)
		print ('Writing fixtures file...')

print (shr)

bbcResultsSoup = bs4.BeautifulSoup(bbcResults.text, "html.parser")
with open (os.path.join(localPath + 'bbcResults.html'), 'wb') as fo:
	for chunk in bbcResults.iter_content(100000):
		fo.write(chunk)
		print ('Writing results file...')

print (hr)

fixtureContainer = bbcFixtureSoup.find('div', class_="fixtures-table full-table-medium")
fixtureRow = fixtureContainer.find_all('table', class_="table-stats")

resultsContainer = bbcResultsSoup.find('div', class_="fixtures-table full-table-medium")
resultRow = resultsContainer.find_all('table', class_="table-stats")

# Function to process container. Pass two variables. 
# X = Container
# Y = Container Type 1 = Fixtures; 2 = Results
def processContainer(x, y):
	container = x
	processType = y
	count = 2

	if processType == 1:
		print ('Output for Fixtures Started...')
		print (shr)
	if processType == 2:
		print ('Output for Results Started...')
		print (shr)

	for i in container:
		rowData = i
		if len(rowData) == 1:
			fixtureDate = str((rowData.string).strip())
			if len(fixtureDate) > 1:
				dateYear = fixtureDate[-4:]
				dayOfWeek = fixtureDate[0:3]
				dayOfMonth = re.findall(r'\d{1,2}', fixtureDate)
				dayOfMonth = dayOfMonth[0]
				month = re.findall(r'[A-Z][a-z]*', fixtureDate)
				month = month[1]
				printFixtureDate = str(dateYear) + ' ' + month[0:3] + ' ' + str(dayOfMonth) + ' ' + dayOfWeek
				#print (printFixtureDate)
				#print (shr)
		if processType == 1:
			if len(rowData) > 1:
				tableRow = rowData.find_all('tr')
				previewData = i.find_all('tr', class_="preview")
				for i in previewData:
					# Identify the information about the Home Team
					homeTeam = i.find('span', class_="team-home teams")
					homeTeamURL = homeTeam.a['href']
					homeTeamName = homeTeam.a.get_text()
				
					# Identify the information about the Away Team
					awayTeam = i.find('span', class_="team-away teams")
					awayTeamURL = awayTeam.a['href']
					awayTeamName = awayTeam.a.get_text()
			
					# Identify Kickoff Time and Status
					kickoff = i.find('td', class_="kickoff")
					kickoff = kickoff.get_text().strip()
					status = i.find('td', class_="status")
					status = status.get_text().strip()
					
					# Output to Excel File
					fixtureSheet.cell('A' + str(count)).value = homeTeamName
					fixtureSheet.cell('B' + str(count)).value = awayTeamName
					fixtureSheet.cell('C' + str(count)).value = printFixtureDate
					fixtureSheet.cell('D' + str(count)).value = kickoff
					fixtureSheet.cell('E' + str(count)).value = status

					count += 1

		if processType == 2:
			if len(rowData) > 1:
				tableRow = rowData.find_all('tr', class_="report")
				for i in tableRow:
					# Identify the information about the Home Team
					homeTeam = i.find('span', class_="team-home teams")
					homeTeamURL = homeTeam.a['href']
					homeTeamName = homeTeam.a.get_text()
				
					# Identify the information about the Away Team
					awayTeam = i.find('span', class_="team-away teams")
					awayTeamURL = awayTeam.a['href']
					awayTeamName = awayTeam.a.get_text()

					result = i.find('span', class_="score")
					result = result.get_text()
					result = result.strip()
					if len(result.strip()) <= 3:
						homeScore = result[0]
						awayScore = result[2]
					else:
						scoreLine = result.striip()
						scoreLine.find('-')
						print(len(scoreLine))
						homeScore = '99'
						awayScore = '99'
					matchReport = i.find('a', class_='report')
					matchReport = matchReport['href']
					matchID = matchReport[16:len(matchReport)]

					matchSheet.cell('A' + str(count)).value = homeTeamName
					matchSheet.cell('B' + str(count)).value = awayTeamName
					matchSheet.cell('C' + str(count)).value = printFixtureDate
					matchSheet.cell('D' + str(count)).value = homeScore
					matchSheet.cell('E' + str(count)).value = awayScore
					matchSheet.cell('F' + str(count)).value = "http://www.bbc.co.uk" + matchReport
					matchSheet.cell('G' + str(count)).value = matchID

					count += 1
	print ('Fixtures and Team Results completed... ')
	workBook.save(os.path.join(localPath + ds + '.xlsx'))
	print (hr)

processContainer(fixtureContainer, 1)
processContainer(resultsContainer, 2)

# Pull URL from Match Sheet and process Player Results
maxResultRow = matchSheet.get_highest_row()
for row in range(2, matchSheet.get_highest_row()):
	homeTeam = matchSheet['A' + str(row)].value
	awayTeam = matchSheet['B' + str(row)].value
	matchURL = matchSheet['F' + str(row)].value
	
	print (homeTeam + ' v. ' + awayTeam)
	print (matchURL)

	# Parse Match Results
	matchResult = requests.get(matchURL)
	matchResult.raise_for_status()
	matchSoup = bs4.BeautifulSoup(matchResult.text, "html.parser")
	matchDetails = matchSoup.find('div', class_="story-body")
	matchHomeTeam = matchDetails.find('div', id="home-team")

	# Find home team, away team and team badges:


	print (shr)

print ('Max Result Row is: ' + str(maxResultRow))

print (hr)