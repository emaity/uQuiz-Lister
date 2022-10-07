from os import remove
from re import T
from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3, random, json, sys

app=Flask(__name__)

connection = sqlite3.connect('./static/Quizzes.db')
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM 'quizzes'")
quizAmount = cursor.fetchone()[0] # number of quizzes in the database
connection.close()

numQuizzes = 40 # number of quizzes per page
pageNumber = 1
maxPages = int((quizAmount/numQuizzes) + (quizAmount%numQuizzes > 0))

orderAscending = False
orderDescending = False
orderRandom = True
randSeed = random.random()

def setOrderAscending():
    global orderAscending, orderDescending, orderRandom
    orderAscending = True
    orderDescending = False
    orderRandom = False

def setOrderDescending():
    global orderAscending, orderDescending, orderRandom
    orderAscending = False
    orderDescending = True
    orderRandom = False

def setOrderRandom():
    global orderAscending, orderDescending, orderRandom
    orderAscending = False
    orderDescending = False
    orderRandom = True


@app.context_processor
def inject_maxPages():
    return dict(maxPages = int((quizAmount/numQuizzes) + (quizAmount%numQuizzes > 0)))
@app.context_processor
def inject_orders():
    return dict(orderAscending=False, orderDescending=False, orderRandom=False)

@app.route('/')
def home():
    return redirect(url_for('page', pageNumber = pageNumber))

@app.route('/<int:pageNumber>')
def page(pageNumber):
    removeQuizzes=[]
    if 'quizzesTaken' in request.cookies:
        removeQuizzes = json.loads(request.cookies.get('quizzesTaken'))
    
    connection = sqlite3.connect('./static/Quizzes.db')
    cursor = connection.cursor()

    offset = (pageNumber-1)*numQuizzes

    # assembles part of query restricting the quizzes shown, based on removeQuizzes list (based on cookie data)
    # This could be improved:
    # make removeQuizzes a global variable, changing that instead
    # ~~~~~ONLY CHANGE WHEN it needs to be, create a list at the local scope to compare with global scope
    # Execute this code when lists are != each other
    # Would also have to make restrictQuery global, to keep its state
    # So, test equality, then find shorter of the two, then manipulate restrictQuery accordingly
    # will execute differently depending on whether the new list is shorter or longer
    restrictQuery = ''
    if removeQuizzes:
        restrictQuery = "WHERE url NOT IN ("
        for quizID in removeQuizzes:
            restrictQuery+= "'"+quizID+"'"
            if quizID != removeQuizzes[-1]:
                restrictQuery+=","
        restrictQuery+=") "

    # assembles query for database, depending on what order the user wants
    query = "SELECT * FROM 'quizzes' " + restrictQuery
    if orderAscending:
        query += "ORDER BY takerCount asc "
    elif orderDescending:
        query += "ORDER BY takerCount desc "
    elif orderRandom:
        query += f"ORDER BY (substr(takerCount * {randSeed}, length(takerCount) + 2))" # code from stackOverflow - 24256258
    query += "LIMIT ?, ?"

    cursor.execute(query, (offset, numQuizzes))
    dataList = cursor.fetchall() # list of entries of the database, correspoding to the proper page

    # get the user's cookies and make a list from the quizzes they've hidden
    hiddenQuizzes = []
    if 'quizzesTaken' in request.cookies:
        hiddenQuizzes = json.loads(request.cookies.get('quizzesTaken'))

    # didn't know how to do this properly lol, this isn't efficient at all
    # make a dictionary of urls:titles because the cookies only hold urls and I want to display titles
    quizDict = {}
    for quizUrl in hiddenQuizzes:
        cursor.execute("SELECT name FROM 'quizzes' WHERE url = '" + quizUrl +"'")
        quizTitle = cursor.fetchone()
        quizDict[quizUrl] = quizTitle[0]


    return render_template("home.html", pageNumber=pageNumber, dataList=dataList, orderAscending=orderAscending, orderDescending=orderDescending, orderRandom=orderRandom, numQuizzes=numQuizzes, removeQuizzes=removeQuizzes, hiddenQuizzes=hiddenQuizzes, quizDict=quizDict)

# Previous page
@app.route('/previous')
def previous():
    global pageNumber
    if pageNumber == 1:
        return redirect(url_for('page', pageNumber = pageNumber))
    else:
        pageNumber -= 1
        return redirect(url_for('page', pageNumber = pageNumber))

# Next page
@app.route('/next')
def next():
    global pageNumber
    if pageNumber == maxPages:
        return redirect(url_for('page', pageNumber = pageNumber))
    else:
        pageNumber += 1
        return redirect(url_for('page', pageNumber = pageNumber))

# Go to page input into the navigation input box
@app.route('/jump', methods=["POST", "GET"])
def jump():
    global pageNumber
    if request.method == "POST":
        print(type(request.form["page"]))
        if request.form["page"] == '':
            return redirect(url_for('page', pageNumber = pageNumber))
        elif int(request.form["page"]) > maxPages or int(request.form["page"]) < 1:
            return redirect(url_for('page', pageNumber = pageNumber))
        else:
            pageNumber = int(request.form["page"])
            return redirect(url_for('page', pageNumber = pageNumber))
    else:
        return "how did you get here?"

# Set quiz ordering to ascending
@app.route('/ascending')
def ascending():
    global pageNumber
    setOrderAscending()
    pageNumber = 1
    return redirect(url_for('page', pageNumber = pageNumber))

# Set quiz ordering to descending
@app.route('/descending')
def descending():
    global pageNumber
    setOrderDescending()
    pageNumber = 1
    return redirect(url_for('page', pageNumber = pageNumber))

# Set quiz ordering to random
@app.route('/random')
def randomRoute():
    global pageNumber, randSeed
    setOrderRandom()
    pageNumber = 1
    randSeed = random.random()
    return redirect(url_for('page', pageNumber = pageNumber))



# Stuff for handling cookies (quizzesTaken list) here

@app.route('/setCookie',methods=['POST'])
def setCookie():
    response = make_response()
    if 'quizzesTaken' in request.cookies:
        quizList = json.loads(request.cookies.get('quizzesTaken')) # takes in cookie data as a list
        quizList.append(request.get_data(as_text=True))
        #print(request.get_data(),file=sys.stderr)
        response.set_cookie('quizzesTaken', json.dumps(quizList))
        return response
    else:
        response = make_response()
        response.set_cookie('quizzesTaken', json.dumps([request.get_data(as_text=True)]))
        return response
    

# @app.route('/getCookie', methods=['GET','POST']) # for later, maybe dispaly list of removed quizzes
# def getCookie():
#     if 'quizzesTaken' in request.cookies:
#         quizList = request.cookies.get('quizzesTaken')
#         return quizList
#     else:
#         return "No cookie created yet"

@app.route('/removeFromHidden',methods=['POST'])
def removeFromHidden():
    response = make_response()
    # assumes that the cookie is present (button wouldn't show up otherwise)
    quizList = json.loads(request.cookies.get('quizzesTaken'))
    quizList.remove(request.get_data(as_text=True))
    response.set_cookie('quizzesTaken', json.dumps(quizList))
    return response

if __name__ == "__main__":
    app.run(debug=True)