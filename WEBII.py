#!/usr/local/bin/python3

from cgitb import enable
enable()

from cgi import FieldStorage
import pymysql as db

print('Content-Type: text/html')
print()

form_data = FieldStorage()
result =''
first_name = form_data.getfirst('name', '').strip() # we can grab any form data sent to us here

if len(form_data) != 0 : # check if there is any form data, if there is we need to do something
    #do something
    try :
        # OPTION 1:
        # if you want to add something to the database
        connection = db.connect('credentials')
        cursor = connection.cursor(db.cursors.DictCursor) # we set up a cursor to interact with the databse
        cursor.execute("""INSERT INTO people (name)
                    VALUES (%s)""", (first_name)) # always use the comma to sanitize our code
        
        connection.commit() #WaRNING HERE# # this is only needed if we are adding data to our database
    
    except db.Error : # if there is an error connecting to the database do something
        result = "Sorry yo, couldn't do what you asked" # in this case we set the result to an error message
        # this is the final print statement, it returns our edited web page
 
 
 
print( """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Insert gigs</title>
    </head>
    <body>
    <form action="db.py" method="post">
    <label for="name">First Name: </label>
    <input type="text" name="name" size="50" maxlength="50" id="name"><br>
    <input type="submit" value="Insert">
    </form>
    %s
    </body>
    </html>""" % (result)) # here we insert the updated or value of 'result'
