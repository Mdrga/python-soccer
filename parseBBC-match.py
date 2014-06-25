
'''
Created on Jun 16, 2014
Modified on Jun 24, 2014
Version 0.13.a
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
website = ["http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Parse out Specific Match Results
gameMatch = urllib2.urlopen(website[0])
matchSoup = BeautifulSoup(gameMatch)
parseVersion = 'WorldCup v0.13.a'

outputBase = 'WorldCup-MatchBase.html'
with open(outputBase, "w") as f:
	 f.write(matchSoup.prettify("utf-8"))
	 f.close()

divDetailResults = matchSoup.find_all("div", {"class":"team-match-details"})

#with open('detailResults.html', "w") as f:
#	f.write(divDetailResults)
#	f.close()

divLineup = matchSoup.find("div", {"id":"oppm-team-list"})

listHomeRoster = divLineup.find_all("div", {"class":"home-team"})
# print listHomeRoster
for i in listHomeRoster:
	listRoster = i.find_all("ul", {"class":"player-list"})
	lineup = i.find_all("li")
	for i in lineup:
		# print i.text
		# print len(i.text)
		playerDetails =  i.text[7:len(i.text)]
		print i.text[3:5] + ' ' + playerDetails
		playerStart = playerDetails.find("  ")
		if len(playerDetails) - playerStart > 2:
			playerUpdate = i.text[7:(len(i.text)-(len(playerDetails) - playerStart))]
			print playerUpdate

for i in divDetailResults:
	# print i
	detailsTeam = i.find("span", {"class":"team-name"})
	detailsScorer = i.find_all("p", {"class":"scorer-list blq-clearfix"})
	detailsSpan = i.find("span")
	returnTeam = detailsTeam.get_text()
	
	
	# Determine if the Scorers contains any values
	try:
		detailsScorer
	except NameError:
		detailsScorer = None

 