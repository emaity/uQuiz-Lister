# Getting uquiz quizzes
import requests
import os
import sqlite3
import time # uquiz updates the random quizzes every 5 minutes

# This is the url that uquiz gets its 'random' quizzes from
JSONurl = 'https://uquiz.com/Api/Discovery/Random?returnJson=true&NumberToReturn=40'

r = requests.get(JSONurl) # sends a get request to that url maybe? gets a json file as a response
jsonResponse = r.json()

# jsonResponse['Quizzes'] gives us a list of dictionaries, I think

# Notable keys for each dictionary:
# UrlId - id to append to https://uquiz.com/
# QuizName - name of the quiz
# TakerCount - number of people who have taken the quiz
# HalfAndHalfImageFileName - Image used for quiz thumbnail, can be null
#                            Accessed with format https://img.uquiz.com/content/images/quiz_thumbnails/halfandhalf/[UrlId]/[HalfAndHalfImageFileName]/
# HasHalfAndHalfImage - either 'true' or 'false'
#                       If false, then thumbnail can be BackgroundImageFileName - check HasBackgroundImage first
#                       HalfAndHalf image takes precedence over BackgroundImage - if this is true, then just display that one
# BackgroundImageFileName - Image possibly used for quiz thumbnail, can be null
#                           Accessed with format https://img.uquiz.com/content/images/quiz/[BackgroundImageFileName]
# HasBackgroundImage  - only to be checked if HasHalfAndHalfImage is false; can be either 'true' or 'false'
# DisplayTakerCount   - string to be displayed along with thumbnail; how many people took the quiz



# Alright now let's put stuff into a database I guess?

connection = sqlite3.connect('Quizzes.db')
cursor = connection.cursor()

# Creates a table to hold quiz information

# Use JSON bools to decide which image to use
# When db -> html, check if HH is null - if so, then check if BG is null - else, some default image

# This creates a database file (quizzes) with these columns vvv
cursor.execute(''' CREATE TABLE IF NOT EXISTS quizzes (
                url TEXT PRIMARY KEY,
                name TEXT,
                takerCount INTEGER,
                HHImageFile TEXT,
                BGImageFile TEXT,
                displayCount TEXT)''')

while True:
    r = requests.get(JSONurl)
    jsonResponse = r.json()
    numQuizzes = 0

    for quiz in jsonResponse['Quizzes']:
        if quiz['TakerCount'] > 0: # only add to database if more than 1000 people have taken the quiz
            numQuizzes += 1
            url = quiz['UrlId']
            name = quiz['QuizName']
            takerCount = int(quiz['TakerCount'])
            displayCount = quiz['DisplayTakerCount']
            if quiz['HasHalfAndHalfImage'] == False:
                if quiz['HasBackgroundImage'] == False:
                    HHImageFile = None
                    BGImageFile = None
                else:
                    HHImageFile = None
                    BGImageFile = quiz['BackgroundImageFileName']
            else:
                HHImageFile = quiz['HalfAndHalfImageFileName']
                BGImageFile = None
            
            #tupleToInsert = (url, name, takerCount, HHImageFile, BGImageFile, displayCount)

            cursor.execute("INSERT OR IGNORE INTO quizzes VALUES (?,?,?,?,?,?)", (url, name, takerCount, HHImageFile, BGImageFile, displayCount) )

    connection.commit()
    print("Added maybe", numQuizzes, "quizzes")
    print()

    time.sleep(305) # Wait 5 minutes (and 5 seconds) for uquiz to update
    print("looped")