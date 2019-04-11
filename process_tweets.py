import sqlite3
from sqlite3 import Error
from os import path, getcwd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

stopwords = set(STOPWORDS) 

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
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
    
def select_all_tweets(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    all_tweet_text = ""
    
    cur = conn.cursor()
    cur.execute("SELECT tweet_text FROM tweets")
 
    rows = cur.fetchall()
    
    for tweet_text in rows:
    	print(tweet_text)
 
    all_tweet_text = ','.join(str(tweet_text) for tweet_text in rows)
    
    print(all_tweet_text)
    
    return all_tweet_text
        

def main():
    database = "C:\\sqlite\\db\\tweets.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("getting tweets:")
        all_tweet_text = select_all_tweets(conn)
        createWordCloud(all_tweet_text)
 
 
if __name__ == '__main__':
    main()