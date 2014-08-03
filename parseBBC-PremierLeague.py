'''
Created on Jul 23, 2014
Modified on Jul 31, 2014
Version 0.03.b
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime
import sqlite3

# Establish the process Date, Time and Version Stamp of the Script
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
parseVersion = 'Premier League 2014 - v0.03.b'

# URLs for Main Body of Script to work through
fixturesURL = "http://www.bbc.com/sport/football/premier-league/fixtures"
fixturesOpen = urllib2.urlopen(fixturesURL)
fixturesSoup = BeautifulSoup(fixturesOpen)

# Save a local copy of the Fixtures Page
outputBase = 'PL-Fixtures.html'
with open(outputBase, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
     f.write(fixturesSoup.prettify("utf-8"))
     f.close()

# Find the containers with the Fixtures information within the HTML page
fixtureList = fixturesSoup.find("div", {"class":"stats"})
fixtureDiv = fixtureList.find("div", {"class":"fixtures-table full-table-medium"})

# Parse out the main Fixture Table to a local file
fixturesTable = fixturesSoup.find("div", {"class":"stats-body"})
with open("PL-fixture-table.html", "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
     f.write(fixtureDiv.prettify("utf-8"))
     f.close()

# Create Iteration to Output Fixtures by Date
counter = 0
matchDate = fixtureDiv.find_all("h2", {"class":"table-header"})
matches = fixtureDiv.find_all("table")

# Create a function to return the Team Name or URL
# x = Incoming data from the HTML
# y = 'H'ome or 'A'way Team
# z = 'N'ame / 'H'REF or 'O'ther Data
def returnTeam(x, y, z):
	teamContent = x
	teamSearch = y
	outputFormat = z
	teamSearchReturn = ""
	output = ''

	# Search for either the Home or Away Team Span
	if teamSearch == 'H':
		teamSearchReturn = teamContent.find("span", {"class":"team-home teams"})
	elif teamSearch == 'A':
		teamSearchReturn = teamContent.find("span", {"class":"team-away teams"})
	else:
		teamSearchReturn = "Invalid Team Type Parameter Passed. Please pass either an H or an A."
	
	# Intake Team and establish Output Format
	if outputFormat == 'N':
		output = teamSearchReturn.get_text(strip=True)
	elif outputFormat == 'H':
		output = teamSearchReturn.a
		output = output.get("href")
	else:
		output = output + " :: Additionally the Format Indicator Selected is Incorrect."

	return output

# Function to receive a Text Date (i.e., Saturday 16th August 2014) and return 2014-08-16
def textDate(x):
	stringDate = x
	dayOfWeek = stringDate[0:4]
	length = len(stringDate)
	output = ''
	dateSpace = stringDate.find(" ")
	# print dateSpace
	year = stringDate[length-4:length]
	monthDay = stringDate[dateSpace+1:length-4]
	monthSpace = monthDay.find(" ")
	# print monthSpace
	day = monthDay[0:monthSpace-2]
	month = monthDay[monthSpace+1:len(monthDay)-1]
	month = returnMonth(month)
	output = dayOfWeek + '|' + year +'-' + month + '-' + day
	return output

# Function to return a two digit month for a literal Month (i.e., change "August" to "08").
def returnMonth(x):
	inputMonth = x
	inputMonth = inputMonth[0:3]
	outputMonth = ''
	# print inputMonth
	if inputMonth == 'Aug':
		outputMonth = '08'
	elif inputMonth == 'Sep':
		outputMonth = '09'
	elif inputMonth == 'Oct':
		outputMonth = '10'
	elif inputMonth == 'Nov':
		outputMonth = '11'
	elif inputMonth == 'Dec':
		outputMonth = '12'
	elif inputMonth == 'Jan':
		outputMonth = '01'
	elif inputMonth == 'Feb':
		outputMonth = '02'
	elif inputMonth == 'Mar':
		outputMonth = '03'
	elif inputMonth == 'Apr':
		outputMonth = '04'
	elif inputMonth == 'May':
		outputMonth = '05'
	elif inputMonth == 'Jun':
		outputMonth = '06'
	else:
		outputMonth = '07'
	return outputMonth

# Create file that parses out the Fixture Details
with open("PL-fixtures.txt", "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
     f.write("dayOfWeek|fixtureDate|matchKickoff|matchID|matchStatus|homeName|awayName|homeURL|awayURL" + '\n')
     f.close()

'''	  
TODO - Create a log table within the database to track when the process runs
       Log Table should read: DateStamp | TimeStamp | Script Version
TODO - Track if the parsing of the URL was successful
TODO - DateTime stamp the row when written to the database
TODO - Parse data to database
'''	

while counter < len(matchDate):
# Line below is used for Unit Testing of Code
# while counter < 2:
	# Parse out the pieces of the Fixture from the main HTML container
	fixtureDate = matchDate[counter]
	fixtureDate = fixtureDate.get_text(strip=True)
	fixtureDate = textDate(fixtureDate)
	fixtureBlock = matches[counter]
	fixtureDetail = fixtureBlock.find_all("tr", {"class":"preview"})
	# Parse out the components of the Fixture. Create a single line to parse the data out
	for i in fixtureDetail:
		matchID = i.get("id")
		matchID = matchID[10:len(matchID)]
		matchKickoff = i.find("td", {"class":"kickoff"})
		matchKickoff = matchKickoff.get_text(strip=True)
		matchStatus = i.find("td", {"class":"status"})
		matchStatus = matchStatus.get_text(strip=True)
		homeName = returnTeam(i, 'H', 'N') 
		homeURL = returnTeam(i, 'H', 'H')
		awayName = returnTeam(i, 'A', 'N') 
		awayURL = returnTeam(i, 'A', 'H')
		with open("PL-fixtures.txt", "a") as f:
			f.write(fixtureDate + "|" + matchKickoff + ' GMT' + '|' + matchID + '|' + matchStatus + '|' + homeName + '|' + awayName + '|' + homeURL + '|' + awayURL + '\n')
			f.close()
	counter +=1
