'''
Created on Jun 16, 2014
Modified on Jun 26, 2014
Version 0.13.c
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
website = ["http://www.bbc.com/sport/football/25285249", "http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Parse out Specific Match Results
gameMatch = urllib2.urlopen(website[0])
matchSoup = BeautifulSoup(gameMatch)
parseVersion = 'WorldCup v0.13.c'

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
        # listHoldRoster = i.find_all("ul", {"class":"player-list"})
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
	       playerRow = playerJersey + '|' + playerDetails + '|' + startingLineup(counter) + '|'
	       #print playerRow
	       counter += 1
	       rosterArray.append(playerRow.encode('utf-8'))
    return rosterArray

for i in rosterOutput(listHomeRoster):
    with open ('MatchDetails-output.txt', "a") as f:
        f.write(i + '\n')
        f.close()
      

print rosterOutput(listAwayRoster)

# for i in rosterOutput(listHomeRoster):
#    print i

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
        print detailsTeam.get_text() + ' No Goals Scored'
    else: 
        for i in listScorer:
            scorer = i.find("span")
            print detailsTeam.get_text() + ' Goal Scorers: ' + i.get_text(strip=True) + ' '
        # print listScorer


