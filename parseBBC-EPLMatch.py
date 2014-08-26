# -*- coding: utf-8 -*-
'''
Created on Jun 16, 2014
Modified on Aug 24, 2014
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

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")

# Create an array of URL Links.
website = ["http://www.bbc.com/sport/football/27961190","http://www.bbc.com/sport/0/football/28102403","http://www.bbc.com/sport/football/25285249", "http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/premier-league/results", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Parse out Specific Match Results
matchResults = urllib2.urlopen(website[5])
gameURL = website[1]
gameMatch = urllib2.urlopen(gameURL)
resultSoup = BeautifulSoup(matchResults)
matchSoup = BeautifulSoup(gameMatch)

# Program Version
parseVersion = 'Premier League v0.13.i'
outputPath = 'PL-Data/'
outputImgsPath = 'PL-Data/imgs/'
outputMatchPath = 'PL-Data/match/'

outputBase = 'EPL-MatchBase.html'
outputBase = os.path.join(outputMatchPath, outputBase)
with open(outputBase, "w") as f:
     f.write(matchSoup.prettify("utf-8"))
     f.close()

# Identify Team Lineup
divDetailResults = matchSoup.find_all("div", {"class":"team-match-details"})
divLineup = matchSoup.find("div", {"id":"oppm-team-list"})

# Function to return the Home Team Name using the divTeamDetails
def returnHome(x):
    homeTeam = x.find("div", {"id":"home-team"})
    spanHomeTeam = homeTeam.find("span", {"class":"team-name"})
    return spanHomeTeam.get_text()

# Function to return the Away Team Name using the divTeamDetails
def returnAway(x):
    awayTeam = x.find("div", {"id":"away-team"})
    spanAwayTeam = awayTeam.find("span", {"class":"team-name"})
    return spanAwayTeam.get_text()

# Function to return the Roster & Lineup of the squads
# TODO - Use the value of the Start / Substitue in the Roster coming in
def rosterOutput(x):
    rosterArray = []
    counter = 1
    for i in x:
        print i.encode('utf-8')
        lineup = i.find_all("li")
        teamName = i.find("h3")

        # print i
        for i in lineup:
            playerJersey = i.text[3:5]
            playerDetails =  i.text[7:len(i.text)]
            playerDetails.encode('utf-8')
            playerStart = playerDetails.find("  ")
            playerString = len(playerDetails) 
        if len(playerDetails) - playerStart > 2:
           playerName = i.text[7:(len(i.text)-(len(playerDetails) - playerStart))]
           # print playerName
           playerUpdate = i.text[7+len(playerName):7+playerString]
           playerUpdateRow = teamName.get_text()+ '|' + playerJersey + '|' + playerName + '|' + startingLineup(counter) + '|' + playerUpdate 
           #print playerUpdateRow
           counter += 1
           rosterArray.append(playerUpdateRow.encode('utf-8'))
        else:
           playerRow = teamName.get_text() + '|' + playerJersey + '|' + playerDetails[0:len(playerDetails)-2] + '|' + startingLineup(counter) + '|'
           #print playerRow
           counter += 1
           rosterArray.append(playerRow.encode('utf-8'))
    return rosterArray

# Team Match Details & Team Badge
divTeamDetails = matchSoup.find("div", {"class":"post-match"})

# Initialize the Stats File
outputMatch = "MatchStats-output.txt"
outputMatch = os.path.join(outputMatchPath, outputMatch)
with open(outputMatch, "w") as f:
    f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '|' + 'Match Stats File' + '\n')
    f.write('MatchID' + '|' + 'Team Side' + '|' + 'Team Name' + '|' + 'Goals Scored' + '|' + 'Team Badge' + '|' + 'Possession %' + '|' + 'Shots' + '|' + 'Shots On Goal' + '|' + 'Corners' + '|' + 'Fouls' + '|' + 'Match Notice' + '\n')
    f.close()

# Get the Home Team from the URL
# Paramaters are as follows:
# x = BeautifulSoup(URL)
# y = Output Format
# z = 'H'ome or 'A'way Team
def teamName (x,y,z):
    funcMatch = x
    formatType = y
    returnName = z
    returnArray = []
    returnString = ''
    divTeamDetails = funcMatch.find("div", {"class":"post-match"})
    homeTeam = divTeamDetails.find("div", {"id":"home-team"})
    awayTeam = divTeamDetails.find("div", {"id":"away-team"})
    if formatType == 0:
        returnArray.append(homeTeam.a.get_text())
        returnArray.append(awayTeam.a.get_text())
    elif formatType == 1:
        returnArray.append(homeTeam)
        returnArray.append(awayTeam)
    else:
        returnArray = []
        returnString = 'Some Other Format'
    if returnName == 'H':
        returnString = returnArray[0]
    elif returnName == 'A':
        returnString = returnArray[1]
    else:
        returnString = returnString + ' Also you did not pick a team'

    return returnString 

def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print 'Downloading %s...' % (localFileName)
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True
    
# Function to return Match Stats based on input of matchSoup
# Paramaters are as follows:
# x = BeautifulSoup(gameURL)
# y = gameURL
# z = 'H'ome, 'A'way or 'B'oth
def matchStats(x,y,z):
    # Pull in the main Match Detail page from the Function Call
    funcMatch = x

    # Parse Game URL into segments. Will be using the last portions to create a unique BBC_MatchID 
    strGameURL = y.split('/')
    BBC_MatchID = strGameURL[5]
    
    # Define the Output Format for the Match Stats
    outputFormat = z

    # Create a local copy of the Match HTML page
    matchStats = BBC_MatchID + '.html'
    matchStats = os.path.join(outputMatchPath, matchStats)
    with open (matchStats, "w") as f:
        f.write(funcMatch.prettify('utf-8'))
        f.close()

    # Parse out the two main sections of the Match (Roster & Stats)
    divTeamDetails = funcMatch.find("div", {"class":"post-match"})
    divMatchStats = funcMatch.find("div", {"id":"match-stats-wrapper"})

    # Parse out the Match Statistics
    statPossession = divMatchStats.find("div", {"id":"possession"})
    statShots = divMatchStats.find("div", {"id":"total-shots"})
    statShotsGoal = divMatchStats.find("div", {"id":"shots-on-target"})
    statCorners = divMatchStats.find("div", {"id":"corners-wrapper"})
    statFouls = divMatchStats.find("div", {"id":"fouls-wrapper"})
    statPossessionHome = statPossession.find("span", {"class":"home"})
    statPossessionAway = statPossession.find("span", {"class":"away"})
    statShotsHome = statShots.find("span", {"class":"home"})
    statShotsAway = statShots.find("span", {"class":"away"})
    statShotsGoalHome = statShotsGoal.find("span", {"class":"home"})
    statShotsGoalAway = statShotsGoal.find("span", {"class":"away"})
    statCornersHome = statCorners.find("span", {"class":"home"})
    statCornersAway = statCorners.find("span", {"class":"away"})
    statFoulsHome = statFouls.find("span", {"class":"home"})
    statFoulsAway = statFouls.find("span", {"class":"away"})

    # Parse out the Team Names, Team Badge, Scores and Scorers of Goals
    homeTeam = divTeamDetails.find("div", {"id":"home-team"})
    awayTeam = divTeamDetails.find("div", {"id":"away-team"})
    homeScorer = homeTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
    print homeScorer
    awayScorer = awayTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
    print awayScorer
    spanHomeScore = homeTeam.find("span", {"class":"team-score"})
    spanAwayScore = awayTeam.find("span", {"class":"team-score"})
    homeTeamBadge = homeTeam.find("img")
    awayTeamBadge = awayTeam.find("img")

    # Download Badge from Site
    homeBadgeURL = homeTeamBadge["src"]
    homeBadgeFile = homeBadgeURL[64:len(homeBadgeURL)]
    homeBadge = os.path.join(outputImgsPath, homeBadgeFile)
    downloadImage(homeBadgeURL, homeBadge)
    awayBadgeURL = awayTeamBadge["src"]
    awayBadgeFile = awayBadgeURL[64:len(awayBadgeURL)]
    awayBadge = os.path.join(outputImgsPath, awayBadgeFile)
    downloadImage(awayBadgeURL, awayBadge)
    
    # Create an array to store the Team-Level Statistics that will be returned
    teamStats = []

    # Advice of Winner in event of a Penalty Shoot Out
    specNotice = funcMatch.find("div", {"id":"special-notice"})
    try:
        specNotice
    except NameError:
        specNotice = None

    if specNotice != None:
        matchNotice = "DRAW" + ' - ' + specNotice.get_text(strip=True)
    else:
        matchNotice = "No Special Notice"

    # print spanHomeScorer
    # print homeTeam.prettify('utf-8')
    # for i in homeTeam.p:
    #    print i

    #print homeScorer
    #print awayScorer

    # Define the Function Output to the Array teamStats
    if outputFormat == 'H':
        teamStats.append(BBC_MatchID + '|' + 'Home' + '|' + homeTeam.a.get_text() + '|' + spanHomeScore.get_text() + '|' + homeTeamBadge["src"] + '|' + statPossessionHome.get_text() + \
        '|' + statShotsHome.get_text() + '|' + statShotsGoalHome.get_text() + '|' + statCornersHome.get_text() + '|' + statFoulsHome.get_text() + '|' + matchNotice)
    elif outputFormat == 'A':
        teamStats.append(BBC_MatchID + '|' + 'Away' + '|' + awayTeam.a.get_text() + '|' + spanAwayScore.get_text() + '|' + awayTeamBadge["src"] + '|' + statPossessionAway.get_text() + \
        '|' + statShotsAway.get_text() + '|' + statShotsGoalAway.get_text() + '|' + statCornersAway.get_text() + '|'+ statFoulsAway.get_text() + '|' + matchNotice)
    elif outputFormat == 'B':
        teamStats.append(BBC_MatchID + '|' + 'Home' + '|' + homeTeam.a.get_text() + '|' + spanHomeScore.get_text() + '|' + homeTeamBadge["src"] + '|' + statPossessionHome.get_text() + \
        '|' + statShotsHome.get_text() + '|' + statShotsGoalHome.get_text() + '|' + statCornersHome.get_text() + '|' + statFoulsHome.get_text() + '|' + matchNotice)
        teamStats.append(BBC_MatchID + '|' + 'Away' + '|' + awayTeam.a.get_text() + '|' + spanAwayScore.get_text() + '|' + awayTeamBadge["src"] + '|' + statPossessionAway.get_text() + \
        '|' + statShotsAway.get_text() + '|' + statShotsGoalAway.get_text() + '|' + statCornersAway.get_text() + '|'+ statFoulsAway.get_text() + '|' + matchNotice)
    else:
        teamStats.append('INCORRECT OUTPUT FORMAT SELECTED')

    return teamStats

# Initialize the Player Stats File
playerStats = 'PlayerStats-output.txt'
playerStats = os.path.join(outputMatchPath, playerStats)
with open(playerStats, 'w') as f:
    f.write(ds + ' :: ' + ts + ' :: ' + 'Premier League Player Output ' + parseVersion + '\n' + '\n')
    f.write('Match ID|Team Side|Country|Player Name|Player ID|Bench Status|Jersey #|Incident|Booked|Dismissed|Substituted|' + '\n')
    f.close()

# Function to return the Individual Team Members
# Parameters are as follows:
# x = BeautifulSoup(SomeURL)
# y = SomeURL
# z = Return Roster Type 'H'ome or 'A'way
def outputRosters(x,y,z):
    # Incoming Game to Return Results Upon
    funcMatch = x
    
    #URL to identify the Match
    strGameURL = y.split('/')
    BBC_MatchID = strGameURL[5]

    # Format Return Type
    returnType = z

    # The Match Details
    divLineup = funcMatch.find("div", {"id":"oppm-team-list"})
    
    # Setting up the necessary Variables for the function
    if returnType == 'H':
        listRoster = divLineup.find("div", {"class":"home-team"})
        listStarter = listRoster.find("ul", {"class":"player-list"})
        listSubs = listRoster.find("ul", {"class":"subs-list"})
        lineupStarter = listStarter.find_all("li")
        lineupSubs = listSubs.find_all("li")
        teamSide = 'Home'
    elif returnType == 'A':
        listRoster = divLineup.find("div", {"class":"away-team"})
        listStarter = listRoster.find("ul", {"class":"player-list"})
        listSubs = listRoster.find("ul", {"class":"subs-list"})
        lineupStarter = listStarter.find_all("li")
        lineupSubs = listSubs.find_all("li")
        teamSide = 'Away'
    else: 
        print 'BAD RETURN TYPE INDICATED'
        listRoster = []
        listStarter = []
        listSubs = []
        lineupStarter = []
        lineupSubs = []

    # print "*** - - - - - - - - - - - - - - - - - - ***"
    # print 'Player Name|Country|Bench Status|Jersey #|Incident|Booked|Dismissed|Substituted|'
    teamRoster = []

    # Creates the Player Lineup for the incoming Match
    for i in lineupStarter:
        i.encode('utf-8')
        playerID = i.span["id"]
        playerID = playerID[10:len(playerID)]
        playerJersey = i.text[3:5]
        playerDetails =  i.text[7:len(i.text)]
        playerStart = playerDetails.find("  ")
        playerString = len(playerDetails) 
        playerName = i.text[7:(len(i.text)-(len(playerDetails) - playerStart))]
        playerUpdate = i.text[7+len(playerName):7+playerString]
        # print len(playerUpdate)
        if len(playerUpdate) > 2: 
            # print playerUpdate
            playerIncident = 'Y'
            playerBooked = playerUpdate.find("Booked")
            playerDismissed = playerUpdate.find("Dismissed")
            playerSub = playerUpdate.find("(")
            # print playerName.encode('utf-8') + ' Red Card ' + str(playerDismissed)
            if playerDismissed > 0:
                playerDismissed = 'Y'
            else:
                playerDismissed = 'N'
            # print playerSub
            if playerBooked > 0:
                playerBooked = 'Y'
            else:
                playerBooked = 'N'
            if playerSub > 0:
                playerSub = playerUpdate[playerSub + 1:len(playerUpdate) - 4]
            else:
                playerSub = ''
        else:
            playerIncident = 'N'
            playerDismissed = 'N'
            playerUpdate = 'N'
            playerBooked = 'N'
            playerSub = 'N'
        
        
        teamRoster.append(BBC_MatchID + '|' + teamSide + '|' + teamName(funcMatch,0,returnType) +  '|' + playerName + '|' + playerID + '|Starter|' + \
        playerJersey + '|' + playerIncident + '|' + playerBooked + '|' + playerDismissed + '|' + playerSub + '|')

    for i in lineupSubs:
        # print i
        i.encode('utf-8')
        playerID = i.span["id"]
        playerID = playerID[10:len(playerID)]
        playerJersey = i.text[3:5]
        playerDetails =  i.text[7:len(i.text)]
        playerStart = playerDetails.find("  ")
        playerName = i.text[7:(len(i.text)-(len(playerDetails) - playerStart))]

        teamRoster.append(BBC_MatchID + '|' + teamSide + '|' + teamName(funcMatch,0,returnType) + '|' + playerName + '|' + playerID + '|Bench|' + playerJersey + '|||||')

    #for i in teamRoster:
    #    print i.encode('utf-8')

    return teamRoster

# Output Game URLs from Results page resultSoup
def resultsURL(x):
    listURL = []
    funcSoup = x
    divMatchResults = funcSoup.find_all("div", {"class":"fixtures-table full-table-medium"})
    for i in divMatchResults:
        urlList = i.find_all('a', {'class': 'report'})
        for i in urlList:
            listURL.append("http://www.bbc.com" + i.get("href"))

    return listURL

# Function to return the Goal Scorers for a Match
# Parameters are as follows:
# x = BeautifulSoup(SomeURL)
# y = SomeURL
# z = Return Roster Type 'H'ome or 'A'way
def goalScorer(x,y,z):
    # Incoming Game to Return Results Upon
    funcMatch = x
    
    #URL to identify the Match
    strGameURL = y.split('/')
    BBC_MatchID = strGameURL[5]

    # Designate the output type for the Match in Qestion
    returnType = z

    # Comment
    #<div class="story blq-clearfix" id="main-content">
    gameDetails = funcMatch.find("div", {"id":"main-content"})

    # Output Array
    scorerArray = []

    # For Home
    if returnType == 'H':
        team = gameDetails.find("div", {"id":"home-team"})
    if returnType == 'A':
        team = gameDetails.find("div", {"id":"away-team"})
        #print homeTeam.prettify('utf-8')
        
    teamScore = team.find("span", {"class":"team-score"})
    if teamScore.get_text() > 0:
        for i in teamScore:
            goalScorer = team.find("p", {"class":"scorer-list blq-clearfix"})
            # print goalScorer
            # print goalScorer.prettify('utf-8')
            try:
                goalScorer
            except NameError:
                goalScorer = None

            if goalScorer != None:
                textGoalScorer = goalScorer.find_all("span")
                for i in textGoalScorer:
                    textScorer = (i.text).encode('utf-8')
                    scorerArray.append(textScorer)
    else:
        scorerArray = []

        # <div class="team" id="home-team">

    return scorerArray

# Output tests run below this line
print '***- - - - - - - - - - - - - - - - -***'
# outputRosters(matchSoup, 'A')
print datetime.datetime.now().strftime("%H:%M:%S")

urlArray = resultsURL(resultSoup)

print len(urlArray)
print '***- - - - - - - - - - - - - - - - -***'

for i in urlArray:
    parseURL = i # "http://www.bbc.com/sport/football/25285106"
    parseMatch = urllib2.urlopen(parseURL)
    parseSoup = BeautifulSoup(parseMatch)
    parseSoup.prettify()
    print outputRosters(parseSoup,parseURL,'H')
    print parseSoup.title.get_text() + ' :: ' + parseURL
    for i in goalScorer(parseSoup,parseURL,'H'):
        if i != None:
            specGoal = i.find("(")
            if specGoal > 0:
            #    print 'Special Character Begins @: ' + str(specGoal) + ' Total Length is: ' + str(len(i)) + ' Special Character Length is: ' + str(len(i)-specGoal)
                if (len(i)-specGoal) > 6:
                    endSpec = i.find(")")
                    print i[0:specGoal] + i[endSpec+1:len(i)] + ' :: ' + i[specGoal:endSpec+1]
                else:
                    print i[0:specGoal] + ' :: ' + i[specGoal:len(i)]
            else:
                print i
    for i in goalScorer(parseSoup,parseURL,'A'):
        if i != None:
            specGoal = i.find("(")
            if specGoal > 0:
            #    print 'Special Character Begins @: ' + str(specGoal) + ' Total Length is: ' + str(len(i)) + ' Special Character Length is: ' + str(len(i)-specGoal)
                if (len(i)-specGoal) > 6:
                    endSpec = i.find(")")
                    print i[0:specGoal] + i[endSpec+1:len(i)] + ' :: ' + i[specGoal:endSpec+1]
                else:
                    print i[0:specGoal] + ' :: ' + i[specGoal:len(i)]
            else:
                print i



counter = 0
while counter < 1:
    # Iterate over all Results for the World Cup
    urlArray = []
    urlArray = resultsURL(resultSoup)
    # print urlArray
    counter +=1
    # print '*** --------------- ***'
    # print (counter < 5)
    for i in urlArray:
        print '*** - - - - - - - - - - - - - - - - - - - - ***'
        parseURL = i
        parseMatch = urllib2.urlopen(parseURL)
        parseSoup = BeautifulSoup(parseMatch)
        print teamName(parseSoup,0,'H') + ' vs ' + teamName(parseSoup,0,'A') + ' ' + datetime.datetime.now().strftime("%H:%M:%S") + " Record Read"
        # counter += 1
        # print teamRosters(parseSoup,parseURL)

        for i in matchStats(parseSoup,parseURL,'B'):
            if i.find("Home") > 0:
                print "Record Saved for " + teamName(parseSoup,0,'H') + ' ' + datetime.datetime.now().strftime("%H:%M:%S")
                with open(outputMatch, "a") as f:
                    f.write(i.encode('utf-8') + '\n')
                    f.close() 
                for i in outputRosters(parseSoup,parseURL,'H'):
                    with open(playerStats, "a") as f:
                        f.write(i.encode('utf-8') + '\n')
                        f.close()

                    # print i.encode('utf-8')
            else:
                print "Record Saved for " + teamName(parseSoup,0,'A') + ' ' + datetime.datetime.now().strftime("%H:%M:%S")
                with open(outputMatch, "a") as f:
                    f.write(i.encode('utf-8') + '\n')
                    f.close() 
                for i in outputRosters(parseSoup,parseURL,'A'):
                    with open(playerStats, "a") as f:
                        f.write(i.encode('utf-8') + '\n')
                        f.close()                    
                    # print i.encode('utf-8')  


# 
