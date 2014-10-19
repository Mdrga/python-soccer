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
eplURL = 'http://www.espnfc.us/gamecast/statistics/id/395758/statistics.html'
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

print hr
print eplURL + ' | ' + eplSoup.title.get_text() 
print hr

#  <div class="container clearfix" id="content-wrap">
header = eplSoup.find("div", {"class":"container clearfix"})

# <section class="match final gamecast-match" id="matchcenter-395758">
gameMatch = header.find("section", {"class":"match final gamecast-match"})
reportHomeTeam = gameMatch.find("div", {"class":"team home"})
reportAwayTeam = gameMatch.find("div", {"class":"team away"})

# Return Team Name or Team URL
def teamName (x, y, z):
	passHTML = x
	outputOption = y
	teamSide = z
	returnOutput = ''

	if teamSide == 'H':
		if outputOption == 'N': 
			passHTML = passHTML.find("p", {"class":"team-name floatleft"})
			passHTML = passHTML.get_text(strip=True)
			returnOutput = passHTML
		elif outputOption == 'U':
			passHTML = passHTML.find("a")
			passHTML = passHTML["href"]
			returnOutput = passHTML
	else:
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
	if teamSide == 'H':
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
	elif teamSide == 'A':
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

print homeSide + '|' + homeURL + '|' + homeBadge
print shr
print goalScorer(reportHomeTeam, 'H')
print hr
print awaySide + '|' + awayURL + '|' + awayBadge
print shr
print goalScorer(reportAwayTeam, 'A')
print hr

matchSummary = header.find("section", {"class":"mod-container gc-stat-list"})
matchStats = matchSummary.find_all("ul")
for i in matchStats:
	matchDetail = i.find_all("li")
	for i in matchDetail:
		print i
	print shr
# print matchStats

''''
homeTeamBadge = homeTeam.find("img")
homeTeamBadge = homeTeamBadge["src"]
homeTeamBadge = homeTeamBadge[0:len(homeTeamBadge[0:len(homeTeamBadge)-5])]
outputHomeTeamBadge = outputImgsPath + homeTeam + '.png'	
print outputHomeTeamBadge
'''