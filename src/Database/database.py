import sqlite3
from zipfile import ZipFile
import os
from os.path import basename, exists
from utils import ClearConsole
from messages import unauthorized

# TODO: Create local DB
# TODO: Fill in user data to local DB
# # Open a database in read-only mode.
# "file:template.db?mode=ro"

class Database:
  def __init__(self):
    if (not exists("highlyClassified.db")):
      self.conn = sqlite3.connect("highlyClassified.db")
      self.cur = self.conn.cursor()
      self.cur.execute("CREATE TABLE members (Id text, Firstname text, Lastname text, Address text, Email text, MobileNumber number, RegisteredOn text)")
      self.cur.execute("CREATE TABLE users (username number, password text, role text, firstname text, lastname text, registeredOn text)")
      self.conn.commit()
    else:
      self.conn = sqlite3.connect("highlyClassified.db")
      self.cur = self.conn.cursor()

  def getUser(self, data):
    try:
      sql = '''SELECT username, role, firstname, lastname FROM users WHERE username = ? AND password = ?'''
      self.cur.execute(sql, (data))
      user = self.cur.fetchone()
    except sqlite3.Error as err:
      # TODO: Add Logging
      print(err)
    return user
    

  # Close connection
  def Close(self):
    self.conn.close()
