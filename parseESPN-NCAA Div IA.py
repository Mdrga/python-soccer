# -*- coding: utf-8 -*-

'''
Created on Aug 12, 2014
Modified on Aug 13, 2014
Version 0.01.b 
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Establish the process Date, Time and Version Stamp of the Script
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
parseVersion = 'NCAA Div IA Stats & Schedule 2014 - v0.01.b'

# URLs for Main Body of Script to work through
scheduleURL = "http://espn.go.com/college-football/schedule"
scheduleOpen = urllib2.urlopen(scheduleURL)
scheduleSoup = BeautifulSoup(scheduleOpen)

outputPath = 'NCAA-Data/'
outputImgs = 'NCAA-Data/imgs/'

# Output base 
outputBase = 'NCAA-Schedule.html'
outputBase = os.path.join(outputPath, outputBase)
with open(outputBase, "w") as f:
     f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
     f.write(scheduleSoup.prettify("utf-8"))
     f.close()

# <div class="span-6 last">
scheduleDiv = scheduleSoup.find("div", {"class":"span-6 last"})
outputURLs = 'NCAA-FullSchedules.html'
outputURLs = os.path.join(outputPath, outputURLs)
with open(outputURLs, "w") as f:
	f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
	f.write(scheduleDiv.prettify())
	f.close()

# <div class="col-main">
scheduleActual = scheduleSoup.find("div", {"class":"col-main"})
outputWeek = 'NCAA-WeekSchedules.html'
outputWeek = os.path.join(outputPath, outputWeek)
with open(outputWeek, "w") as f:
	f.write(ds + ' :: ' + ts + ' :: ' + parseVersion + '\n')
	f.write(scheduleActual.prettify())
	f.close()

# Arrays for Output of the Week's Schedule
scheduleURLWeekArray = []
scheduleURLConfArray = []
scheduleTXTConfArray = []

# <div class="week">
scheduleWeek = scheduleDiv.find("div", {"class":"week"})
scheduleConf = scheduleDiv.find("div", {"class":"floatright cross-links"})
scheduleWeekURL = scheduleWeek.find_all("a")
scheduleConfURL = scheduleConf.find_all("option")
scheduleTable = scheduleActual.find_all("table")

for i in scheduleWeekURL:
	scheduleURLWeekArray.append(i["href"])
for i in scheduleConfURL:
	scheduleURLConfArray.append(i["value"])
for i in scheduleConfURL:
	scheduleTXTConfArray.append(i.get_text(strip=True))

# Test output of HTML and Navigational Elements
# print scheduleConf.prettify()
# print scheduleWeekURL
for i in scheduleTable:
	# print i.prettify()
	print '>>>> **** ================================================================================================================================ **** <<<<'
	weekDate = i.find("tr", {"class":"stathead"})
	weekDate = weekDate.get_text(strip=True)
	# print weekDate
	weekRow = i.find_all("td")
	print len(weekRow)
	rowData = []
	for i in weekRow:
		print i.prettify()
		print i.get_text()
		dayLength = weekDate.find(",")
		day = weekDate[0:dayLength]
		date = weekDate[dayLength+2:len(weekDate)]
		dateOfMonth = date.find(" ")
		dateOfMonth = date[dateOfMonth+1:len(weekDate)]
		month = date[0:date.find(" ")]
		rowData.append(day[0:3] + ', ' + dateOfMonth + '-' + month[0:3]) 
		print '>>> *** =========================== *** <<<'

# print scheduleDiv.prettify()
'''
teamName = teamURL[22:len(teamURL)]
teamNameHTML = teamName + '.html'
teamNameHTML = os.path.join(outputPath, teamNameHTML)
teamTitle = str(teamSoup.title.get_text(strip=True))
teamTitle = teamTitle[24:len(teamTitle)]
'''