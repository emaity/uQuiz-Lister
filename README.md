# uQuiz-Lister
Provides an interface to access uQuiz quizzes.

# Why?
uQuiz doesn't display more quizzes on additional pages, for some reason.

However, new quizzes are displayed in the "random" tab every 5 minutes. This project takes those new quizzes and stores their information into a database, allowing for multiple pages of quizzes without having to use uQuiz directly.

# Features
Pages! Yay!

Sorting by number of takers of a quiz, either by highest to lowest, lowest to highest, or in a random order. Changed with the drop down menu at the top right.

Hiding quizzes from the interface by pressing the "Don't Show Again" button overlaid on quiz entries. Quizzes can be unhidden in the menu opened using the "Hidden Quizzes" button at the bottom right. Hidden quizzes are handled with a cookie saved in the user's browser.

# requirements.txt
Additional packages that need to be installed for quizGet.py and the Flask application. Alternatively, one can browse quizzes by passing Quizzes.db into an online SQLite database viewer.

# quizGet.py
**NO LONGER WORKS** possibly due to some cloudfare protection. There may be a way to bypass this using cloudscraper, don't know if I'll try to implement that though.

quizGet.py sends a GET request to the uQuiz server for the random quizzes every 5 minutes, adding quizzes to the Quizzes.db database (quizzes already contained in the database are ignored).

quizGet.py has to be run for a while to save a decent amount of quizzes because it has to wait 5 minutes between each request. If there is a uQuiz api that I could've used instead, then I didn't find it. The included Quizzes.db file contains quizzes from when I ran it myself.

Note: The Quizzes.db file contained outside of the FlaskStuff folder is not the one that is accessed when main.py is run. The user will have to copy and paste it into the /static/ folder within FlaskStuff for new quizzes to be considered.

# FlaskStuff

This contains the files for the browser interface of uQuiz Lister. The .html, .css etc. files can be changed to customize the look of it, but the file to see the interface itself is main.py.

After running main.py, the application should then run on localhost, accessed at http://127.0.0.1:5000. If anything, it should say where the application is running.
