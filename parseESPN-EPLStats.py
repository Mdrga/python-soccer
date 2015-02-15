# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2014
Modified on Nov 03, 2014
Version 0.02.d
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime
import requests
import os
import platform
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%H:%M:%S")
    return update

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print 'Downloading %s...' % (localFileName)
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

# Program Version & System Variables
parseVersion = 'ESPN Premier League Match Stats v0.02.d'
print ds + ' :: ' + ts + ' :: ' + parseVersion
print sys.version

# Set Output Path for Windows or Mac environments
os_System = platform.system()
win_BasePath = "C:/Users/Rainier/Documents/GitHub/python-soccer"

if os_System == "Windows":
    outputPath = win_BasePath + "/PL-Data/"
    outputImgPath = win_BasePath + "/PL-Data/imgs/"
    outputTeamPath = win_BasePath + "/PL-Data/teams/"
    outputMatchPath = win_BasePath + "/PL-Data/match/"
else:
    outputPath = 'PL-Data/'
    outputImgPath = 'PL-Data/imgs/'
    outputTeamPath = 'PL-Data/teams/'
    outputMatchPath = 'PL-Data/match/'

hr = " >>> *** ====================================================== *** <<<"
shr = " >>> *** ==================== *** <<<"

# Return Team Name or Team URL
def teamName (x, y, z):
	passHTML = x
	outputOption = y
	teamSide = z
	returnOutput = ''

	if teamSide == 'A':
		if outputOption == 'N': 
			passHTML = passHTML.find("p", {"class":"team-name floatleft"})
			passHTML = passHTML.get_text(strip=True)
			returnOutput = passHTML
		elif outputOption == 'U':
			passHTML = passHTML.find("a")
			passHTML = passHTML["href"]
			returnOutput = passHTML
	elif teamSide == 'H':
		if outputOption == 'N': 
			passHTML = passHTML.find("p", {"class":"team-name floatright"})
			passHTML = passHTML.get_text(strip=True)
			returnOutput = passHTML
		elif outputOption == 'U':
			passHTML = passHTML.find("a")
			passHTML = passHTML["href"]
			returnOutput = passHTML
	return returnOutput

def teamBadge (x,y):
	teamInfo = x
	sideToOutput = y
	teamSide = teamName(x,'N', sideToOutput)
	teamBadge = teamInfo.find("img")
	teamBadge = teamBadge["src"]
	teamBadge = teamBadge[0:len(teamBadge[0:len(teamBadge)-5])]
	outputTeamBadge = outputImgPath + teamSide + '.png'
	if os.path.isfile(outputTeamBadge):
		with open(outputTeamBadge) as file:
			pass
	else:
		downloadImage(teamBadge, outputTeamBadge)
	return outputTeamBadge 

def goalScorer(x,y):
	teamInfo = x
	teamSide = y
	goalsScored = []
	if teamSide == 'A':
		goalScorer = teamInfo.find_all("ul", {"class":"goal-scorers"})
		# print goalScorer
		for i in goalScorer:
			goalScored = i.find_all("li")
			for i in goalScored:
				scorer = i.get_text(strip=True)
				# print scorer
				scorer = scorer[1:(len(scorer)-3)] + ' ' + scorer[len(scorer)-3:len(scorer)]
				print scorer
				goalsScored.append(scorer)
	elif teamSide == 'H':
		goalScorer = teamInfo.find_all("ul", {"class":"goal-scorers"})
		for i in goalScorer:
			goalScored = i.find_all("li")
			for i in goalScored:
				scorer = i.get_text(strip=True)
				# print scorer
				scorer = scorer[0:len(scorer)-4] + ' ' + scorer[len(scorer)-4:len(scorer)-1]
				goalsScored.append(scorer)
				print scorer
	return goalsScored

# Returns the team stats based upon the parameters given.
def teamStats(x, y, z):
	teamInfo = x
	teamSide = y
	outputType = z
	if teamSide == 'A':
		teamStats = teamInfo[2].find_all("li")
	elif teamSide == 'H':
		teamStats = teamInfo[1].find_all("li")
	teamName = teamStats[0].get_text()
	teamShots = teamStats[1].get_text()
	findSOGstart = teamShots.find("(")
	findSOGend = teamShots.find(")")
	teamTotalShots = teamShots[0:findSOGstart]
	teamShotsOnGoal = teamShots[findSOGstart+1:findSOGend]
	teamTackles = teamStats[2].get_text()
	teamFouls = teamStats[3].get_text()
	if outputType == 0:
		statOutput = teamTotalShots
	elif outputType == 1:
		statOutput = teamShotsOnGoal
	elif outputType == 2:
		statOutput = teamTackles
	elif outputType == 3:
		statOutput = teamFouls
	else:
		statOutput = 'Invalid Option'
	return statOutput

def statParse(x):
	statResult = x
	if statResult == '-':
		statResult = 0

	return statResult

# Parses out the Squad based upon the parameters given.
def squadParse(x, y, z):
	# Receive a table and parse out the player stats
	squad = x
	# print 'Squad Length is: ' + str(len(squad))
	teamSide = y
	gameDate = z
	maxLength = len(squad)
	starterCount = 2
	subCount = 16
	if teamSide == 'A':
		teamSide = awaySide
		side = 'Away'
	elif teamSide == 'H':
		teamSide = homeSide
		side = 'Home'
	while starterCount < 13:
	#	Parse out the Stat Line for the Players
		currentRow = squad[starterCount]
		playerData = currentRow.find_all("td")
		playerPOS = playerData[0].get_text()
		playerJersey = playerData[1].get_text()
		playerName = playerData[2].get_text(strip=True)

		playerURL = playerData[2].find("a")
		playerURL = playerURL["href"]
		playerStartID = playerURL.find("r/")
		playerID = playerURL[8:(len(playerURL)-len(playerName)-1)]
	
		playerShots = statParse(playerData[3].get_text(strip=True))
		playerSOG = statParse(playerData[4].get_text(strip=True))
		playerGoals = statParse(playerData[5].get_text(strip=True))
		playerAssists = statParse(playerData[6].get_text(strip=True))
		# playerPoints = (playerSOG * 3) + (playerGoals * 10) + (playerAssists * 4)

		playerOffsides = statParse(playerData[7].get_text(strip=True))
		playerFoulsDrawn = statParse(playerData[8].get_text(strip=True))
		playerFoulsCommitted = statParse(playerData[9].get_text(strip=True))
		playerSaves = statParse(playerData[10].get_text(strip=True))
		playerYellowCards = statParse(playerData[11].get_text(strip=True))
		playerRedCards = statParse(playerData[12].get_text(strip=True))
		outputRow = gameDate + '|' + teamSide + '|' + side + '|' + matchID + '|' + playerID + '|' + playerPOS + '|' + playerJersey + '|' + playerName + '|' + '"' + playerURL + '"' + '|' + str(playerShots) + '|' + str(playerSOG) + '|' +  str(playerGoals) \
		      + '|' + str(playerAssists) + '|' + str(playerOffsides) + '|' + str(playerFoulsDrawn) + '|' + str(playerFoulsCommitted) + '|' + str(playerSaves) + '|' + str(playerYellowCards) \
		      + '|' + str(playerRedCards) + '|Starter|' + 'N'+ '|' + '|' + '\n' # str(playerPoints) + 
		# print shr
		playerData = 'epl-playerstats.txt'
		outputPlayerData = os.path.join(outputMatchPath, playerData)
		with open(outputPlayerData, "a") as f:
			f.write(outputRow)
			f.close()
		# print outputRow

		starterCount += 1
	while subCount < maxLength:
		currentRow = squad[subCount]
		# print currentRow
		subCount += 1
		playerData = currentRow.find_all("td")
		playerPOS = playerData[0].get_text()
		playerJersey = playerData[1].get_text()
		playerName = playerData[2].get_text(strip=True)
		playerAttrs = playerData[2]
		playerAttrs = playerAttrs.div
		if playerAttrs != None:
			playerSubbing = str(playerAttrs)
			playerTimeOn = playerSubbing[147:150]
			playerSubbedName = playerSubbing[150+19:len(playerSubbing)-11]
		else:
			playerSubbedName = ''
			playerTimeOn = ''
		playerURL = playerData[2].find("a")
		playerURL =  playerURL["href"]
		playerStartID = playerURL.find("r/")
		playerID = playerURL[8:(len(playerURL)-len(playerName)-1)]
		playerSubbed = playerData[2].find("div", {"class":"soccer-icons soccer-icons-subinout"})
		playerShots = statParse(playerData[3].get_text(strip=True))
		playerSOG = statParse(playerData[4].get_text(strip=True))
		playerGoals = statParse(playerData[5].get_text(strip=True))
		playerAssists = statParse(playerData[6].get_text(strip=True))
		playerOffsides = statParse(playerData[7].get_text(strip=True))
		playerFoulsDrawn = statParse(playerData[8].get_text(strip=True))
		playerFoulsCommitted = statParse(playerData[9].get_text(strip=True))
		playerSaves = statParse(playerData[10].get_text(strip=True))
		playerYellowCards = statParse(playerData[11].get_text(strip=True))
		playerRedCards = statParse(playerData[12].get_text(strip=True))
		if playerSubbed != None:
			playerSubbed = 'Y'
		else:
			playerSubbed = 'N'
		outputRow = gameDate + '|' + teamSide +  '|' + side + '|' + matchID + '|' + playerID + '|' + playerPOS + '|' + playerJersey + '|' + playerName + '|' + '"' + playerURL + '"' + '|' + str(playerShots) + '|' + str(playerSOG) + '|' +  str(playerGoals) \
		      + '|' + str(playerAssists) + '|' + str(playerOffsides) + '|' + str(playerFoulsDrawn) + '|' + str(playerFoulsCommitted) + '|' + str(playerSaves) + '|' + str(playerYellowCards) \
		      + '|' + str(playerRedCards) + '|Bench|' + playerSubbed + '|' + playerSubbedName + '|' + playerTimeOn + '\n' # str(playerPoints) + '\n'
		# print outputRow
		playerData = 'epl-playerstats.txt'
		outputPlayerData = os.path.join(outputMatchPath, playerData)
		with open(outputPlayerData, "a") as f:
			f.write(outputRow)
			f.close()

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
	else:
		outputMonth = '07'
	return outputMonth

# ESPN Scores & Fixtures Date URL = 
# http://www.espnfc.us/barclays-premier-league/23/scores?date=20141026

print hr
playerData = 'epl-playerstats.txt'
outputPlayerData = os.path.join(outputMatchPath, playerData)
with open(outputPlayerData, "w") as f:
			f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
			f.write('Team|Side|Match ID|Player ID|POS|#|Name|URL|Shots|Shots On Goal|Goals|Assists|Offsides|Fouls Drawn|Fouls Committed|Saves|Yellow Cards|Red Cards|Status|Subbed Player|SubName|TimeOn|Points' + '\n' )
			f.close()

matchURLs = ['http://www.espnfc.us/gamecast/statistics/id/395758/statistics.html', 'http://www.espnfc.us/gamecast/statistics/id/395753/statistics.html']

# URLs for Main Body of Script to work through
fixturesURL = "http://www.bbc.com/sport/football/premier-league/fixtures"
fixturesOpen = urllib2.urlopen(fixturesURL)
fixturesSoup = BeautifulSoup(fixturesOpen)
print updateTS() + ' Fixtures Read'
print shr

# URLS for Main Body of Script to get Results
resultsURL = "http://www.bbc.com/sport/football/premier-league/results"
resultsOpen = urllib2.urlopen(resultsURL)
resultsSoup = BeautifulSoup(resultsOpen)
print updateTS() + ' Results Read'
print shr

prefixBBC = "http://www.bbc.com"
prefixESPN = "http://www.espnfc.us"

# Save a local copy of the Fixtures Page
outputBase = 'PL-Fixtures.html'
outputResults = 'PL-Results.html'
outputTable = "PL-fixture-table.html"

# Find the containers with the Fixtures information within the HTML page
fixtureList = fixturesSoup.find("div", {"class":"stats"})
fixtureDiv = fixtureList.find("div", {"class":"fixtures-table full-table-medium"})
resultsList = resultsSoup.find("div", {"class":"stats"})
resultsDiv = resultsList.find("div", {"class":"fixtures-table full-table-medium"})

# Parse out the main Fixture Table to a local file
fixturesTable = fixturesSoup.find("div", {"class":"stats-body"})
matchesResults = resultsDiv.find_all("table")
resultsDate = resultsDiv.find_all("h2", {"class":"table-header"})

matchDates = []
teamURLs = []
counter = 0
matchDate = fixtureDiv.find_all("h2", {"class":"table-header"})
matches = fixtureDiv.find_all("table")

while counter < len(resultsDate):
	matchesDate = resultsDate[counter]
	matchesDate = matchesDate.get_text(strip=True)
	# print matchesDate
	matchesDate = textDate(matchesDate)
	# print matchesDate
	matchDates.append(matchesDate)
	counter += 1

'''
while counter < len(matchDate):
	fixtureDate = matchDate[counter]
	fixtureDate = fixtureDate.get_text(strip=True)
	fixtureDate = textDate(fixtureDate)
	matchDates.append(fixtureDate)
	counter += 1
'''
eplMatchBaseURL = "http://www.espnfc.us/barclays-premier-league/23/scores?date="
matchReportURL = []
matchReportID = []

for i in matchDates:
    matchDate = i
    matchURL = eplMatchBaseURL + matchDate
    matchOpen = urllib2.urlopen(matchURL)
    matchSoup = BeautifulSoup(matchOpen)
    matchTXT = 'espn-scores-' + matchDate + '.txt'
    matchHTML = 'espn-scores-' + matchDate + '.html'
    outputMatch = os.path.join(outputMatchPath, matchHTML)
    # outputMatchText = os.path.join(outputMatchPath, matchTXT)
    scores = matchSoup.find("div", {"class":"scores"})
    # with open(outputMatch, "w") as f:
    #    f.write(ds + ' :: ' + ts + ' :: ' + parseVersion)
    #    f.write(scores.prettify())
    #     f.close()   
    counter = 0
    # print "Number of Matches is: " + str(len(scores))    
    boxScore = scores.find_all("div", {"class":"score-box"})
    for i in boxScore:
        # print shr
        # print i
        matchID = i.find("div", {"class":"score full"})
        matchID = str(matchID)
        matchReportID.append(matchID[37:43] + "|" + matchDate)
        # print updateTS()
        # print hr
        counter += 1

print hr

for i in matchReportID:
	matchID = i[0:6]
	# print matchID
	matchDate = i[7:len(i)]
	matchPrefix = 'http://www.espnfc.us/gamecast/statistics/id/'
	matchSuffix = '/statistics.html'
	# print matchDate
	matchReportURL.append(matchDate + "|" + matchPrefix + matchID + matchSuffix)

# matchReportURL = ['http://www.espnfc.us/gamecast/statistics/id/395696/statistics.html', 'http://www.espnfc.us/gamecast/statistics/id/395689/statistics.html', 'http://www.espnfc.us/gamecast/statistics/id/395688/statistics.html', \
# 'http://www.espnfc.us/gamecast/statistics/id/395693/statistics.html', 'http://www.espnfc.us/gamecast/statistics/id/395695/statistics.html', 'http://www.espnfc.us/gamecast/statistics/id/395690/statistics.html']

countArray = len(matchReportURL)
countDown = 0

outputTxt = 'teamNews.txt'
with open(outputTxt, "w") as f:
   	f.write(ds + " :: " + updateTS() + " :: " + parseVersion + '\n' )
   	f.close()

for i in matchReportURL:
	gameURL = i[9:len(i)]
	gameDate = i[0:8]
	if gameURL == "http://www.espnfc.us/gamecast/statistics/id/395672/statistics.html":
		gameURL = "http://www.espnfc.us/gamecast/statistics/id/395675/statistics.html"
	print gameDate
	print gameURL
	gameHTML = urllib2.urlopen(gameURL)
	gameSoup = BeautifulSoup(gameHTML)	
	matchID = gameURL[44:len(gameURL)-16]
	print "The Game URL is: " +  gameURL

	# Output a local copy of the FULL ESPN page to the local drive
	outputBase = 'ESPN-EPL-' + matchID + '.html'
	outputBase = os.path.join(outputPath, outputBase)
	with open(outputBase, "w") as f:
    	 f.write(gameSoup.prettify("utf-8"))
     	f.close()

    # Main Container for Game Stats
	gameHeader = gameSoup.find("div", {"class":"container clearfix"})

	# <section class="match final gamecast-match" id="matchcenter-395758">
	gameMatch = gameHeader.find("section", {"class":"match final gamecast-match"})
	reportAwayTeam = gameMatch.find("div", {"class":"team home"})
	getURLAwayTeam = reportAwayTeam.find("a")
	teamURLs.append(getURLAwayTeam["href"])
	reportHomeTeam = gameMatch.find("div", {"class":"team away"})     

	# Finds the Home and Away Sides in the Results Page
	homeSide = teamName(reportHomeTeam, 'N', 'H')
	homeURL =  prefixESPN + teamName(reportHomeTeam, 'U', 'H')
	homeBadge = teamBadge(reportHomeTeam, 'H')
	awaySide = teamName(reportAwayTeam, 'N', 'A')
	awayURL = prefixESPN + teamName(reportAwayTeam, 'U', 'H')
	awayBadge = teamBadge(reportAwayTeam, 'A')

	# Finds Match Info from Results Page
	# ESPN Changed their Match Stat Page Format 
	# This portion is deprecated as of 2014-Nov-03
	matchSummary = gameHeader.find("section", {"class":"mod-container gc-stat-list"})
	#matchSummary = gameHeader.find("div", {"class":"tab-cont matchstats"})
	matchStats = matchSummary.find_all("ul")
	
	# Counter to Iterate through Game Roster and Stats
	rsCounter = 0

	#Finds Player Info from Results Page
	playerSummary = gameHeader.find("div", {"class":"span-12 column"})

	playerStats = playerSummary.find_all("table")
	homeStats = playerStats[0]
	homePlayers = homeStats.find_all("tr")
	awayStats = playerStats[1]
	awayPlayers = awayStats.find_all("tr")   

	# Need to add a Parse of the Game Date to this player output.
	squadParse(homePlayers, 'H', gameDate)
	squadParse(awayPlayers, 'A', gameDate)

	# Identifies the Match ID
	print gameSoup.title.get_text() 
	# print gameURL 
	countDown += 1
	print "Games left to parse = " + str(countArray - countDown)
	print "Games that have been parsed = " + str(countDown) 
	print ds + " :: " + updateTS()
	print hr

def teamNews(x):
	teamURL = x
	teamName = x
	teamName = teamName[6:len(teamName)-10]
	teamURL = prefixESPN + teamURL
	teamHTML = urllib2.urlopen(teamURL)
	teamSoup = BeautifulSoup(teamHTML)	
	recentNews = teamSoup.find("div", {"id":"feed"})
	recentNewsItems = recentNews.find_all("div", {"class":"feed-item-content"})
	recapOutput = []
	print "Team News Parsed :: " + teamName
	for i in recentNewsItems:
		recapPhotoItem = i.find("div", {"class":"thumbnail picture"})

		if len(i) > 3:
			# recapPhotoItem = recapPhotoItem.find("img")
			# print recapPhotoItem["src"]
			# with open(outputTxt, "a") as f:
			#	f.write('\n' + shr + '\n')
			#	f.write(i.prettify())
			#	f.write('\n' + shr + '\n')
			#	f.close()
			# print shr
			recapHeadline = i.find("h2")
			recapHeadline = recapHeadline.get_text(strip=True)
			recapAge = i.find("span", {"class":"age"})
			recapAge = recapAge.get_text(strip=True)
			recapOutput.append(date + "|" + teamName + "|" + recapHeadline + "|" + recapAge)
			#recapDetails = recapHeadline.find("a")
			#recapDetails = recapDetails["href"]
			#print recapDetails
			# print recapAge.get_text(strip=True)
			
			#print updateTS()
			#print shr
			# print i
		else:
			recapGameOpponents = i.find_all("div", {"class":"team-name"})
			recapGameScore = i.find_all("div", {"class":"team-score"})
			recapGameStatus = i.find("div", {"class":"game-info"})
			recapGameHome = recapGameOpponents[0].get_text(strip=True)
			recapGameAway = recapGameOpponents[1].get_text(strip=True)
			recapHomeScore = recapGameScore[0].get_text(strip=True)
			recapAwayScore = recapGameScore[1].get_text(strip=True)
			#recapGameInfo = i.find("div", {"clas=":"game-info"})
			recapOutput.append(date + "|" + teamName + "|" + recapGameHome + " " + recapHomeScore +  " v. " + recapAwayScore + " "+ recapGameAway)
			# print i
	print hr 
	return recapOutput

teamURLs = sorted(set(teamURLs))
teamURLtxt = 'teamURLs.txt'
with open(teamURLtxt, "w") as f:
   	f.write(ds + " :: " + updateTS() + " :: " + parseVersion + '\n' )
   	f.close()

for i in teamURLs:
	with open(teamURLtxt, "a") as f:
		f.write(i)
		f.write('\n')
		f.close()

teamNewstxt = 'teamNews.txt'
with open(teamNewstxt, "w") as f:
   	f.write(ds + " :: " + updateTS() + " :: " + parseVersion + '\n' )
   	f.close()

for i in teamURLs:
	for x in teamNews(i):
		with open(teamNewstxt, "a") as f:
			f.write(x + '\n')
			f.close()
