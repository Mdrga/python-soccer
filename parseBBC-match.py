'''
Created on Jun 16, 2014
Modified on Jul 01, 2014
Version 0.13.d
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
website = ["http://www.bbc.com/sport/football/27961190","http://www.bbc.com/sport/football/25285113","http://www.bbc.com/sport/football/25285249", "http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Parse out Specific Match Results
gameMatch = urllib2.urlopen(website[1])
matchSoup = BeautifulSoup(gameMatch)
parseVersion = 'WorldCup v0.13.d'

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

def rosterOutput(x):
    rosterArray = []
    counter = 1
    for i in x:
        i.encode('utf-8')
        # print i
        # listHoldRoster = i.find_all("ul", {"class":"player-list"})
	# Setup Team Name Output
	lineup = i.find_all("li")
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
	       playerUpdateRow = playerJersey + '|' + playerName + '|' + startingLineup(counter) + '|' + playerUpdate 
	       #print playerUpdateRow
	       counter += 1
	       rosterArray.append(playerUpdateRow.encode('utf-8'))
	   else:
	       playerRow = playerJersey + '|' + playerDetails[0:len(playerDetails)-2] + '|' + startingLineup(counter) + '|'
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

# print rosterOutput(listAwayRoster)
# for i in rosterOutput(listHomeRoster):
#    print i
# divDetailResults:
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

# Match Stats Details
divMatchStats = matchSoup.find("div", {"id":"match-stats-wrapper"})

print len(divMatchStats)
divPossession = divMatchStats.find("div", {"id":"possession-chart"})

print divPossession

# Team Match Details & Team Badge
divTeamDetails = matchSoup.find("div", {"class":"post-match"})

for i in divTeamDetails:
    # print i
    if len(i) > 1:
        # print len(i)
        homeTeam = i.find("div", {"id":"home-team"})
        awayTeam = i.find("div", {"id":"away-team"})
        
        spanHomeTeam = homeTeam.find("span", {"class":"team-name"})
        spanAwayTeam = awayTeam.find("span", {"class":"team-name"})
        
        spanHomeScore = homeTeam.find("span", {"class":"team-score"})
        spanAwayScore = awayTeam.find("span", {"class":"team-score"})
        
        homeScorer = homeTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
        awayScorer = awayTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
        
        homeTeamBadge = homeTeam.find("img")
        awayTeamBadge = awayTeam.find("img")
        # Identify if anyone scored for the team
        
        try:
            homeScorer
        except NameError:
            homeScorer = None
        if homeScorer != []:
            for i in homeScorer:
                print spanHomeTeam.get_text() +'|' + spanHomeScore.get_text() + '|'+ i.get_text() + '|' + homeTeamBadge["src"]
        else:
            print spanHomeTeam.get_text() + '|' + spanHomeScore.get_text() + '|' + '|' + homeTeamBadge["src"]
        try:
            awayScorer
        except NameError:
            awayScorer = None
        if awayScorer != []:
            for i in awayScorer:
                print spanAwayTeam.get_text() + '|' + spanAwayScore.get_text() + '|' + i.get_text() + '|' + awayTeamBadge["src"]
        else:
            print spanAwayTeam.get_text() + '|' + spanAwayScore.get_text() + '|' + '|' + awayTeamBadge["src"]
        # print homeScorer
    # else:
        # print "***-------------***"
    
    # homeTeam = i.find("div", {"id":"home-team"})
    # print homeTeam
    # print "***------------------------------------***"
