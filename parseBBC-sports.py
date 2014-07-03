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

''' ======================================================================== ***
URLs for use in testing the parsing of the World Cup & results:
	France vs Honduras - http://www.bbc.com/sport/0/football/25285092
	Switzerland vs Ecuador - http://www.bbc.com/sport/0/football/25285085
	Full World Cup Results - http://www.bbc.com/sport/football/world-cup/results
	Upcoming Fixtures - http://www.bbc.com/sport/football/fixtures
	Algeria v Russia - http://www.bbc.com/sport/football/25285249
*** ======================================================================== '''

''' ======================================================================== ***
    TO-DO ITEMS
    Add in CSV Writer to Parse out the Update File (Identifies when / if Page was updated)
    Output Game Date in CSV Details 
*** ======================================================================== '''

# Create an array of URL Links.
website = ["http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/football/25285249", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Open World Cup Results 
gameWeb = urllib2.urlopen(website[3])
gameSoup = BeautifulSoup(gameWeb)
parseVersion = 'WorldCup v0.13.d'

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
# with open('WorldCup-Update.txt', "a") as f:
# 		f.write(ds + '|' + ts + '|' + parseVersion + '|' + gameSoup.title.get_text() + '\n')
#		f.close()

# Find the Main Results Table and Output the Results
divResults = gameSoup.find("div", {"class":"league-table table-narrow mod"})
'''
with open('WorldCup-Results.html', "w") as f:
	f.write(divResults.prettify())
	f.close()
'''

# Initialize Results Output File
with open('MatchRestuls-output.txt', "w") as f:
    f.write(ds + '|' + ts + '|' + parseVersion + '|' + gameSoup.title.get_text() + '\n')
    f.close()
    
with open('urlOutput.txt', "w") as f:
    f.write(ds + '|' + ts + '|' + parseVersion + '|' + gameSoup.title.get_text() + '\n')
    f.close()

divMatchResults = gameSoup.find_all("div", {"class":"fixtures-table full-table-medium"})
# print divMatchResults
for i in divMatchResults:
	# Create slices for output of results
	resultsHomeTeam = i.find_all("span", {"class":"team-home teams"})
	resultsAwayTeam = i.find_all("span", {"class":"team-away teams"})
	resultsPaddedScore = i.find_all("span", {"class":"score"})
	resultsGameDay = i.find_all("h2", {"class":"table-header"})
	urlList = i.find_all('a', {'class': 'report'})
	
	x = len(resultsHomeTeam)
	z = 0

	# Iterate over the Match Results
	while z < x:
		resultHomeTeam = resultsHomeTeam[z].get_text(strip=True)
		resultAwayTeam = resultsAwayTeam[z].get_text(strip=True)
		resultScore = resultsPaddedScore[z].get_text(strip=True)
		
		# Full URL for BBC Site
		stringURL = urlList[z].get("href")
		href = "http://www.bbc.com" + stringURL
		
		# Create output file of just the URLs for Matches played
		urlOutput = open('urlOutput.txt',"a")
		urlLinkOutput = [stringURL[16:24],href]
		writer = csv.writer(urlOutput, delimiter='|')
		writer.writerow(urlLinkOutput)
		
		# Create output file and generate Results CSV
		resultOutput = open('MatchRestuls-output.txt', "a")
		resultMatchOutput = [ds, ts, stringURL[16:24], resultHomeTeam, resultScore[0], resultAwayTeam, resultScore[2], href]
		writer = csv.writer(resultOutput, delimiter='|')
		writer.writerow(resultMatchOutput)
		# print resultMatchOutput
		z += 1

