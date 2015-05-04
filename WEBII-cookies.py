#!/usr/local/bin/python3

from cgitb import enable 
enable()

from cgi import FieldStorage, escape
import pymysql as db

from os import environ                        # import files needed
from http.cookies import SimpleCookie         # the header section will most likely be provided by Derek Bridge


print("Content-Type: text/html")              # very likely he might ask us for this
print()                                       # don't forget this print, it signals the end of the HTTP header

form_data = FieldStorage()      # grab the data that has been sent to us 

http_cookie_header = environ.get('HTTP_COOKIE')     # check if there are any cookies in the header
if not http_cookie_header :                         # if there isn't proceed
  if len(form_data) != 0 :                          # check if we have been given form data
    # we have data, let's do something with it
    try :
      band_vote = escape(form_data.getfirst('bands')).strip()     # store the band voted for as band_vote
      
      connection = db.connect('localhost', 'userid', 'password', 'database_name')     # connect to database
      cursor = connection.cursor(db.cursors.DictCursor)           # set up cursor
      cursor.execute("""UPDATE votes
                        SET num_votes = num_votes + 1
                        WHERE band = '%s'""", (band_vote))        # don't forget the comma to sanitize
      cursor.commit()                                             # needed because we updated the database
      cookie = SimpleCookie()                         # create a cookie object called cookie 
      cookie['band'] = band_vote                      # set it's value to the band we voted for
      cookie['band']['expires'] = 9999999             # don't firget to set an expiration date
      result = 'Woo, you voted for %s. What terrible taste' % band_vote;
    except db.Error :                       # this is called if something goes wrong connecting to the database
      result = 'Something went wrong!'         # create an error message if we coudn't connect
else :                                      # the user already voted
  cookie.load(http_cookie_header)
  last_vote = cookie['band'].value
  result = 'You already voted for %s, twonk.' % last_vote     # what a twonk
  
  
  # our final print, which sends our finalized html in the http standard
print("""
      <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Voting Form</title>
        </head>
        <body>
            <form action='this-page.py' method='post'>
                <label for='bands'>Select your favourite band to vote.</label>
                <select name='bands'>
                  <option value='Evanescence'>Evanescence</option>
                  <option value='LinkinPark'>Linkin Park</option>
                </select>
                <input type='submit' value='Vote'>
            </form>
            %s
        </body>
    </html>
      """ % (result))

