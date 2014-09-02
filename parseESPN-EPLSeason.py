# -*- coding: utf-8 -*-
'''
Created on Aug 28, 2014
Modified on Aug 28, 2014
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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")

# Set Base EPL Link for ESPN
eplURL = 'http://www.espnfc.us/barclays-premier-league/23/index'
eplHTML = urllib2.urlopen(eplURL)
eplSoup = BeautifulSoup(eplHTML)

# print eplSoup.prettify()

# Program Version & System Variables
parseVersion = 'ESPN Premier League v0.01.a'
outputPath = 'PL-Data/'
outputImgsPath = 'PL-Data/imgs/'
outputMatchPath = 'PL-Data/match/'
hr = " >>> *** ====================================================== *** <<<"

# Output a local copy of the FULL ESPN page to the local drive
outputBase = 'ESPN-EPL-MatchBase.html'
outputBase = os.path.join(outputPath, outputBase)
with open(outputBase, "w") as f:
     f.write(eplSoup.prettify("utf-8"))
     f.close()
     
#  <div class="scroll-area columns-5">
teamList = eplSoup.find_all("div", {"class":"scroll-area columns-5"})

# Page Navigational Elements
pageNav = 'espn-pagenav.html'
outputPageNav = os.path.join(outputPath, pageNav)

with open (outputPageNav, "w") as fi:
    fi.write(ds + ' :: ' + ts + ' :: Page Nav ' + parseVersion + '\n')
    fi.close()

for i in teamList:    
    with open(outputPageNav, "a") as f:
        f.write(i.prettify())
        f.write(hr)
        f.write('\n')
        f.close() 

# http://www.espnfc.us/barclays-premier-league/23/scores?date=20140816
eplMatchesURL = "http://www.espnfc.us/barclays-premier-league/23/scores?date=20140816"
eplMatchBaseURL = "http://www.espnfc.us/barclays-premier-league/23/scores?date="
matchDateArray = ['20140816']# ,'20140817','20140818','20140823','20140824','20140825','20140830','20140831'] #,'20140830']
matchReportURL = []
matchReportID = []

for i in matchDateArray:
    matchDate = i
    matchURL = eplMatchBaseURL + matchDate
    matchOpen = urllib2.urlopen(matchURL)
    matchSoup = BeautifulSoup(matchOpen)
    matchTXT = 'espn-scores-' + matchDate + '.txt'
    matchHTML = 'espn-scores-' + matchDate + '.html'
    outputMatch = os.path.join(outputMatchPath, matchHTML)
    # outputMatchText = os.path.join(outputMatchPath, matchTXT)
    scores = matchSoup.find("div", {"class":"scores"})
    with open(outputMatch, "w") as f:
        f.write(scores.prettify())
        f.close()   
    # with open(outputMatchText, "w") as f:
    #    f.write(ds + ' :: ' + ts + ' :: ' + parseVersion)
    #    f.close()
    counter = 0
    print len(scores)    
    boxScore = scores.find_all("div", {"class":"score-box"})
    for i in boxScore:
        print hr
        # print i
        
        # This will need to become a function and be called for each element of i
        # Find the Match ID from ESPN
        matchID = i.find("div", {"class":"score complete full"})

        # For Completed Match this will work. For Upcoming Matches, the second portion works.
        try:
            matchID
        except NameError:
            matchID = i.find("div", {"class":"score upcoming full"})
        
        if matchID == None:
            matchID = i.find("div", {"class":"score upcoming full"})
            matchReportID.append(matchID['data-gameid'])
            print matchDate + ' ' + matchID['data-gameid']
        else:
            print matchDate + ' ' + matchID['data-gameid']
            matchReportID.append(matchID['data-gameid'])
        
        # Find Teams & Score for the Match
        matchTeams = i.find_all("div", {"class":"team-name"})
        matchScore = i.find_all("div", {"class":"team-score"})
        matchCount = 0
        
        # Match Info
        gameInfo = i.find("div", {"class":"game-info"})
        gameURL = i.find("a")
        for i in matchTeams:
            team = i.get_text(strip=True)
            teamScore = matchScore[matchCount]
            teamScore = teamScore.get_text(strip=True)
            teamSpan = i.find("span")
            teamImg = teamSpan.find("img")
            # print "*** ======== ***"
            # print team + ' ' + teamScore
            # print teamImg["src"]
            matchCount +=1 
        
        # Find Match Scores
        # print "*** ======== ***"
        matchDuration = gameInfo.get_text(strip=True)
        matchReportURL.append(gameURL["href"])
        # print gameURL["href"]
        print hr
        counter += 1
    
'''for i in matchReportURL:
    reportURL = i
    # print reportURL
    reportOpen = urllib2.urlopen(reportURL)
    reportSoup = BeautifulSoup(reportOpen)
    reportHTML = reportSoup.title.get_text(strip=True)
    print reportHTML
    
    # http://www.espnfc.us/gamecast/statistics/id/395758/statistics.html
'''
matchPrefix = 'http://www.espnfc.us/gamecast/statistics/id/'
matchSuffix = '/statistics.html'

print matchReportID[0]

for i in matchReportID:    
    reportURL = matchPrefix + i + matchSuffix
    matchID = i
    # http://www.espnfc.us/gamecast/statistics/id/395758/statistics.html    
    print reportURL
    reportOpen = urllib2.urlopen(reportURL)
    reportSoup = BeautifulSoup(reportOpen)
    reportTXT = 'espn-scores-' + i + '.txt'
    outputReportText = os.path.join(outputMatchPath, reportTXT)
    #with open(outputReportText, "w") as f:
    #    f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
    #    f.write(reportSoup.prettify())
    #    f.write('\n' + hr + '\n')
    #    f.close()
    reportTitle = reportSoup.find("title")
    reportSummary = reportSoup.find_all("section", {"class":"match final gamecast-match"})
    # Summary of Match Stats
    reportMatchSummary = reportSoup.find_all("section", {"class":"mod-container gc-stat-list"})
    reportHomeTeam = reportSoup.find("div", {"class":"team home"})
    reportAwayTeam = reportSoup.find("div", {"class":"team away"})
    reportPlayerDetails = reportSoup.find_all("div", {"class":"span-12 column"})
    reportDetails = reportSoup.find_all("div", {"class":"match-details"})
    # print reportTitle.get_text()
    # print reportHomeTeam
    # print hr
    # print reportAwayTeam
    # print hr
    playerTXT = 'espn-players' + i + '.txt'
    outputPlayerText = os.path.join(outputMatchPath, playerTXT)
    with open(outputPlayerText, "w") as f:
         f.write(ds + ' :: ' + ts + ' :: Player Parser :: ' + parseVersion + '\n')
         f.write(hr + '\n')
         # f.write(reportPlayerDetails)
         f.close()
    
    # for i in reportMatchSummary:
        # print hr
        # print i
        # print hr
    for i in reportPlayerDetails:
        teamTable = i.find_all("section")
        for i in teamTable:
            homeSide = i.find("h1", {"id":"home-team"})
            awaySide = i.find("h1", {"id":"away-team"})
            print homeSide
            print awaySide
            playerTable = i.find_all("table")
            #print len(playerTable)
            # print playerTable
        with open(outputPlayerText, "a") as f:
            f.write(i.prettify())
            f.close()
                
                                
        '''
        with open(outputPlayerText, "a") as f:
            f.write(playerTable.prettify())
            f.close()
        
        playerRow = playerTable.find_all("tr")
        for i in playerRow:
            # playerRow = i.find("th", {"class":"pstat-pos"})
            # with open(outputPlayerText, "a") as f:
                # f.write(i.prettify())
                # f.write(hr + '\n')
                # f.close()
            playerDetails = i.find_all("td")
            # print len(playerDetails)
            if len(playerDetails) >=13:
                playerPos = playerDetails[0]
                playerPos = playerPos.get_text(strip=True)
                playerJersey = playerDetails[1]
                playerJersey = playerJersey.get_text(strip=True)
                playerName = playerDetails[2]
                playerLink = playerName.find("a")
                playerLink = playerLink["href"]
                playerID = playerLink[8:14]
                playerName = playerName.get_text(strip=True)
                playerShots = playerDetails[3]
                playerShots = playerShots.get_text(strip=True)
                playerShotsOnGoal = playerDetails[4]
                playerShotsOnGoal = playerShotsOnGoal.get_text(strip=True)
                playerGoals = playerDetails[5]
                playerGoals = playerGoals.get_text(strip=True)
                playerAssists = playerDetails[6]
                playerAssists = playerAssists.get_text(strip=True)
                playerOffsides = playerDetails[7]
                playerFoulsDrawn = playerDetails[8]
                playerFoulsCommitted = playerDetails[9]
                playerSaves = playerDetails[10]
                playerYellowCards= playerDetails[11]
                playerRedCards = playerDetails[12]
                # print playerPos
                with open(outputPlayerText, "a") as f:
                    f.write(matchID + "|" + playerID +'|' + playerPos + "|" + playerJersey + "|" + playerName + "|" + playerLink + "|" + playerShots +"|"+ \
                    playerShotsOnGoal +"|"+ playerGoals +"|" +                     playerAssists + '\n')
                    # f.write(hr + '\n')
                    f.close()
            try:
                playerRow
            except NameError:
                playerRow = None
                print "NOT A PLAYER ROW!"
            if playerRow != None:
                playerPos = i.find("th", {"class":"pstat-pos"})
                playerPos = playerPos.get_text(strip=True)
                playerJerseyNo = i.find("th", {"class":"pstat-no"})
                playerJerserNo = playerJerseyNo.get_text(strip=True)
                with open(outputPlayerText, "a") as f:
                   f.write(playerPos + '|' + playerJerseyNo)
                   f.close()
            # print i
        
    '''    
        
    # <div class="match-details">    
    # for i in reportDetails:
    # with open(outputReportText, "a") as f:
    #    f.write(reportDetails)
    #    f.write(hr + '\n')
    #    f.close
    
''' 
    try:
        specNotice
    except NameError:
        specNotice = None

    if specNotice != None:
        matchNotice = "DRAW" + ' - ' + specNotice.get_text(strip=True)
    else:
        matchNotice = "No Special Notice"
'''
