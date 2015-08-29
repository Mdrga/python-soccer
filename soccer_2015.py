# -*- coding: utf-8 -*-
'''
Created on  May 24, 2015
Modified on May 24, 2015
Version 0.01.a
@author: rainier.madruga@assurant.com
A simple Python Program to pull data for the 2015-16 Soccer Season
'''
# Import and Load Libraries for Script
import datetime
import os
import platform
import sys
import openpyxl
import json
import requests
import re
import http.client
import pprint

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime('%H:%M:%S %f')[:-3]
fileTS = datetime.datetime.now().strftime('%H%M%S')
ds = datetime.datetime.now().strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y%m%d")

# parseVersion Devfinition used for output file tagging
parseVersion = 'v0.01.a :: Barclays Premier League 2015-16 ' 

# Updates the Time Stamp
def updateTS():
    update = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    return update

shr = '>> *** ============= *** <<'
hr = '>> *** =========================================== *** <<'

baseSeasonURL = '/alpha/soccerseasons'
baseBPLSeason = '/alpha/soccerseasons/354'
connection = http.client.HTTPConnection('api.football-data.org')
headers = {'X=Auth-Token': '1449f58d05384f9fb4f9102961ed2fd3'}
connection.request('GET', baseBPLSeason, None, headers)

seasonJSON = json.loads(connection.getresponse().read().decode())

seasonData = 'bpl-file.json'
with open(seasonData, "w") as j:
	j.write('[ ' + parseVersion + ' :: ' + ds + ' ' + updateTS() + ' ]' + '\n')
	j.close()
	print (hr, '\n', 'JSON saved locally')

# Dump seasonJSON to local File
with open(seasonData, "a") as output:
	json.dump(seasonJSON, output)
	output.write('\n' + shr + '\n')
	output.close()

seasonDetail = seasonJSON['_links']
teamsURL = seasonDetail['teams']['href']
fixturesURL = seasonDetail['fixtures']['href']
lastUpdated = seasonJSON['lastUpdated']
seasonDesc = seasonJSON['caption']
print (teamsURL)
print (lastUpdated)
print (seasonDesc)
print (hr)

# pprint.pprint(seasonJSON)

teamResponse = requests.get(teamsURL)
teamResponse.raise_for_status()

teamsJSON = json.loads(teamResponse.text)
teamsData = teamsJSON['teams']
stepCount = 0
for i in teamsData:
	teamsInfo = teamsData[stepCount]
	pprint.pprint(teamsInfo)
	print (shr)
	teamDetail = teamsInfo['_links']
	teamAbbr = teamsInfo['code']
	#teamCrest = teamsInfo['crestURL']
	teamName = teamsInfo['name']
	#teamValue = teamsInfo['squadMarketValue']

#pprint.pprint(teamsJSON)

with open(seasonData, "a") as output:
	json.dump(teamsJSON, output)