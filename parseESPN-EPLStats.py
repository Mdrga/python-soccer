# -*- coding: utf-8 -*-
'''
Created on Oct 19, 2014
Modified on Oct 19, 2014
Version 0.01.a
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
siteBasePath = "http://www.espnfc.us"

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
parseVersion = 'ESPN Premier League Match Stats v0.01.a'
print date + ' :: ' + ts + ' :: ' + parseVersion

# Set Base EPL Link for ESPN
eplURL = 'http://www.espnfc.us/gamecast/statistics/id/395758/statistics.html' # 'http://www.espnfc.us/gamecast/statistics/id/395753/statistics.html' # 
eplHTML = urllib2.urlopen(eplURL)
eplSoup = BeautifulSoup(eplHTML)

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

# Output a local copy of the FULL ESPN page to the local drive
outputBase = 'ESPN-EPL-MatchBase.html'
outputBase = os.path.join(outputPath, outputBase)
with open(outputBase, "w") as f:
     f.write(eplSoup.prettify("utf-8"))
     f.close()

#  <div class="container clearfix" id="content-wrap">
header = eplSoup.find("div", {"class":"container clearfix"})

# <section class="match final gamecast-match" id="matchcenter-395758">
gameMatch = header.find("section", {"class":"match final gamecast-match"})
reportAwayTeam = gameMatch.find("div", {"class":"team home"})
reportHomeTeam = gameMatch.find("div", {"class":"team away"})

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

homeSide = teamName(reportHomeTeam, 'N', 'H')
homeURL =  siteBasePath + teamName(reportHomeTeam, 'U', 'H')
homeBadge = teamBadge(reportHomeTeam, 'H')
awaySide = teamName(reportAwayTeam, 'N', 'A')
awayURL = siteBasePath + teamName(reportAwayTeam, 'U', 'H')
awayBadge = teamBadge(reportAwayTeam, 'A')

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

matchSummary = header.find("section", {"class":"mod-container gc-stat-list"})
matchStats = matchSummary.find_all("ul")
rsCounter = 0

playerSummary = header.find("div", {"class":"span-12 column"})

# print matchStats

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
matchID = eplURL[44:len(eplURL)-16]
print hr
print eplSoup.title.get_text() 
print eplURL 
print hr

# print len(goalScorer(reportHomeTeam, 'H'))
# print len(goalScorer(reportAwayTeam, 'A'))
# print homeSide + '|' + homeURL + '|' + homeBadge + '|' 
# print awaySide + '|' + awayURL + '|' + awayBadge + '|' 
# print hr

#print "Team Name|Total Shots|Shots On Goal|Tackles|Fouls"
#print homeSide + '|' + teamStats(matchStats, 'H', 0) + '|' + teamStats(matchStats, 'H', 1) + '|' + teamStats(matchStats, 'H', 2) + '|' + teamStats(matchStats, 'H', 3)
#print awaySide + '|' + teamStats(matchStats, 'A', 0) + '|' + teamStats(matchStats, 'A', 1) + '|' + teamStats(matchStats, 'A', 2) + '|' + teamStats(matchStats, 'A', 3)
#print hr
# print matchStats
# print playerSummary
# print playerSummary.prettify()
playerStats = playerSummary.find_all("table")
homeStats = playerStats[0]
homePlayers = homeStats.find_all("tr")
awayStats = playerStats[1]
awayPlayers = awayStats.find_all("tr")


def statParse(x):
	statResult = x
	if statResult == '-':
		statResult = 0

	return statResult

def squadParse(x, y):
	# Receive a table and parse out the player stats
	squad = x
	teamSide = y
	starterCount = 2
	subCount = 16
	if teamSide == 'A':
		teamSide = awaySide
	elif teamSide == 'H':
		teamSide = homeSide
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
		playerOffsides = statParse(playerData[7].get_text(strip=True))
		playerFoulsDrawn = statParse(playerData[8].get_text(strip=True))
		playerFoulsCommitted = statParse(playerData[9].get_text(strip=True))
		playerSaves = statParse(playerData[10].get_text(strip=True))
		playerYellowCards = statParse(playerData[11].get_text(strip=True))
		playerRedCards = statParse(playerData[12].get_text(strip=True))
		outputRow = teamSide + '|' + matchID + '|' + playerID + '|' + playerPOS + '|' + playerJersey + '|' + playerName + '|' + '"' + playerURL + '"' + '|' + str(playerShots) + '|' + str(playerSOG) + '|' +  str(playerGoals) \
		      + '|' + str(playerAssists) + '|' + str(playerOffsides) + '|' + str(playerFoulsDrawn) + '|' + str(playerFoulsCommitted) + '|' + str(playerSaves) + '|' + str(playerYellowCards) \
		      + '|' + str(playerRedCards) + '|Starter|' + 'N'
		# print shr
		print outputRow
		starterCount += 1
	while subCount < 23:
		currentRow = squad[subCount]
		subCount += 1
		playerData = currentRow.find_all("td")
		playerPOS = playerData[0].get_text()
		playerJersey = playerData[1].get_text()
		playerName = playerData[2].get_text(strip=True)
		playerURL = playerData[2].find("a")
		playerURL = playerURL["href"]
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
		outputRow = teamSide + '|' + matchID + '|' + playerID + '|' + playerPOS + '|' + playerJersey + '|' + playerName + '|' + '"' + playerURL + '"' + '|' + str(playerShots) + '|' + str(playerSOG) + '|' +  str(playerGoals) \
		      + '|' + str(playerAssists) + '|' + str(playerOffsides) + '|' + str(playerFoulsDrawn) + '|' + str(playerFoulsCommitted) + '|' + str(playerSaves) + '|' + str(playerYellowCards) \
		      + '|' + str(playerRedCards) + '|Bench|' + playerSubbed
		print outputRow

playerTXT = matchID + '.txt'
#outputPlayerText = os.path.join(outputMatchPath, playerTXT)
#	with open(outputPlayerText, "w") as f:
#        f.write(ds + ' :: ' + updateTS() + ' :: Player Parser :: ' + parseVersion + '\n')
#         f.write(hr + '\n')
         # f.write(reportPlayerDetails)
#         f.close()
   

print 'Tean|Match ID|Player ID|POS|#|Name|Shots|Shots On Goal|Goals|Assists|Offsides|Fouls Drawn|Fouls Committed|Saves|Yellow Cards|Red Cards|Status|Subbed In?'
squadParse(homePlayers, 'H')
print hr
squadParse(awayPlayers, 'A')

