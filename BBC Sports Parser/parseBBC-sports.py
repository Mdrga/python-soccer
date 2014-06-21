'''
Created on Jun 16, 2014
Modified on Jun 20, 2014
Version 0.12.a
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime

''' ======================================================================== ***
URLs for use in testing the parsing of the World Cup & results:
	France vs Honduras - http://www.bbc.com/sport/0/football/25285092
	Switzerland vs Ecuador - http://www.bbc.com/sport/0/football/25285085
	Full World Cup Results - http://www.bbc.com/sport/football/world-cup/results
	Upcoming Fixtures - http://www.bbc.com/sport/football/fixtures
*** ======================================================================== '''

''' ======================================================================== ***
    TO-DO ITEMS
    Add in CSV Writer to Parse out the Update File (Identifies when / if Page was updated)
    Output Game Date in CSV Details 
    Output Match Results Link to CSV Details
*** ======================================================================== '''

# Create an array of URL Links.
website = ["http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Open World Cup Results 
gameWeb = urllib2.urlopen(website[2])
gameSoup = BeautifulSoup(gameWeb)
parseVersion = 'WorldCup v0.12.a'

# Output All Results Page to a local HTML file
outputTxt = 'WorldCup-Base.html'
with open(outputTxt, "w") as f:
	 f.write(gameSoup.prettify("utf-8"))
	 f.close()

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")

# Output Time & Date Stamp as well as Script Version
print ds + ' | ' + ts
with open('WorldCup-Update.txt', "a") as f:
		f.write(ds + '|' + ts + '|' + parseVersion + '|' + gameSoup.title.get_text() + '\n')
		f.close()

# Find the Main Results Table and Output the Results
divResults = gameSoup.find("div", {"class":"league-table table-narrow mod"})
with open('WorldCup-Results.html', "w") as f:
	f.write(divResults.prettify())
	f.close()

divMatchResults = gameSoup.find("div", {"class":"fixtures-table full-table-medium"})
with open('WorlCup-MatchResults.html', "w") as f:
	f.write(divMatchResults.prettify())
	f.close()

# Update Date for Matches
divUpdateDate = gameSoup.find_all("h2", {"class":"table-header"})
print divUpdateDate

# Posts when Matches were last updated on Page
tableGameResults = divMatchResults.find_all("table", {"class":"table-stats"})

# Output Match Results to a File
divMatchDetails = gameSoup.find_all("td", {"class":"match-details"})
for i in divMatchDetails:
	with open('WorldCup-MatchDetails.html', "a") as f:
		f.write(i.prettify())
		f.close()

# Initialize the MatchDetails-output.txt File for appending the Game Scores
with open('MatchDetails-output.txt', "w") as f:
	f.write(ds + " " + ts + '\n')
	f.close()

for i in divMatchDetails:
	# print str(i)
	divHomeTeam = i.find("span", {"class":"team-home teams"})
	divAwayTeam = i.find("span", {"class":"team-away teams"})
	divPaddedScore = i.find("span", {"class":"score"})
	divScore = divPaddedScore.get_text(strip=True)
	divMatchOutput = ds + '|' + ts + '|' + divHomeTeam.get_text(strip=True) +'|' + divScore[0] + '|' + divAwayTeam.get_text(strip=True) + '|' + divScore[2] + '\n'
	# urlMatchLink = i.find("a", {"class":"report"})
	# Test File Output with this statement
	# print divMatchOutput
	# print str(len(divHomeTeam.get_text(strip=True)))
	# print ts
	
	with open('MatchDetails-output.txt', "a") as f:
		f.write(divMatchOutput)
		f.close()	
	# print divScore
	# <tr class="report" id="match-row-EFBO731784">
	# <a class="report" href="/sport/football/25285162">

urlList = divMatchResults.find_all('a', {'class': 'report'})
for i in urlList:
	print i

