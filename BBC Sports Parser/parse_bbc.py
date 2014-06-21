'''
Created on Jun 13, 2014
Modified on 
Version 0.01
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC News website for content.
'''
from bs4 import BeautifulSoup
import os, sys, csv
import urllib2
import time

# Define current path for the Script
currentPath = os.path.dirname(os.path.abspath("__file__"))

# Get the BBC News Website to a Variable
webpage = urllib2.urlopen("http://www.bbc.com/news/world/latin_america/")
soup = BeautifulSoup(webpage)

# Define and output the raw HTML to a local file for reference
outputTxt = currentPath + '/BBC_news.html'
with open(outputTxt, "w") as f:
	 f.write(soup.prettify("utf-8"))
	 f.close()

# Create writer object
# writer = csv.writer(outputTxt, delimiter='|')

# Find the Block Main Navigation 
divNavMain = soup.find("ul", {"id":"blq-nav-main"})
#print divNavMain.prettify("utf-8")

# Pull out the navigation elements from the blq-nav-main list
divElements = divNavMain.find_all("a")
# for i in divElements:
	# print i.a
	# print i.href

divListMain = divNavMain.find_all("li")
for i in divListMain:
	print i.a

# Get Main Contents of the Page
divMain = soup.find("div", {"id":"main-content"})

# Get Page Last Update Date & Time
divUpdateSpan = soup.find("div", {"class":"index-date"})
divUpdateDate = divUpdateSpan.find("span", {"class":"date"})
divUpdateTime = divUpdateSpan.find("span", {"class":"time"})
print divUpdateDate.get_text() + ' ' + divUpdateTime.get_text()

# Output to File Header
with open('Update.txt', "a") as f:
    f.write(divUpdateDate.get_text() + '|' + divUpdateTime.get_text() + '|' + (time.strftime("%H:%M")) + '|' + soup.title.get_text() + '\n')
    f.close()

print (divUpdateDate.get_text() + '|' + divUpdateTime.get_text() + '|' + (time.strftime("%H:%M")) + '|' + soup.title.get_text())

# Find all Stories on the page
divStory = soup.find_all("a", {"class":"story"})

'''
for i in divStory:
	href = i.get("href")
	print href
'''