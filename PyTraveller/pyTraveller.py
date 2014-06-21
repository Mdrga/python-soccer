'''
Created on  Aug 19, 2013
Modified on Apr 29, 2014
Version 0.52
@author: rainier.madruga@gmail.com
A simple Python Program to generate Traveller characters, in accordance with the Mongoose Traveller rules.
'''
import random
import collections
import sqlite3

''' # Character Attributes as a Tuple
    # First Number is the Attribute Score
    # Second Number is the Dice Modifier'''

# Class to Define the Player Character Object
class PlayerCharacter(object):
    def __init__(self, name, hw1, hw2, Str, Dex, End, Int, Edu, Soc):
        self.name = name
        self.hw1 = hw1
        self.hw2 = hw2
        self.Str = Str
        self.Dex = Dex
        self.End = End
        self.Int = Int
        self.Edu = Edu
        self.Soc = Soc

'''# Function to randomly generate the character's name '''
def charName():
    names = ['Magnus', 'Reginald', 'Magnolia', 'Carter', 'Scooter', 'Hobart', 'James', 'Flash', 'Coltrane', 'Luke', 'Han']
    charName = random.choice(names)
    return charName

'''# Function to roll a number of multi-sided dice '''
def diceRoll(num, sides):
    x = num
    y = sides
    counter = 0
    score = 0
    while counter < x:
        score += random.randint(1,y)
        counter +=1
    return score

'''# Function to return the Dice Modifier for the Attribute Score
   # Pass an Integer (X) and the function returns an Integer Dice Modifier 
   # -3 to 3 as a possible range of values'''
def attribMod(x):
    mod = 0
    score = x
    if score <= 0 :
        mod = -3
    elif score >= 1 and score <= 2:
        mod = -2
    elif score >= 3 and score <= 5:
        mod = -1
    elif score >= 6 and score <= 8:
        mod = 0
    elif score >= 9 and score <=11:
        mod = 1
    elif score >= 12 and score <= 14:
        mod = 2
    elif score >= 15:
        mod = 3
    return mod

''' # Function to return the Homeworld Literal for the Homeworld Roll '''
def homeWorld(x):
    if x == 1:
        homeWorld = 'Agricultural'
    elif x == 2:
        homeWorld = 'Asteroid'
    elif x == 3:
        homeWorld = 'Desert'
    elif x == 4:
        homeWorld = 'Fluid Oceans'
    elif x == 5:
        homeWorld = 'Garden'
    elif x == 6:
        homeWorld = 'High Technology'
    elif x == 7:
        homeWorld = 'High Population'
    elif x == 8:
        homeWorld = 'Ice-Capped'
    elif x == 9:
        homeWorld = 'Industrial'
    elif x == 10:
        homeWorld = 'Low Technology'
    elif x == 11:
        homeWorld = 'Poor'
    elif x == 12:
        homeWorld = 'Rich'
    elif x == 13:
        homeWorld = 'Water World'
    elif x == 14:
        homeWorld = 'Vacuum'
    return homeWorld

loopCounter = 0
numLoops = 50

while loopCounter < numLoops:
    player = PlayerCharacter(charName(), diceRoll(1,14), diceRoll(1,14), diceRoll(2,6), diceRoll(2,6), diceRoll(2,6), diceRoll(2,6), diceRoll(2,6), diceRoll(2,6))
    while player.hw1 == player.hw2:
        player.hw2 = diceRoll(1,14)
    print("Name: " + player.name)
    print("Str %d " % player.Str +"| %d" % attribMod(player.Str) + " Dex %d " % player.Dex +"| %d" % attribMod(player.Dex) + " End %d " % player.End + "| %d" % attribMod(player.End))
    print("Int %d " % player.Int +"| %d" % attribMod(player.Int) + " Edu %d " % player.Edu +"| %d" % attribMod(player.Edu) +  " Soc %d " %player.Soc + "| %d" % attribMod(player.Soc)) 
    print("Homeworld Traits: " + homeWorld(player.hw1) + ' & ' + homeWorld(player.hw2))
    # print("Homeworld Trait #1 = %d " % player.hw1)
    # print("Homeworld Trait #2 = %d " % player.hw2)
    print("")
    loopCounter += 1


