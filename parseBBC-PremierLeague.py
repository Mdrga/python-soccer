'''
Created on Jul 23, 2014
Modified on Jul 25, 2014
Version 0.02.a
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime

# Establish the process Date, Time and Version Stamp of the Script
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
parseVersion = 'Premier League 2014 - v0.02.a'

# URLs for Main Body of Script to work through
fixturesURL = "http://www.bbc.com/sport/football/premier-league/fixtures"
fixturesOpen = urllib2.urlopen(fixturesURL)
fixturesSoup = BeautifulSoup(fixturesOpen)

#print fixturesSoup.prettify('utf-8')

# Save a local copy of the Fixtures Page
outputBase = 'PL-Fixtures.html'
with open(outputBase, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion)
     f.write(fixturesSoup.prettify("utf-8"))
     f.close()

fixtureList = fixturesSoup.find("div", {"class":"stats"})

# print fixtureList.prettify('utf-8')

# <div class="stats-body" role="main">
# <div class="fixtures-table full-table-medium" id="fixtures-data">

fixturesTable = fixturesSoup.find("div", {"class":"stats-body"})
fixturesDates = fixturesTable.find_all("h2", {"class":"table-header"})

'''# Fixture Date for Table Row
for i in fixturesDates:
	fixDate = i.get_text()
	dateStart = fixDate[12:len(fixDate)]
	print dateStart
	# print len(i.get_text())
'''

print "*** >>> = = = = = = = = = = = = = = = = = <<< ***"
# print "\n"
# print fixturesTable.prettify()

'''
for i in fixturesMatch:
	print "*** >>> = = = = = = = = = = = = = = = = = <<< ***"
	print i.prettify()
'''

with open("PL-fixture-table.html", "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion)
     f.write(fixturesTable.prettify("utf-8"))
     f.close()

fixtureRow = fixturesTable.find_all("tr", {"class":"preview"})
for i in fixtureRow:
	# print i
	matchID = i.get("id")
	matchKickoff = i.find("td", {"class":"kickoff"})
	matchKickoff = matchKickoff.get_text(strip=True)
	
	spanHome = i.find("span", {"class":"team-home teams"})
	homeURL = spanHome.find("a")
	homeURL = homeURL.get("href")
	spanHome = spanHome.get_text(strip=True)
	
	spanAway = i.find("span", {"class":"team-away teams"})
	awayURL = spanAway.find("a")
	awayURL = awayURL.get("href")
	spanAway = spanAway.get_text(strip=True)

	print matchID + '|' + matchKickoff + '|GMT|H|' + spanHome + '|A|' + spanAway + '|' + homeURL + '|' + awayURL

# print fixturesTable.prettify()		