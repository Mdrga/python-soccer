# -*- coding: utf-8 -*-
'''
Created on Jan 30, 2015
Modified on Jan 30, 2015
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
'''
'''
Version Number of Script
'''
version = '0.01.a'

# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime
import requests
import os
import platform
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%H:%M:%S")
    return update

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print 'Downloading %s...' % (localFileName)
    with open(localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

# Program Version & System Variables
parseVersion = 'ESPN Premier League Team News ' + version
print ds + ' :: ' + ts + ' :: ' + parseVersion

# Set Output Path for Windows or Mac environments
os_System = platform.system()
win_BasePath = "C:/Users/Rainier/Documents/GitHub/python-soccer"

if os_System == "Windows":
    outputPath = win_BasePath + "/PL-Data/"
    outputImgPath = win_BasePath + "/PL-Data/imgs/"
    outputTeamPath = win_BasePath + "/PL-Data/teams/"
    outputMatchPath = win_BasePath + "/PL-Data/match/"
else:
    outputPath = 'PL-Data/'
    outputImgPath = 'PL-Data/imgs/'
    outputTeamPath = 'PL-Data/teams/'
    outputMatchPath = 'PL-Data/match/'

hr = " >>> *** ====================================================== *** <<<"
shr = " >>> *** ==================== *** <<<"

prefixBBC = "http://www.bbc.com"
prefixESPN = "http://www.espnfc.us"
OutOfSquad = "http://www.fantasyfootballscout.co.uk/fantasy-football-injuries/"

print hr

# Create Text File for Player Injuries
playerData = 'epl-playerinjuries.txt'
outputPlayerData = os.path.join(outputPath, playerData)
with open(outputPlayerData, "w") as f:
			f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
			f.write('Team|PlayerName|Img|Status|ReturnDate|Reason|Detail|URL' + '\n' )
			f.close()

# Open Website and parse HTML
OutOfSquadOpen = urllib2.urlopen(OutOfSquad)
OutOfSquadSoup = BeautifulSoup(OutOfSquadOpen)
oosDiv = OutOfSquadSoup.find("div", {"id":"content"})
oosTable = oosDiv.find("table", {"class":"ffs-ib ffs-ib-full-content ffs-ib-sort"})

print hr
oosDataArray = []

oosTableBody = oosTable.find_all("tbody")
for i in oosTableBody:
	oosTableRow = i.find_all("tr")
	for i in oosTableRow:
		oosTableElement = i.find_all("td")
		# print oosTableElement[0]
		cellOne = oosTableElement[0]
		cellTwo = oosTableElement[1]
		cellThree = oosTableElement[2]
		cellFour = oosTableElement[3]
		cellFive = oosTableElement[4]
		cellSix = oosTableElement[5]
		returnDate = cellFour.get_text(strip=True)
		imgSrc = cellOne.find("img")
		imgSrc = "http:" + imgSrc["src"]
		teamName = cellTwo["title"]
		playerStatus = cellThree.get_text(strip=True)
		playerName = cellOne.get_text(strip=True)
		playerGivenName = playerName.find("(")
<<<<<<< Updated upstream
		statusDetail = cellFive.get_text()
		statusDetail = statusDetail.lstrip()
=======
>>>>>>> Stashed changes
		statusURL = cellFive.find("a")
		statusReason = cellFive.find("strong")
		statusReason = statusReason.get_text(strip=True)
		statusDesc = cellFive.get_text(strip=True)
		statusDesc = statusDesc[len(statusReason):len(statusDesc)]
<<<<<<< Updated upstream
		statusDesc = statusDesc.rstrip("[Source]")
=======
		statusDesc = statusDesc.strip('[Source]')
		updateDate = cellSix.get_text(strip=True)
		updateDate = updateDate[6:10] + "-" + updateDate[3:5] + "-" + updateDate[0:2]
>>>>>>> Stashed changes
		
		# print statusReason + "|" + statusDesc
		# print statusURL
		if statusURL is not None:
			statusURL = statusURL["href"]
			# print statusURL
		else:
			statusURL = " "
		# statusURL = cellFive.find("a")
		# statusURL = statusURL["href"]

		# Determine if Player identified just by Surname or Given Name + Surname
		if playerGivenName > -1:
			playerName = playerName[playerGivenName+1:len(playerName)-1] + " " + playerName[0:playerGivenName]
		else:
			playerName = playerName
		if returnDate == "Unknown":
			returnDate = "0000-00-00"
		else:
			returnDate = returnDate[6:10] + "-" + returnDate[3:5] + "-" + returnDate[0:2]

<<<<<<< Updated upstream
		output = playerName + "|" + imgSrc + "|" + teamName + "|" + playerStatus + "|" + returnDate + "|" + statusReason + "|" + statusDesc + "|"  + statusURL
		with open(outputPlayerData, "a") as f:
			f.write(output + '\n')
			f.close()

		print "Record written."
=======
		output = updateDate + "|" + playerName + "|" + teamName + "|" + imgSrc + "|" + playerStatus + "|" + returnDate + "|" + statusReason + "|" + statusDesc + "|" + statusURL
		print output
>>>>>>> Stashed changes

		#for i in oosTableElement:
			# print i.prettify()
		# print shr
	print hr