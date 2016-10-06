#!python3
# -*- coding: utf-8 -*-
'''
Created on Sep 22, 2016
Modified on Oct 04, 2016
Version 0.03.ga
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the ESPN FC website for content.
'''
# Import Libraries needed for Scraping the various web pages
import bs4 
import re
import datetime
import time
import requests
import webbrowser
import os
import sys
import codecs
import mysql.connector

'''
### =========================================================================================== ###
### Change & Revision Log                                                                       ###
### Date             Dev        Change Description                                              ###
### =========================================================================================== ###
    2016-09Sep-22    RWM        Initial Draft to parse out stats from the staged stats line
    2016-10Oct-04    RWM        Added queries to begin looking for the existence of the Stat Row
                                for the player in the table Player_Statistics

'''

# Set Character Output
print ('System Encoding:', sys.stdout.encoding)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Establish MySQL Connection
cnx = mysql.connector.connect(user='root', password='password',
								 host='127.0.0.1',
								 database='fanfootball',
								 use_pure=False)

playerCnx = mysql.connector.connect(user='root', password='password',
                                 host='127.0.0.1',
                                 database='fanfootball',
                                 use_pure=False)

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return update

# Download Image
def downloadImage(imageURL, localFileName):
    response = requests.get(imageURL)
    if response.status_code == 200:
        print ('Downloading %s...' % (localFileName))
    with open(localimgPath + localFileName, 'wb') as fo:
        for chunk in response.iter_content(4096):
            fo.write(chunk)
    return True

hr = " >>> *** ======================================================================= *** <<<"
shr = " >>> *** ==================== *** <<<"

# Program Version & System Variables
parseVersion = 'Premier League Stats Parser v0.03.ga'
print (ds + ' :: ' + ts + ' :: ' + parseVersion)
print ('Python Version :: ' + sys.version)
print (hr)

seasonID = 2

cursor = cnx.cursor()
cursor.execute("SELECT ps_seasonID, ps_team, ps_matchID, ps_playerID, ps_Shots, ps_ShotsOnGoal, ps_Goals, ps_Assists, ps_Offsides, ps_FoulsDrawn, ps_FoulsCommitted, ps_Saves, ps_YellowCards, ps_RedCards FROM fanfootball.stg_player_stats WHERE ps_seasonID = 2")

# Function to Update Player Yow
def statUpdate(row):
    # print (row)
    # Parse out the Stat Rows from the Staging Table
    statSeasonID = row[0]
    statTeamID = row[1]
    statMatchID = row[2]
    statPlayerID = row[3]
    
    # Stats Quantities
    statShots = row[4]
    statSOG = row[5]
    statGoals = row[6]
    statAssist = row[7]
    statOffside = row[8]
    statFoulDrawn = row[9]
    statFoulCommit = row[10]
    statSaves = row[11]
    statYellowC = row[12]
    statRedC = row[13]

    chkStat = 1

    # Create a counter per Row to help assign the Stat Category ID per Staging Row...
    while chkStat <= 10:
        sql = ("SELECT seasonID, teamID, matchID, playerID, statCategoryID FROM fanfootball.player_statistics WHERE seasonID = %s AND teamID = %s AND matchID = %s and playerID = %s and statCategoryID = %s" % (statSeasonID, statTeamID, statMatchID, statPlayerID, chkStat))
        insert = ("INSERT INTO fanfootball.player_statistics VALUES (%s, %s, %s, %s, %s, %s)" % (statSeasonID, statTeamID, statMatchID, statPlayerID, chkStat, row[chkStat+3]))

        statUpdate = playerCnx.cursor()
        try:
            statUpdate.execute(insert)
            playerCnx.commit()
            print ('Row written succesfully...')
        except:
            playerCnx.rollback()
        
        chkStat += 1
    # print ('Done')

# Begin Parsing out the Rows needed to be added to the Player Stats Table
for row in cursor:
    statUpdate(row)
    # print (hr)

cnx.close()