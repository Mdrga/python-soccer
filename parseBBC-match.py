'''
Created on Jun 16, 2014
Modified on Jul 07, 2014
Version 0.13.e
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import csv
import urllib2
import datetime

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")

# Create an array of URL Links.
website = ["http://www.bbc.com/sport/football/27961190","http://www.bbc.com/sport/football/27990605","http://www.bbc.com/sport/football/25285249", "http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Parse out Specific Match Results
gameMatch = urllib2.urlopen(website[1])
gameURL = website[1]
matchSoup = BeautifulSoup(gameMatch)
parseVersion = 'WorldCup v0.13.e'

outputBase = 'WorldCup-MatchBase.html'
with open(outputBase, "w") as f:
     f.write(matchSoup.prettify("utf-8"))
     f.close()
# Identify Team Lineup
divDetailResults = matchSoup.find_all("div", {"class":"team-match-details"})
divLineup = matchSoup.find("div", {"id":"oppm-team-list"})

listHomeRoster = divLineup.find_all("div", {"class":"home-team"})
listAwayRoster = divLineup.find_all("div", {"class":"away-team"})

# Initialize Results Output File
with open('MatchDetails-output.txt', "w") as f:
    f.write(ds + '|' + ts + '|' + parseVersion + '|' + 'Match Results File' + '\n')
    f.close()

# Identify the Starting IX and the Bench
def startingLineup(x):
    lineupCount = x
    if lineupCount < 12:
        return "Started Match"
    else:
        return "Bench"

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
        i.encode('utf-8')
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

for i in rosterOutput(listHomeRoster):
    with open ('MatchDetails-output.txt', "a") as f:
        f.write(i + '\n')
        f.close()

for i in rosterOutput(listAwayRoster):
    with open ('MatchDetails-output.txt', "a") as f:
        f.write(i + '\n')
        f.close()

'''# Get Team Results from the container divDetailResults:
for i in divDetailResults:
    # print i
    detailsTeam = i.find("span", {"class":"team-name"})
    listScorer = i.find_all("p", {"class":"scorer-list blq-clearfix"})
    detailsSpan = i.find("span")
    returnTeam = detailsTeam.get_text()
    # Determine if the Scorers contains any values
    try:
        listScorer
    except NameError:
        listScorer = None
    
    # Output of the Goal Scorers for the Teams
    if listScorer == []:
        scorer = ""
    else: 
        for i in listScorer:
            scorer = i.find("span")
            # print detailsTeam.get_text() + ' Goal Scorers: ' + i.get_text(strip=True) + ' '
        # print listScorer
'''

# Team Match Details & Team Badge
divTeamDetails = matchSoup.find("div", {"class":"post-match"})

# Initialize the Stats File
with open('MatchStats-output.txt', "w") as f:
    f.write(ds + '|' + ts + '|' + parseVersion + '|' + 'Match Stats File' + '\n')
    f.close()

# Parses the values contained in the divTeamDetails in to Team-Level Stats for the Match
for i in divTeamDetails:
    #print i
    if len(i) > 1:
        # print len(i)
        homeTeam = i.find("div", {"id":"home-team"})
        awayTeam = i.find("div", {"id":"away-team"})
        
        spanHomeScore = homeTeam.find("span", {"class":"team-score"})
        spanAwayScore = awayTeam.find("span", {"class":"team-score"})
        
        homeScorer = homeTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
        awayScorer = awayTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
        
        homeTeamBadge = homeTeam.find("img")
        awayTeamBadge = awayTeam.find("img")
        # Identify if anyone scored for the team
        
        # Array to contain the Team Output Line
        teamOutput = []
        
        totalGoalsScored = int(spanHomeScore.get_text()) + int(spanAwayScore.get_text())
        # print totalGoalsScored

        # Change this Process to look at the value of spanTEAMScore and run from that.
        try:
            homeScorer
        except NameError:
            homeScorer = None
        if homeScorer != []:
            for i in homeScorer:
                i.encode('utf-8')
                teamOutput.append(gameURL + '|' + returnHome(divTeamDetails) +'|' + spanHomeScore.get_text() + '|'+ i.get_text() + '|' + homeTeamBadge["src"])
        else:
            teamOutput.append(gameURL + '|' + returnHome(divTeamDetails) + '|' + spanHomeScore.get_text() + '|' + '|' + homeTeamBadge["src"])
        try:
            awayScorer
        except NameError:
            awayScorer = None
        if awayScorer != []:
            for i in awayScorer:
                i.encode('utf-8')
                teamOutput.append(gameURL + '|' + returnAway(divTeamDetails) + '|' + spanAwayScore.get_text() + '|' + i.get_text() + '|' + awayTeamBadge["src"])
        else:
            teamOutput.append(gameURL + '|' + returnAway(divTeamDetails) + '|' + spanAwayScore.get_text() + '|' + '|' + awayTeamBadge["src"])
        
        # print teamOutput
        for i in teamOutput:
            with open('MatchStats-output.txt', "a") as f:
                f.write(i.encode('utf-8') + '\n')
                f.close()

# Function to return Match Stats based on input of matchSoup
def matchStats(x):
    funcMatch = x
    divTeamDetails = funcMatch.find("div", {"class":"post-match"})
    divMatchStats = funcMatch.find("div", {"id":"match-stats-wrapper"})
    statPossession = divMatchStats.find("div", {"id":"possession"})
    statShots = divMatchStats.find("div", {"id":"total-shots"})
    statPossessionHome = statPossession.find("span", {"class":"home"})
    statPossessionAway = statPossession.find("span", {"class":"away"})
    homeTeam = divTeamDetails.find("div", {"id":"home-team"})
    awayTeam = divTeamDetails.find("div", {"id":"away-team"})
    homeScorer = homeTeam.find("p", {"class":"scorer-list blq-clearfix"})
    awayScorer = awayTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
    spanHomeScorer = homeScorer.find_all("span")
    spanHomeScore = homeTeam.find("span", {"class":"team-score"})
    spanAwayScore = awayTeam.find("span", {"class":"team-score"})

    homeTeamBadge = homeTeam.find("img")
    awayTeamBadge = awayTeam.find("img")

    teamStats = []

    # Parse Game URL into segments. Will be using the last portions to create a unique BBC_MatchID 
    strGameURL = gameURL.split('/')
    BBC_MatchID = strGameURL[5]

    teamStats.append(BBC_MatchID + '|' + 'Home' + '|' + homeTeam.a.get_text() + '|' + homeTeamBadge["src"] + '|' + statPossessionHome.get_text() + '|' + spanHomeScore.get_text())
    teamStats.append(BBC_MatchID + '|' + 'Away' + '|' + awayTeam.a.get_text() + '|' + awayTeamBadge["src"] + '|' + statPossessionAway.get_text() + '|' + spanAwayScore.get_text())

    with open ('MatchStats-output.html', "w") as f:
        f.write(funcMatch.prettify('utf-8'))
        f.close()

    return teamStats

for i in matchStats(matchSoup):
    print i