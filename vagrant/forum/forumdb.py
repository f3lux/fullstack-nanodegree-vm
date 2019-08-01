# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

POSTS = [("This is the first post.", datetime.datetime.now())]

def get_posts():
  """Return all posts from the 'database', most recent first."""
  connection = psycopg2.connect("dbname=forum")
  cursor = connection.cursor()
  cursor.execute(
  	"SELECT content, time FROM posts ORDER BY time DESC;")
  results = cursor.fetchall()
  connection.close()
  return results

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  connection = psycopg2.connect("dbname=forum")
  cursor = connection.cursor()
  cursor.execute(
  	"INSERT INTO posts VALUES(%s)", (bleach.clean(content),))
  connection.commit()
  connection.close()


