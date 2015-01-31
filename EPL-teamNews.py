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

teamURLs = ['/club/arsenal/359/index','/club/aston-villa/362/index','/club/burnley/379/index','/club/chelsea/363/index','/club/crystal-palace/384/index','/club/everton/368/index','/club/hull-city/306/index','/club/leicester-city/375/index','/club/liverpool/364/index','/club/manchester-city/382/index','/club/manchester-united/360/index','/club/newcastle-united/361/index','/club/queens-park-rangers/334/index','/club/southampton/376/index','/club/stoke-city/336/index','/club/sunderland/366/index','/club/swansea-city/318/index','/club/tottenham-hotspur/367/index','/club/west-bromwich-albion/383/index','/club/west-ham-united/371/index']

def teamNews(x):
	teamURL = x
	teamName = x
	teamName = teamName[6:len(teamName)-10]
	teamURL = prefixESPN + teamURL
	teamHTML = urllib2.urlopen(teamURL)
	teamSoup = BeautifulSoup(teamHTML)	
	recentNews = teamSoup.find("div", {"id":"feed"})
	recentNewsItems = recentNews.find_all("div", {"class":"feed-item-content"})
	recapOutput = []
	print "Team News Parsed :: " + teamName
	for i in recentNewsItems:
		recapPhotoItem = i.find("div", {"class":"thumbnail picture"})

		if len(i) > 3:
			# recapPhotoItem = recapPhotoItem.find("img")
			# print recapPhotoItem["src"]
			# with open(outputTxt, "a") as f:
			#	f.write('\n' + shr + '\n')
			#	f.write(i.prettify())
			#	f.write('\n' + shr + '\n')
			#	f.close()
			# print shr
			recapHeadline = i.find("h2")
			recapHeadlineDetails = recapHeadline.find("a")
			recapHeadlineDetails = recapHeadlineDetails["href"]
			recapHeadline = recapHeadline.get_text(strip=True)
			recapAge = i.find("span", {"class":"age"})
			recapAge = recapAge.get_text(strip=True)
			recapOutput.append(date + "|" + teamName + "|" + recapHeadline + "|" + recapHeadlineDetails + "|" + recapAge)
			#print shr
			# print i.prettify()
			#print recapHeadlineDetails 
			#print shr
			#recapDetails = recapHeadline.find("a")
			#recapDetails = recapDetails["href"]
			#print recapDetails
			# print recapAge.get_text(strip=True)
			
			#print updateTS()
			#print shr
			# print i
		else:
			#print i
			#print shr
			recapGameOpponents = i.find_all("div", {"class":"team-name"})
			recapGameScore = i.find_all("div", {"class":"team-score"})
			recapGameStatus = i.find("div", {"class":"game-info"})
			recapGameHome = recapGameOpponents[0].get_text(strip=True)
			recapGameAway = recapGameOpponents[1].get_text(strip=True)
			recapHomeScore = recapGameScore[0].get_text(strip=True)
			recapAwayScore = recapGameScore[1].get_text(strip=True)
			#recapGameInfo = i.find("div", {"clas=":"game-info"})
			recapOutput.append(date + "|" + teamName + "|" + recapGameHome + " " + recapHomeScore +  " v. " + recapAwayScore + " "+ recapGameAway + "||")
			# print i
	for i in recapOutput:
		print i
	print hr 
	return recapOutput

teamNewstxt = 'teamNews.txt'
with open(teamNewstxt, "w") as f:
   	f.write(ds + " :: " + updateTS() + " :: " + parseVersion + '\n' )
   	f.close()

for i in teamURLs:
	for x in teamNews(i):
		with open(teamNewstxt, "a") as f:
			f.write(x + '\n')
			f.close()
