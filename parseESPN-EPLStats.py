# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2014
Modified on Sep 22, 2016
Version 0.03.hb
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
=================================================================================================
*** 2016-09-22  RWM   Updated the code to remove Excel file references and Excel library
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import datetime
import requests
# import openpyxl
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

# Establish MySQL Connection for General Use
cnx = mysql.connector.connect(user='root', password='password',
								 host='127.0.0.1',
								 database='fanfootball',
								 use_pure=False)

#Establish MySQL Connection for Fixture Use
fixtureCnx = mysql.connector.connect(user='root', password='password',
                                 host='127.0.0.1',
                                 database='fanfootball',
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
parseVersion = 'ESPN Premier League Match Stats v0.03.h'
print (ds + ' :: ' + ts + ' :: ' + parseVersion)
print (sys.version)

# Set Output Path for Windows or Mac environments
os_System = platform.system()
win_BasePath = "D:/ESPN-Parser/"
seasonID = 2
leagueID = 1

# Output paths based on OS
if os_System == "Windows":
    # outputPath = win_BasePath + "/data/"
    outputImgPath = win_BasePath + "/img/"
    localPath = win_BasePath
    outputPath = win_BasePath
    localimgPath = outputImgPath
    outputTeamPath = win_BasePath + "/data/teams/"
    outputMatchPath = win_BasePath + "/data/match/"
else:
    outputPath = 'PL-Data/'
    outputImgPath = 'PL-Data/imgs/'
    outputTeamPath = 'PL-Data/teams/'
    outputMatchPath = 'PL-Data/match/'

# 2016-09-22 Deprecated Code for the creation of stats into an Excel Spreadsheet.
# Open Excel Object for Writing Data
# baseWkBkName = 'detail_stats.xlsx'
# workBook = openpyxl.load_workbook(os.path.join(localPath + baseWkBkName))
# coreSheet = workBook.get_sheet_by_name('CoreData')
# teamSheet = workBook.get_sheet_by_name('teams')
# playerSheet = workBook.get_sheet_by_name('players')
# matchSheet = workBook.get_sheet_by_name('matches')
# fixtureSheet = workBook.get_sheet_by_name('fixtures')

# Screen Output Dividers used for readability
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

# Will Need to Update with new season update and promotions / relegations...
# Current as of 2015/16
def returnTeam(x):
	inputTeam = x
	outputTeam = 0
	if inputTeam == 'AFC Bournemouth' or inputTeam == 'Bournemouth':
		outputTeam = 1
	elif inputTeam == 'Arsenal':
		outputTeam = 2
	elif inputTeam == 'Aston Villa':
		outputTeam = 3
	elif inputTeam == 'Chelsea':
		outputTeam = 4
	elif inputTeam == 'Crystal Palace':
		outputTeam = 5
	elif inputTeam == 'Everton':
		outputTeam = 6
	elif inputTeam == 'Leicester City' or inputTeam == 'Leicester':
		outputTeam = 7
	elif inputTeam == 'Liverpool':
		outputTeam = 8
	elif inputTeam == 'Manchester City' or inputTeam == 'Man City':
		outputTeam = 9
	elif inputTeam == 'Manchester United' or inputTeam == 'Man Utd':
		outputTeam = 10
	elif inputTeam == 'Newcastle United' or inputTeam == 'Newcastle':
		outputTeam = 11
	elif inputTeam == 'Norwich City' or inputTeam == 'Norwich':
		outputTeam = 12
	elif inputTeam == 'Southampton':
		outputTeam = 13
	elif inputTeam == 'Stoke City' or inputTeam == 'Stoke':
		outputTeam = 14
	elif inputTeam == 'Sunderland': 
		outputTeam = 15
	elif inputTeam == 'Swansea City' or inputTeam == 'Swansea':
		outputTeam = 16
	elif inputTeam == 'Tottenham Hotspur' or inputTeam == 'Tottenham':
		outputTeam = 17
	elif inputTeam == 'Watford': 
		outputTeam = 18
	elif inputTeam == 'West Bromwich Albion' or inputTeam == 'West Brom':
		outputTeam = 19
	elif inputTeam == 'West Ham United' or inputTeam == 'West Ham':
		outputTeam = 20
	elif inputTeam == 'Burnley':
		outputTeam = 24
	elif inputTeam == 'Hull' or inputTeam == 'Hull City':
		outputTeam = 25
	elif inputTeam == 'Middlesbrough':
		outputTeam = 27
	else:
		outputTeam = 99
	return outputTeam


# Return Team Badge
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

# Return Goal Scorer
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
				print (scorer)
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
				print (scorer)
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

# Save Player to the Database. X must be a tuple
def playerSaveDB(x):
	playerStats = []
	playerStats = x

	# Content of X
	# [dateOfMatch, returnTeam(teamSide), side, matchID, playerID, playerPOS, playerJersey, playerName, playerURL, playerShots, playerSOG, playerGoals, playerAssists, playerOffsides, playerFoulsDrawn, playerFoulsCommitted, playerSaves, playerYellowCards, playerRedCards, rosterStatus, playerSubbed, playerSubbedName, playerTimeOn]

	# Assign details from List to local Variables for Function
	dateOfMatch = playerStats[0]
	team = int(playerStats[1])
	side = playerStats[2]
	matchID = int(playerStats[3])
	playerID = int(playerStats[4])
	playerPOS = playerStats[5]
	playerJersey = int(playerStats[6])
	# Sanitize for Apostrephes
	playerName = playerStats[7]
	playerName = playerName.replace("'","\\'")
	# Sanitize for Apostrephes
	playerURL = playerStats[8]
	playerURL = playerURL.replace("'", "\\'")
	playerShots = int(playerStats[9])
	playerSOG = int(playerStats[10])
	playerGoals = int(playerStats[11])
	playerAssists = int(playerStats[12])
	playerOffsides = int(playerStats[13])
	playerFoulsDrawn = int(playerStats[14])
	playerFoulsCommitted = int(playerStats[15])
	playerSaves = int(playerStats[16])
	playerYellowCards = int(playerStats[17])
	playerRedCards = int(playerStats[18])
	rosterStatus = playerStats[19]
	playerSubbed = playerStats[20]
	playerSubbedName = playerStats[21]
	playerSubbedName = playerSubbedName.replace("'", "\\'")
	playerTimeOn = str(playerStats[22])
	playerTimeOn = playerTimeOn.replace("\\"," ")

	cursor = cnx.cursor()
	sqlCheck = ("SELECT ps_matchdate, ps_team, ps_teamSide, ps_matchID, ps_playerID FROM stg_player_stats WHERE ps_matchdate = '%s' AND ps_team = %d AND ps_teamSide = '%s' AND ps_matchID = %s and ps_playerID = %s" % (dateOfMatch, team, side, int(matchID), int(playerID)))
	# print ('The SQL Query is:', sqlCheck)
	# print ('Variables are:', dateOfMatch, str(returnTeam(team)), side, matchID, playerID)
	cursor.execute(sqlCheck)
	results = cursor.fetchone()

	# print (results)
	# print (dateOfMatch)
	cursor.close()

	if results == None:
		cursor = cnx.cursor()
		sqlInsert = ("INSERT INTO stg_player_stats (ps_matchdate, ps_team, ps_teamSide, ps_seasonID, ps_leagueID, ps_matchID, ps_playerID, ps_playerPOS, ps_jerseyNo, ps_playerName, ps_playerURL, ps_Shots, ps_ShotsOnGoal, ps_Goals, ps_Assists, ps_Offsides, ps_FoulsDrawn, ps_FoulsCommitted, ps_Saves, ps_YellowCards, ps_RedCards, ps_rosterStatus, ps_Subbed, ps_SubbedName, ps_TimeOn) VALUES ('%s', %d, '%s', %d, %d, %d, %d, '%s', %d, '%s', '%s', %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, '%s', '%s', '%s', '%s')" % (dateOfMatch, team, side, seasonID, leagueID, matchID, playerID, playerPOS, playerJersey, playerName, playerURL, playerShots, playerSOG, playerGoals, playerAssists, playerOffsides, playerFoulsDrawn, playerFoulsCommitted, playerSaves, playerYellowCards, playerRedCards, rosterStatus, playerSubbed, playerSubbedName, playerTimeOn))
		# print (sqlInsert)
		cursor.execute(sqlInsert)
		cnx.commit()
		# print ('Results Row written for %s' % playerName)

	# else:
		# print ('Record exists for: %s' % playerName)
	cnx.commit()

# Parses out the Squad based upon the parameters given.
def squadParse(x, y, z):
	# Receive a table and parse out the player stats
	squad = x
	# print 'Squad Length is: ' + str(len(squad))
	teamSide = y
	gameDate = z
	maxLength = len(squad)
	# print (len(squad))
	starterCount = 2
	subCount = 16
	if len(squad) == 24:
		subCount = 17
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
		# print (playerPOS)
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
		rosterStatus = 'Starter'
		dateOfMatch = (gameDate[0:4]+'-'+gameDate[4:6]+'-'+gameDate[6:8])
		outputRow = gameDate + '|' + teamSide + '|' + side + '|' + matchID + '|' + playerID + '|' + playerPOS + '|' + playerJersey + '|' + playerName + '|' + '"' + playerURL + '"' + '|' + str(playerShots) + '|' + str(playerSOG) + '|' +  str(playerGoals) \
		      + '|' + str(playerAssists) + '|' + str(playerOffsides) + '|' + str(playerFoulsDrawn) + '|' + str(playerFoulsCommitted) + '|' + str(playerSaves) + '|' + str(playerYellowCards) \
		      + '|' + str(playerRedCards) + '|'+ rosterStatus + '|' + 'N'+ '|' + '|' + '\n' # str(playerPoints) + 
		# print shr
		playerData = 'epl-playerstats-' + ds + '.txt'
		outputPlayerData = os.path.join(outputMatchPath, playerData)
		with open(outputPlayerData, "a") as f:
			f.write(outputRow)
			f.close()
		# print outputRow
		playerRow = [dateOfMatch, returnTeam(teamSide), side, matchID, playerID, playerPOS, playerJersey, playerName, playerURL, playerShots, playerSOG, playerGoals, playerAssists, playerOffsides, playerFoulsDrawn, playerFoulsCommitted, playerSaves, playerYellowCards, playerRedCards, rosterStatus, 'N', '', 0]
		playerSaveDB(playerRow)

		starterCount += 1

	while subCount < maxLength:
		currentRow = squad[subCount]
		# print (currentRow)
		subCount += 1
		playerData = currentRow.find_all("td")
		playerPOS = playerData[0].get_text()
		playerJersey = playerData[1].get_text()
		playerName = playerData[2].get_text(strip=True)
		# print (playerName, playerPOS)
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
		#print (playerURL)
		#if playerURL[] == "-":
		#	print ("Hyphen")
		playerID = playerURL[8:(len(playerURL)-len(playerName)-1)]
		if "/" in playerID:
			playerID = playerID[0:len(playerID)-1]
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
		dateOfMatch = (gameDate[0:4]+'-'+gameDate[4:6]+'-'+gameDate[6:8])
		rosterStatus = 'Bench'
		if playerSubbed != None:
			playerSubbed = 'Y'
		else:
			playerSubbed = 'N'
		dateOfMatch = (gameDate[0:4]+'-'+gameDate[4:6]+'-'+gameDate[6:8])
		outputRow = gameDate + '|' + teamSide +  '|' + side + '|' + matchID + '|' + playerID + '|' + playerPOS + '|' + playerJersey + '|' + playerName + '|' + '"' + playerURL + '"' + '|' + str(playerShots) + '|' + str(playerSOG) + '|' +  str(playerGoals) \
		      + '|' + str(playerAssists) + '|' + str(playerOffsides) + '|' + str(playerFoulsDrawn) + '|' + str(playerFoulsCommitted) + '|' + str(playerSaves) + '|' + str(playerYellowCards) \
		      + '|' + str(playerRedCards) + '|'+ rosterStatus + '|' + playerSubbed + '|' + playerSubbedName + '|' + playerTimeOn + '\n' # str(playerPoints) + '\n'
		# print (outputRow)
		playerData = 'epl-playerstats-' + ds + '.txt'
		outputPlayerData = os.path.join(outputMatchPath, playerData)
		with open(outputPlayerData, "a") as f:
			f.write(outputRow)
			f.close()
		
		playerRow = [dateOfMatch, returnTeam(teamSide), side, matchID, playerID, playerPOS, playerJersey, playerName, playerURL, playerShots, playerSOG, playerGoals, playerAssists, playerOffsides, playerFoulsDrawn, playerFoulsCommitted, playerSaves, playerYellowCards, playerRedCards, rosterStatus, playerSubbed, playerSubbedName, playerTimeOn]
		playerSaveDB(playerRow)
		# print (shr)

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

print (hr)
'''
playerData = 'epl-playerstats-' + ds + '.txt'
outputPlayerData = os.path.join(outputMatchPath, playerData)
with open(outputPlayerData, "w") as f:
			f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
			f.write('FixtureDate|Team|Side|Match ID|Player ID|POS|#|Name|URL|Shots|Shots On Goal|Goals|Assists|Offsides|Fouls Drawn|Fouls Committed|Saves|Yellow Cards|Red Cards|Status|Subbed Player|SubName|TimeOn|Points' + '\n' )
			f.close()

matchURLs = ['http://www.espnfc.us/gamecast/statistics/id/395758/statistics.html', 'http://www.espnfc.us/gamecast/statistics/id/395753/statistics.html']
'''

# URLs for Main Body of Script to work through
fixturesURL = "http://www.bbc.com/sport/football/premier-league/fixtures"
fixturesOpen = requests.get(fixturesURL)
fixturesOpen.raise_for_status()
fixturesSoup = BeautifulSoup(fixturesOpen.text, "html.parser")
print (updateTS() + ' Fixtures Read')
print (shr)

# URLS for Main Body of Script to get Results
resultsURL = "http://www.bbc.com/sport/football/premier-league/results"
resultsOpen = requests.get(resultsURL)
resultsOpen.raise_for_status()
resultsSoup = BeautifulSoup(resultsOpen.text, "html.parser")
print (updateTS() + ' Results Read')
print (shr)

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

# Output Fixtures to the SQL Table HERE
# print (fixturesTable)

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
	matchDates.append(matchesDate)
	counter += 1

print (matchDates)

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

# Creating a Function around the output of the Match Fixtures
def matchOutput(matchRow, outputType):
	# Define the input types. MatchRow = Incoming MatchDates. OutputType = (F)ixtures or (R)esults
	inputMatchRow = matchRow
	inputOutput = outputType
	
for i in matchDates:
    matchDate = i
    matchURL = eplMatchBaseURL + matchDate
    matchOpen = requests.get(matchURL)
    matchSoup = BeautifulSoup(matchOpen.text, "html.parser")
    # matchTXT = 'espn-scores-' + matchDate + '.txt'
    # matchHTML = 'espn-scores-' + matchDate + '.html'
    # outputMatch = os.path.join(outputMatchPath, matchHTML)
    # outputMatchText = os.path.join(outputMatchPath, matchTXT)
    scores = matchSoup.find("div", {"class":"scores"})
    # with open(outputMatch, "w") as f:
    #    f.write(ds + ' :: ' + ts + ' :: ' + parseVersion)
    #    f.write(scores.prettify())
    #     f.close()   
    counter = 0
    # print "Number of Matches is: " + str(len(scores))    
    boxScore = scores.find_all("div", {"class":"score-box"})
    
    # Print out the details for the SQL Insert and Update to the tables
    # print (shr)
    # print (matchURL, matchDate, len(boxScore))
    sqlMatchDate = matchDate[0:4] + '-' + matchDate[4:6] + '-' + matchDate[6:]
    numMatches = len(boxScore)
    sql = ("SELECT seasonID, leagueID, fixtureDate FROM fanfootball.fixtures WHERE seasonID = %s AND leagueID = %s AND fixtureDate = %s" % (seasonID, leagueID, sqlMatchDate))
    insert = ("INSERT INTO fanfootball.fixtures VALUES (%s, %s, '%s', %s, '%s')" % (seasonID, leagueID, sqlMatchDate, numMatches, matchURL))
    # print (insert)

    fixtureCursor = fixtureCnx.cursor()
    try:
    	fixtureCursor.execute(insert)
    	fixtureCnx.commit()
    except:
    	fixtureCnx.rollback()
    
    for i in boxScore:
        # print shr
        # print i
        matchID = i.find("div", {"class":"score full"})
        matchID = str(matchID)
        matchReportID.append(matchID[37:43] + "|" + matchDate)
        # print (matchReportID)
        # print updateTS()
        # print hr
        counter += 1
	

print (hr)

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
	print (shr)
	gameURL = i[9:len(i)]
	gameDate = i[0:8]
	if gameURL == "http://www.espnfc.us/gamecast/statistics/id/395672/statistics.html":
		gameURL = "http://www.espnfc.us/gamecast/statistics/id/395675/statistics.html"
	gameYear = gameDate[0:4]
	gameMonth = gameDate[4:6]
	gameDay = gameDate[6:8]
	print (gameYear + '-' + gameMonth + '-' + gameDay)
	print (gameURL)
	gameHTML = requests.get(gameURL)
	gameHTML.raise_for_status()
	gameSoup = BeautifulSoup(gameHTML.text, "html.parser")	
	matchID = gameURL[44:len(gameURL)-16]
	print ("The Game URL is: " +  gameURL)
	print ("The Match ID is:", matchID, type(matchID))
	print (">>> =================== <<<")

    # Main Container for Game Stats
	gameHeader = gameSoup.find("div", {"class":"container clearfix"})
	gameMatch = gameHeader.find("section", {"class":"match live gamecast-match"})
	homeGoals = 0
	awayGoals = 0
	if gameMatch == None:
		gameMatch = gameHeader.find("section", {"class":"match final gamecast-match"})
		findGameScore = gameSoup.find("div", {"class":"score-time"})
		findGameScore = findGameScore.find("p", {"class":"score"})
		findGameScore = findGameScore.get_text(strip=True)
		dash = " - "
		findDash = findGameScore.find(dash)
		lenGameScore = len(findGameScore)
		homeGoals = findGameScore[0:findDash]
		awayGoals = findGameScore[findDash+3:lenGameScore]
		# Debug to find the value of Home & Away Goals
		# print (str(homeGoals), "::", str(awayGoals))
		# print (findGameScore)
	if gameMatch == None:
		gameStatus = ""
	else: 
		gameStatus = gameMatch.find("p", {"class": "time"})
		gameStatus = gameStatus.get_text(strip=True)
	matchDetails = gameMatch.find("div", {"class":"match-details"})
	stadium = matchDetails.find("p", {"class":"floatright upperCase"})
	stadium = stadium.get_text(strip=True)
	stadium = stadium.replace("'", "\\'")
	attendance = gameHeader.find("div", {"class":"matchup"})
	attendance = attendance.find("p", {"class":"floatleft size-6 normal light"})
	attendance = attendance.get_text(strip=True)
	print (attendance)
	if attendance == '':
		attendance = 'Attendance: 0'
	print (stadium, attendance, 'In Attendance :: Game Status',  gameStatus)
	gameScore = gameSoup.find("div", {"class":"competitors sm-score"})
	print (gameScore)
	
	# Finds Results for team
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
	# print (len(gameStatus))

	if (gameStatus == 'Abandoned'):
		print ('Game was ABANDONED!!')
	elif (gameStatus != 'Postponed'):
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
	print (gameSoup.title.get_text() )
	# print gameURL 
	countDown += 1
	print (shr)
	print ("Games left to parse = %d " % (countArray - countDown))
	print ("Games that have been parsed = %d" % (countDown) )
	print (ds + " :: " + updateTS())

	# Check SQL DB for existence of Record
	sqlCheck = ("SELECT matchID FROM stg_match_details WHERE matchID = %d" % int(matchID))
	cursor = cnx.cursor()
	cursor.execute(sqlCheck)
	results = cursor.fetchone()

	# If Game was Played and Has Not Been Added...
	if results == None and gameStatus != 'Postponed':
		gameScore = gameMatch
		sqlInsert = ("INSERT INTO stg_match_details (matchID, seasonID, homeSide, awaySide, homeScore, awayScore, parseStatus, stadium, attendance, matchURL) VALUES (%d, %d, %d, %d, %d, %d, '%s', '%s', %d, '%s')" % (int(matchID), seasonID, int(returnTeam(homeSide)), int(returnTeam(awaySide)), int(homeGoals), int(awayGoals), 'PLAYED', stadium, int(attendance[12:]), gameURL))
		print ('PLAYED')
		cursor.execute(sqlInsert)
		cnx.commit()
		print ("Row added for Match ID:", matchID)
	elif results == None and gameStatus == 'Postponed':
		sqlInsert = ("INSERT INTO stg_match_details (matchID, seasonID, homeSide, awaySide, homeScore, awayScore, parseStatus, stadium, attendance, matchURL) VALUES (%d, %d, %d, %d, %d, %d, '%s', '%s', %d, '%s')" % (int(matchID), seasonID, int(returnTeam(homeSide)), int(returnTeam(awaySide)), 0, 0, 'PSTPND', stadium, 0, gameURL))
		print ('PSTPND')
		cursor.execute(sqlInsert)
		cnx.commit()
		print ("Row added for Match ID:", matchID)
	else:
		print ("Game Previously Added!")
	cursor.close()
	print (hr)

def teamNews(x):
	teamURL = x
	teamName = x
	teamName = teamName[6:len(teamName)-10]
	teamURL = prefixESPN + teamURL
	teamHTML = requests.get(teamURL)
	teamHTML.raise_for_status()
	teamSoup = BeautifulSoup(teamHTML.text, "html.parser")	
	recentNews = teamSoup.find("div", {"id":"feed"})
	recentNewsItems = recentNews.find_all("div", {"class":"feed-item-content"})
	recapOutput = []
	print ("Team News Parsed :: " + teamName)
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
	print (hr )
	return recapOutput

'''
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
'''

# Commit and Close the Database Connection.
fixtureCnx.commit()
fixtureCnx.close()

cnx.commit()
cnx.close()
print ('MySQL Connection Closed')

'''
# See why this is erroring out in the Program
for i in teamURLs:
	for x in teamNews(i):
		with open(teamNewstxt, "a") as f:
			f.write(x + '\n')
			f.close()
'''