# -*- coding: utf-8 -*-
'''
Created on  Nov 19, 2015
Modified on Nov 19, 2015
Version 0.01.a
@author: rainier.madruga@assurant.com
A simple Python Program to review an Excel file and parse stats for a database
'''
 
# Import and Load Libraries for Script
import datetime
import os
import openpyxl
import zipfile
import re
import sys
import mysql.connector
 
# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime('%H:%M:%S %f')[:-3]
ds = datetime.datetime.now().strftime("%x")
date = datetime.datetime.now().strftime("%Y-%m-%d")
parseVersion = 'v0.01.a :: Excel Stats Parsing :: ' + ts + '\n'
 
# Function to provide an updated Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%H:%M:%S.%f %p")[:-5]
    return update
 
shr = '>> *** ============= *** <<'
hr = '>> *** =========================================== *** <<'
 
# Define Base Path for Scanning and Reading
# Base Bath for Reading
localPath = 'D:\ESPN-Parser'

#Base Excel Workbook to be Read / Written To in Process
baseWkBk = '\\detail_stats.xlsx'
workBook = openpyxl.load_workbook(os.path.join(localPath + baseWkBk))
wkBkSheets = workBook.get_sheet_names()
playerSheet = workBook.get_sheet_by_name('CoreData')
fixtureSheet = workBook.get_sheet_by_name('matches')
savedSheet = workBook.get_sheet_by_name('players')
statSheet = workBook.get_sheet_by_name('Sheet1')
logSheet = workBook.get_sheet_by_name('Sheet2')

print ('Current Worksheets within file:', wkBkSheets)

# Change Base Working Directory to basePath
os.chdir(localPath)

# Function to check that path exists
def pathCheck(x):
    if os.path.exists(x) == False:
        print('Designated Path does not exist: ' + x)
        return False
    else:
    	# print('Path exists: ' + x)
    	return True

# Confirm that all File Directories are available.
pathCheck(localPath)

rowCount = 2
cellCount = 2
playerHighestRow = playerSheet.get_highest_row()
fixtureHighestRow = fixtureSheet.get_highest_row()

print ('Current Count of Player Stats: ', str(playerHighestRow))
print ('Current Count of Match Stats: ', str(fixtureHighestRow))

def returnTeam(x):
	inputTeam = x
	outputTeam = 0
	if inputTeam == 'AFC Bournemouth' or inputTeam == 'Bournemouth':
		outputTeam = 1
	elif inputTeam == 'Arsenal':
		outputTeam = 2
	elif inputTeam == 'Aston Villa':
		outputTeam = 3
	elif inputTeam == 'Chelsea':
		outputTeam = 4
	elif inputTeam == 'Crystal Palace':
		outputTeam = 5
	elif inputTeam == 'Everton':
		outputTeam = 6
	elif inputTeam == 'Leicester City' or inputTeam == 'Leicester':
		outputTeam = 7
	elif inputTeam == 'Liverpool':
		outputTeam = 8
	elif inputTeam == 'Manchester City' or inputTeam == 'Man City':
		outputTeam = 9
	elif inputTeam == 'Manchester United' or inputTeam == 'Man Utd':
		outputTeam = 10
	elif inputTeam == 'Newcastle United' or inputTeam == 'Newcastle':
		outputTeam = 11
	elif inputTeam == 'Norwich City' or inputTeam == 'Norwich':
		outputTeam = 12
	elif inputTeam == 'Southampton':
		outputTeam = 13
	elif inputTeam == 'Stoke City' or inputTeam == 'Stoke':
		outputTeam = 14
	elif inputTeam == 'Sunderland': 
		outputTeam = 15
	elif inputTeam == 'Swansea City' or inputTeam == 'Swansea':
		outputTeam = 16
	elif inputTeam == 'Tottenham Hotspur' or inputTeam == 'Tottenham':
		outputTeam = 17
	elif inputTeam == 'Watford': 
		outputTeam = 18
	elif inputTeam == 'West Bromwich Albion' or inputTeam == 'West Brom':
		outputTeam = 19
	elif inputTeam == 'West Ham United' or inputTeam == 'West Ham':
		outputTeam = 20
	else:
		outputTeam = 99
	return outputTeam

# Set the range from which to work with when parsing the Excel Stats
while rowCount <= playerHighestRow:
	# Load Excel Row...
	fixtureID = playerSheet['D' + str(rowCount)].value
	playerTeam = playerSheet['B' + str(rowCount)].value
	playerID = playerSheet['E' + str(rowCount)].value
	playerJersey = playerSheet['G' + str(rowCount)].value
	playerStatus = playerSheet['T' + str(rowCount)].value
	playerPOS = playerSheet['F' + str(rowCount)].value
	shots = playerSheet['J' + str(rowCount)].value
	shotsOnGoal = playerSheet['K' + str(rowCount)].value
	goals = playerSheet['L' + str(rowCount)].value
	assists = playerSheet['M' + str(rowCount)].value
	offSides = playerSheet['N' + str(rowCount)].value
	foulsDrawn = playerSheet['O' + str(rowCount)].value
	foulsCommitted = playerSheet['P' + str(rowCount)].value
	saves = playerSheet['Q' + str(rowCount)].value
	yellowCards = playerSheet['R' + str(rowCount)].value
	redCards = playerSheet['S' + str(rowCount)].value
	rowValue = [fixtureID, playerTeam, playerID]
	statValues= [shots, shotsOnGoal, goals, assists, offSides, foulsDrawn, foulsCommitted, saves, yellowCards, redCards]

	# Save Players to Players Worksheet
	savedSheet['A' + str(rowCount)] = returnTeam(playerTeam)
	savedSheet['B' + str(rowCount)] = playerID
	savedSheet['C' + str(rowCount)] = playerPOS
	savedSheet['D' + str(rowCount)] = playerJersey
	savedSheet['E' + str(rowCount)] = playerSheet['H' + str(rowCount)].value
	savedSheet['F' + str(rowCount)] = playerSheet['I' + str(rowCount)].value
	savedSheet['G' + str(rowCount)] = 'imgURL'
	print ("Row %d of %d written." % (rowCount, playerHighestRow))

	# print ('Match ID: ', fixtureID, ' :: playerTeam :', playerTeam, ' :: playerID: ', playerID)
	count = 0
	while count < len(statValues):
		statSheet['A' + str(cellCount)] = fixtureID
		statSheet['B' + str(cellCount)] = returnTeam(playerTeam)
		statSheet['C' + str(cellCount)] = playerID
		statSheet['D' + str(cellCount)] = count + 1
		statSheet['E' + str(cellCount)] = statValues[count]
		cellCount +=1
		count += 1
	# print ('Player ID ', playerID, ' written.')
	# Write Player POS for Fixture to New worksheet
	logSheet['A' + str(rowCount)] = fixtureID
	logSheet['B' + str(rowCount)] = returnTeam(playerTeam)
	logSheet['C' + str(rowCount)] = playerID
	logSheet['D' + str(rowCount)] = playerStatus
	logSheet['E' + str(rowCount)] = playerPOS

	# Increment Row Count
	rowCount += 1

# Update Fixture Information
rowCount = 2
while rowCount <= fixtureHighestRow:
	homeTeam = ''
	awayTeam = ''
	print (homeTeam, 'vs. ', awayTeam)

	homeTeam = fixtureSheet['F' + str(rowCount)].value
	fixtureSheet['F' + str(rowCount)] = returnTeam(homeTeam)
	
	awayTeam = fixtureSheet['G' + str(rowCount)].value
	fixtureSheet['G' + str(rowCount)] = returnTeam(awayTeam)
	
	print (homeTeam, 'vs. ', awayTeam)
	print (shr)

	rowCount += 1 

workBook.save(os.path.join(localPath +'\\' + date + '_detailstats.xlsx'))