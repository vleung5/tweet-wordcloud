from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from os import path, getcwd
import time
import numpy as np
import matplotlib.pyplot as plt
import json
import re
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sqlite3
from sqlite3 import Error

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key=""
consumer_secret=""

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=""
access_token_secret=""

start_time = time.time() #grabs the system time

stopwords = set(STOPWORDS) 
sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS tweets(tweet_text text);"""

def cleanTweetText(tweet):
	retweet_rx = re.compile(r'RT @\w+:\s') 
	url_rx     = re.compile(r'https://\w\.\w+/\w+')
	hashtag_rx = re.compile(r'#\w+\s')
	to_user_rx = re.compile(r'@\w+\s')
	regex      = [retweet_rx, url_rx, hashtag_rx, to_user_rx]
	for rx in regex:
		tweet = re.sub(rx, '', tweet)
	return tweet

def createWordCloud(cleanedText):
	d = getcwd()
	mask = np.array(Image.open(path.join(d, 'Sony-Music-logo-880x654.png')))
	wordcloud = WordCloud(background_color='white', width = 880, height = 654, stopwords = stopwords, mask=mask).generate(cleanedText)
	image_colors = ImageColorGenerator(mask)
	plt.figure(figsize=(7,7))
	plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
	plt.axis("off")
	plt.show()
	
	 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("created table")
    except Error as e:
        print(e)   
	
def storeTweet(cleanedText):
	conn = create_connection("C:\\sqlite\\db\\tweets.db")
	if conn is not None:
		#create projects table
		create_table(conn, sql_create_tweets_table)
	else:
		print("Error! cannot create the database connection.")
	cur = conn.cursor()
	print(cleanedText)
	try:
		cur.execute('INSERT INTO tweets(tweet_text) values(?)',(cleanedText,))
	except sqlite3.IntegrityError as e:
		print('sqlite error: ', e.args[0])
	conn.commit()
	conn.close()
	

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    
    def __init__(self, start_time):
    	self.time = start_time
    
    def on_data(self, data):
	all_data = json.loads(data)
	textdata = all_data['text']
	cleanedText = cleanTweetText(textdata)
	storeTweet(cleanedText)

	#cleanedText = 'access guest guest apartment area area bathroom bed bed bed bed bed bedroom block coffee coffee coffee coffee entrance entry francisco free garden guest home house kettle kettle kitchen kitchen kitchen kitchen kitchen kitchen living located microwave neighborhood new park parking place privacy private queen room san separate separate shared space space space street suite time welcome'

	#createWordCloud(cleanedText)
	return True
        	

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener(start_time)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #this is for streaming:
    stream = Stream(auth, listener)
    stream.filter(track=['David Bowie','@DavidBowieReal'], languages=['en'], async=True)