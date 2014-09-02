# -*- coding: utf-8 -*-

'''
Created on Jul 23, 2014
Modified on Aug 2$3, 2014
Version 0.13.i
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime
import requests
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Establish the process Date, Time and Version Stamp of the Script
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
parseVersion = 'Premier League 2014 - v0.13.i'

# URLs for Main Body of Script to work through
fixturesURL = "http://www.bbc.com/sport/football/premier-league/fixtures"
fixturesOpen = urllib2.urlopen(fixturesURL)
fixturesSoup = BeautifulSoup(fixturesOpen)

# URLS for Main Body of Script to get Results
resultsURL = "http://www.bbc.com/sport/football/premier-league/results"
resultsOpen = urllib2.urlopen(resultsURL)
resultsSoup = BeautifulSoup(resultsOpen)

outputPath = 'PL-Data/'
outputImgPath = 'PL-Data/imgs/'
outputTeamPath = 'PL-Data/teams/'
outputMatchPath = 'PL-Data/match/'
prefix = "http://www.bbc.com"

# Save a local copy of the Fixtures Page
outputBase = 'PL-Fixtures.html'
outputResults = 'PL-Results.html'
outputTable = "PL-fixture-table.html"

outputBase = os.path.join(outputPath, outputBase)
with open(outputBase, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
     f.write(fixturesSoup.prettify("utf-8"))
     f.close()

outputResults = os.path.join(outputPath, outputResults)
with open(outputResults, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
     f.write(resultsSoup.prettify("utf-8"))
     f.close()

# Find the containers with the Fixtures information within the HTML page
fixtureList = fixturesSoup.find("div", {"class":"stats"})
fixtureDiv = fixtureList.find("div", {"class":"fixtures-table full-table-medium"})
resultsList = resultsSoup.find("div", {"class":"stats"})
resultsDiv = resultsList.find("div", {"class":"fixtures-table full-table-medium"})

# Parse out the main Fixture Table to a local file
fixturesTable = fixturesSoup.find("div", {"class":"stats-body"})
outputTable = os.path.join(outputPath, outputTable)
with open(outputTable, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n' + '\n')
     f.write(fixtureDiv.prettify("utf-8"))
     f.close()

# Create Iteration to Output Fixtures by Date
counter = 0
matchDate = fixtureDiv.find_all("h2", {"class":"table-header"})
matches = fixtureDiv.find_all("table")
matchesResults = resultsDiv.find_all("table")
resultsDate = resultsDiv.find_all("h2", {"class":"table-header"})

# Create a function to return the Team Name or URL
# x = Incoming data from the HTML
# y = 'H'ome or 'A'way Team
# z = 'N'ame / 'H'REF or 'O'ther Data
def returnTeam(x, y, z):
	teamContent = x
	teamSearch = y
	outputFormat = z
	teamSearchReturn = ""
	output = ''

	# Search for either the Home or Away Team Span
	if teamSearch == 'H':
		teamSearchReturn = teamContent.find("span", {"class":"team-home teams"})
	elif teamSearch == 'A':
		teamSearchReturn = teamContent.find("span", {"class":"team-away teams"})
	else:
		teamSearchReturn = "Invalid Team Type Parameter Passed. Please pass either an H or an A."
	
	# Intake Team and establish Output Format
	if outputFormat == 'N':
		output = teamSearchReturn.get_text(strip=True)
	elif outputFormat == 'H':
		output = teamSearchReturn.a
		output = output.get("href")
	else:
		output = output + " :: Additionally the Format Indicator Selected is Incorrect."

	return output

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
	output = dayOfWeek + '|' + year +'-' + month + '-' + day
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
	else:
		outputMonth = '07'
	return outputMonth

outputTxt = "PL-fixture.txt"
outputTxt = os.path.join(outputMatchPath, outputTxt)

# Create file that parses out the Fixture Details
with open(outputTxt, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n' + '\n')
     f.write("dayOfWeek|fixtureDate|matchKickoff|matchID|matchStatus|homeName|awayName|homeURL|awayURL|score|matchURL" + '\n')
     f.close()

'''	  
TODO - Create a log table within the database to track when the process runs
       Log Table should read: DateStamp | TimeStamp | Script Version
TODO - Track if the parsing of the URL was successful
TODO - DateTime stamp the row when written to the database
TODO - Parse data to database
'''	

# Create an array to capture all the teams in Premier League Play
teamURLs = []
resultURLs = []

def fixtureResults(x):
	fixtureResults = x
	matchID = fixtureResults.get("id")
	matchID = matchID[10:len(matchID)]
	matchKickoff = fixtureResults.find("td", {"class":"time"})
	matchKickoff = matchKickoff.get_text(strip=True)
	matchStatus = fixtureResults.find("td", {"class":"status"})
	matchURL = matchStatus.find("a")
	matchURL = matchURL["href"]
	matchStatus = matchStatus.get_text(strip=True)
	homeName = returnTeam(fixtureResults, 'H', 'N') 
	homeURL = returnTeam(fixtureResults, 'H', 'H')
	awayName = returnTeam(fixtureResults, 'A', 'N') 
	awayURL = returnTeam(fixtureResults, 'A', 'H')
	teamURLs.append(homeURL)
	teamURLs.append(awayURL)
	score = i.find("span", {"class":"score"})
	score = score.get_text(strip=True)
	resultURLs.append(matchURL + '|' + matchID)
	output = '|' + matchID + '|' + matchStatus + '|' + homeName + '|' + awayName + '|' + homeURL + '|' + awayURL + '|' + score + '|' + matchURL + '\n'
	return output

while counter < len(resultsDate):
	matchesDate = resultsDate[counter]
	matchesDate = matchesDate.get_text(strip=True)
	matchesDate = textDate(matchesDate)
	matchesBlock = matchesResults[counter]
	matchesReport = matchesBlock.find_all("tr", {"class":"report"})
	for i in matchesReport:
		# print matchesDate + fixtureResults(i)
		with open(outputTxt, "a") as f:
			f.write(matchesDate + '|' + (fixtureResults(i)))
			f.close()
	# print matchesDate
	counter += 1 

counter = 0
while counter < len(matchDate):
# Line below is used for Unit Testing of Code
# while counter < 2:
	# Parse out the pieces of the Fixture from the main HTML container
	fixtureDate = matchDate[counter]
	fixtureDate = fixtureDate.get_text(strip=True)
	fixtureDate = textDate(fixtureDate)
	print fixtureDate
	fixtureBlock = matches[counter]
	fixtureReport = fixtureBlock.find_all("tr", {"class":"report"})
	fixtureLive = fixtureBlock.find_all("tr", {"class":"live"})
	fixturePreview = fixtureBlock.find_all("tr", {"class":"preview"})
	# Parse out the components of the Fixture. Create a single line to parse the data out
	# Matches that have Completed
	for i in fixtureReport:
		# print fixtureResults(i)
		# matchID = i.get("id")
		# matchID = matchID[10:len(matchID)]
		# matchKickoff = i.find("td", {"class":"time"})
		# matchKickoff = matchKickoff.get_text(strip=True)
		# matchStatus = i.find("td", {"class":"status"})
		# matchURL = matchStatus.find("a")
		# matchURL = matchURL["href"]
		# matchStatus = matchStatus.get_text(strip=True)
		# homeName = returnTeam(i, 'H', 'N') 
		# homeURL = returnTeam(i, 'H', 'H')
		# awayName = returnTeam(i, 'A', 'N') 
		# awayURL = returnTeam(i, 'A', 'H')
		# teamURLs.append(homeURL)
		# teamURLs.append(awayURL)
		# score = i.find("span", {"class":"score"})
		# score = score.get_text(strip=True)
		# print resultURLs
		# print fixtureDate + "|" + matchKickoff + ' GMT' + '|' + matchID + '|' + matchStatus + '|' + homeName + '|' + awayName + '|' + homeURL + '|' + awayURL
		# print fixtureDate + ' ' + matchStatus + ' ' + homeName + ' ' + score + ' ' + awayName
		with open(outputTxt, "a") as f:
			f.write(fixtureDate + '|' + fixtureResults(i))
			f.close()
	
	# Matches In Progress
	for i in fixtureLive:
		matchID = i.get("id")
		matchID = matchID[10:len(matchID)]
		matchKickoff = i.find("td", {"class":"time"})
		matchKickoff = matchKickoff.get_text(strip=True)
		matchStatus = i.find("td", {"class":"status"})
		matchURL = matchStatus.find("a")
		matchURL = matchURL["href"]
		matchStatus = matchStatus.get_text(strip=True)
		homeName = returnTeam(i, 'H', 'N') 
		homeURL = returnTeam(i, 'H', 'H')
		awayName = returnTeam(i, 'A', 'N') 
		awayURL = returnTeam(i, 'A', 'H')
		teamURLs.append(homeURL)
		teamURLs.append(awayURL)
		score = i.find("span", {"class":"score"})
		score = score.get_text(strip=True)
		# print fixtureDate + "|" + matchKickoff + ' GMT' + '|' + matchID + '|' + matchStatus + '|' + homeName + '|' + awayName + '|' + homeURL + '|' + awayURL
		# print fixtureDate + ' ' + matchStatus + ' ' + homeName + ' ' + score + ' ' + awayName
		with open(outputTxt, "a") as f:
			f.write(fixtureDate + "|" + '|' + matchID + '|' + matchStatus + ' - ' + matchKickoff + '|' + homeName + '|' + awayName + '|' + prefix \
			+ homeURL + '|' + prefix + awayURL + '|' + score + '|' + prefix + matchURL + '\n')
			f.close()
	# Matches To Be Played
	for i in fixturePreview:
		matchID = i.get("id")
		matchID = matchID[10:len(matchID)]
		matchKickoff = i.find("td", {"class":"kickoff"})
		matchKickoff = matchKickoff.get_text(strip=True)
		matchStatus = i.find("td", {"class":"status"})
		matchStatus = matchStatus.get_text(strip=True)
		if len(matchStatus) > 0:
		    matchStatus = matchStatus[0:7]
		homeName = returnTeam(i, 'H', 'N') 
		homeURL = returnTeam(i, 'H', 'H')
		awayName = returnTeam(i, 'A', 'N') 
		awayURL = returnTeam(i, 'A', 'H')
		teamURLs.append(homeURL)
		teamURLs.append(awayURL)
		# print fixtureDate + "|" + matchKickoff + ' GMT' + '|' + matchID + '|' + matchStatus + '|' + homeName + '|' + awayName + '|' + homeURL + '|' + awayURL
		# print fixtureDate + ' ' + matchStatus + ' ' + homeName + ' v. ' + awayName
		with open(outputTxt, "a") as f:
			f.write(fixtureDate + "|" + matchKickoff + ' GMT' + '|' + matchID + '|' + matchStatus + '|' + homeName + '|' + awayName + '|' + homeURL + '|' + awayURL + '||' + '\n')
			f.close()
	counter +=1
print "Input Determined..."

# Sort and Remove Duplicates from the array of Premier League Teams
teamURLs = sorted(set(teamURLs))
localTeamFile = []

def teamParse(x, y):
    teamURL = x
    outputFormat = y
    
    teamOpen = urllib2.urlopen(prefix + teamURL)
    teamSoup = BeautifulSoup(teamOpen)
    
    teamName = teamURL[22:len(teamURL)]
    teamNameHTML = teamName + '.html'
    teamNameHTML = os.path.join(outputTeamPath, teamNameHTML)
    localTeamFile.append(teamNameHTML)
    teamTitle = str(teamSoup.title.get_text(strip=True))
    teamTitle = teamTitle[24:len(teamTitle)]
    
    with open(teamNameHTML, "w") as f:
        f.write(teamSoup.prettify('utf-8'))
        f.close()
    
    output = []
    matchData = teamSoup.find("div", {"id":"last-next-match"})
    teamMain = teamSoup.find("div", {"id":"indexpage-body"})
      
    # For the option of 'L' print the details of the LAST MATCH
    if outputFormat == 'L':
        lastMatch = matchData.find("div", {"id":"last-match"})
        lastMatchTeam = matchData.find("span", {"class":"match-against"})
        # lastMatchTeam = lastMatchTeam.get_text(strip=True)
        lastMatchTeam = lastMatchTeam.get_text(strip=True)
        lastMatchTeamName = lastMatchTeam[2:len(lastMatchTeam)-6]
        # print lastMatchTeamName.encode('utf-8')
        lastMatchLeague = lastMatch.find("span", {"class":"match-league"})
        lastMatchLeague = lastMatchLeague.get_text(strip=True)
        lastMatchOutcome = lastMatch.find("span", {"class":"match-outcome"})
        lastMatchOutcome = lastMatchOutcome.get_text(strip=True)
        lastMatchScore = matchData.find("span", {"class":"match-score"})
        lastMatchScore = lastMatchScore.get_text(strip=True)
        lastMatchDate = matchData.find("span", {"itemprop":"startDate"})
        lastMatchDate = lastMatchDate.get_text(strip=True)
        lastMatchDate = lastMatchDate[0:10]
        lastMatchURL = lastMatch.find_all("a")
        lastMatchStatus = matchData.find("span", {"class":"match-status"})
        lastMatchStatus = lastMatchStatus.get_text(strip=True)
        if len(lastMatchURL) == 2:
        	matchURL = 1
        else:
        	matchURL = 2
        output = teamTitle.encode('utf-8') + "|" + lastMatchLeague + "|" + lastMatchDate + "|" + lastMatchTeam[0:2] + ' ' + lastMatchTeamName + " " + lastMatchTeam[len(lastMatchTeam)-6:len(lastMatchTeam)] + '|' + lastMatchOutcome + '|' + lastMatchScore + '|' + prefix + lastMatchURL[matchURL]["href"]
    elif outputFormat == 'N':
        nextMatch = matchData.find("div", {"id":"next-match"})
        nextMatchTeam = nextMatch.find("span", {"class":"match-against"})
        nextMatchTeam = nextMatchTeam.get_text(strip=True)
        nextMatchTeamName = nextMatchTeam[2:len(nextMatchTeam)-6]
        # print nextMatchTeamName
        nextMatchDate = nextMatch.find("span", {"itemprop":"startDate"})
        nextMatchDate = nextMatchDate.get_text(strip=True)
        nextMatchDate = nextMatchDate[0:10]
        nextMatchLeague = nextMatch.find("span", {"class":"match-league"})
        nextMatchLeague = nextMatchLeague.get_text(strip=True)
        nextMatchStatus = nextMatch.find("span", {"class":"match-status"})
        nextMatchStatus = nextMatchStatus.get_text(strip=True)
        output = teamTitle.encode('utf-8') + '|' + nextMatchLeague + '|' + nextMatchDate + '|' + nextMatchTeam[0:2] + ' ' + nextMatchTeamName + ' ' + nextMatchTeam[len(nextMatchTeam)-6:len(nextMatchTeam)] + '|' +nextMatchStatus + '||'
    return output

outputNext = "PL-next-fixture.txt"
outputLast = "PL-last-fixture.txt"
outputNext = os.path.join(outputTeamPath, outputNext)
outputLast = os.path.join(outputTeamPath, outputLast)

# Match Report URL:  /sport/football/28718345
# print resultURLs

'''
resultsOutput = resultURLs
teamURL = teamURLs[0]
# print teamURL

resultDetail = resultsOutput.find("/")
lenResult = resultDetail
resultMatch = resultsOutput[lenResult+1:len(resultsOutput)]
resultDetail = prefix + resultsOutput[0:resultDetail]
'''
'''
matchResults = urllib2.urlopen(resultDetail)
matchSoup = BeautifulSoup(matchResults)

outputMatchResult = resultMatch + '.html'
outputMatchResult = os.path.join(outputMatchPath, outputMatchResult)
resultMainDiv = matchSoup.find("div", {"id":"content-wrapper"})
outputMainDiv = resultMatch + '-maindiv.html'
outputMainDiv = os.path.join(outputMatchPath, outputMainDiv)

with open(outputMatchResult, "w") as f:
    f.write(ds + ' :: ' + ts + ' :: Match Result File :: ' + parseVersion + '\n' + '\n')
    f.write(matchSoup.prettify())
    f.close()
with open(outputMainDiv, "w") as f:
    f.write(ds + ' :: ' + ts + ' :: Match Div Results File :: ' + parseVersion + '\n' + '\n')
    f.write(resultMainDiv.prettify())
    f.close()

# Download of an Image via Requests Library.
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print 'Downloading %s...' % (localFileName)
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

print localTeamFile


    # Download Badge from Site
    homeBadgeURL = homeTeamBadge["src"]
    homeBadgeFile = homeBadgeURL[64:len(homeBadgeURL)]
    homeBadge = os.path.join(outputPath, homeBadgeFile)
    downloadImage(homeBadgeURL, homeBadge)

# print matchSoup.prettify()


# Comment out to work on Team Details Parsing
with open(outputNext, "w") as f:
	f.write(ds + ' :: ' + ts + ' :: Next Match File :: ' + parseVersion + '\n' + '\n')
	f.close()
with open(outputLast, "w") as f:
	f.write(ds + ' :: ' + ts + ' :: Last Match File :: ' + parseVersion + '\n' + '\n')
	f.close()

for i in teamURLs:
	with open(outputNext, "a") as f:
		f.write(teamParse(i,'N') + '\n')
		f.close()
	with open(outputLast, "a") as f:
		f.write(teamParse(i,'L') + '\n')
		f.close()
'''