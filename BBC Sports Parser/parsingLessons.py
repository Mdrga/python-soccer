'''
Created on Jun 5, 2014
Modified on 
Version 0.01
@author: rainier.madruga@gmail.com
A simple Python Program to scrape a website's content.
'''
from bs4 import BeautifulSoup
import os, sys, csv
import urllib2

#Define current path for the Script
currentPath = os.path.dirname(os.path.abspath("__file__"))
print currentPath

# Make the Spreadsheet Path
outputCSV = currentPath + '/spreadsheet.csv'
print outputCSV
print (sys.version)

# Open the file
csvFile = open(outputCSV, "w")

# Create writer object
writer = csv.writer(csvFile, delimiter='|')

# Define source URL & pass to BeautifulSoup
webpage = urllib2.urlopen("http://inadaybooks.com/justiceleague")
soup = BeautifulSoup(webpage)

# Function to extract metadata
def extractMData(webpage):
    soup = BeautifulSoup(webpage)
    print soup.title

# Get Contents of Container Div
divContainer = soup.find("div", {"id":"container"})

# Get Specific Block within Container within Div
divBlock = divContainer.findAll("div", {"class":"block"})

# Get Specific Seperator Block within Div
divSep = divBlock[3].findAll("div", {"class":"separator"})

# Get Member Names from the Page
members = divSep[3].findAll("a")
print divSep[3].prettify()

# Print Out Member Names
for member in members:
	# Strip <a> tags
	href = member.get("href")
	url = "http://inadaybooks.com/justiceleague/" + href
	row = [member.get_text(), member.get("title"), url]
	print row
	writer.writerow(row)

print currentPath

