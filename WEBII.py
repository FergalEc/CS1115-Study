#!/usr/local/bin/python3											# specifies the location of python language files on the server
	
from cgitb import enable 											# allows to see error messages in the browser, should be commented out in release versions
enable()

from cgi import FieldStorage, escape								# these are included from external libraries
import pymysql as db 												# but derk bridge will most likely supply the nessacary imports in the question


            
print('Content-Type: text/html') 									# this is the http header data
print()																# this is the break in the header response



form_data = FieldStorage()											# grab the submitted data (if any) into an object called 'form_data'

result = ''															# make sure to declare variables that are used in the final http response below

if len(form_data) != 0 :											# check if there is any form data, if there is we need to do something
	#do something
	result = 'change'												# this is where we can make changes to the result of our web page
	try :
		first_name = escape(form_data.getfirst('name')).strip()								# we can grab any form data sent to us here

		# 	OPTION 1: 
		# 	if you want to add something to the database

		connection = db.connect('localhost', 'userid', 'password', 'database_name')			# this is how we create a connection to the database
        cursor = connection.cursor(db.cursors.DictCursor)									# we set up a cursor to interact with the databse
        cursor.execute("""INSERT INTO people (name)											# we write our sql code here
                          VALUES (%s, %s)""", (first_name))									# always use the comma to sanitize our code
        connection.commit()		#WARNING HERE#												# this is only needed if we are adding data to our database

        # 	OPTION 2:
        # 	else if you want to fetch something from the database
        connection = db.connect('localhost', 'userid', 'password', 'database_name')
        cursor = connection.cursor(db.cursors.DictCursor)
        cursor.execute("""SELECT * FROM people
        				  WHERE name = %s""", (first_name))									# we use the comma instead of a % to sanitize our SQL
        																					# not doing so would leave our database open to SQL Injection attacks
        #		WARNING - THE FOLLOWING CODE FROM LINES 47-52 IS ONLY USED IF WE FETCH DATA FROM THE DB
        # after grabbing the data in the second example, we have to grab the data from the cursor to use it. 
        # this will require a loop which also allows us to build the result procedurely

        result += "<ul>"							# alternatively you could add the opening tag of a table or something similar
        for row in cursor.fetchall():				# make sure not to forget the fetchall() function
        	result += "<li>%s</li>" % row['name']
        result += "</ul>"
        connecting.close()
        cursor.close()								# clean up a little bit and destroy un-needed objects

    except db.error :																		# if there is an error connecting to the database do something
    	result = "Sorry yo, couldn't do what you asked"										# in this case we set the result to an error message
										

       
       # this is the final print statement, it returns our edited web page
print( """
	<!DOCTYPE html>
        <html lang="en">
            <head>
                <title>Insert gigs</title>
            </head>
            <body>
                <form action="this_page.py" method="post">
                    <label for="name">First Name: </label>
                    <input type="text" name="bandname" value="name" size="50" maxlength="50" id="name"><br>
                    <input type="submit" value="Insert">
                </form>
                %s
            </body>
            </html>""" % (result)) 						# here we insert the updated or value of result



			### ### OTHER USEFUL HTML ### ###
			# this will generate a date picker in our html form automatically
			<input type='date' id='#' step='7' min='2015-02-01'>
			<input type="number" id='#' min='#' max="#" step="1">
			<input type="telephone" id="#" placeholer="081-1110111">



