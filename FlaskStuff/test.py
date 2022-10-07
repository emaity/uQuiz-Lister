import sqlite3

connection = sqlite3.connect('./static/mattQuiz.db')
cursor = connection.cursor()

pageNumber = 1
numQuizzes = 30
offset = (pageNumber-1)*numQuizzes


# cursor.execute("SELECT * FROM 'quizzes' LIMIT ?, ?", (offset, numQuizzes))

# list = cursor.fetchall()

# num = 0
# for thing in list[0]:
#     print(num,": ")
#     print(thing)
#     num += 1

cursor.execute("SELECT COUNT(*) FROM 'quizzes'")

num = cursor.fetchone()[0]

print(num)

connection.close()