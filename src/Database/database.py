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
    pathToDb = os.path.join("Database", "highlyClassified.db")
    print(pathToDb)
    if (not exists(pathToDb)):
      self.conn = sqlite3.connect(pathToDb)
      self.cur = self.conn.cursor()
      self.cur.execute("CREATE TABLE members (Id number, Firstname text, Lastname text, Address text, Email text, MobileNumber number, RegisteredOn text)")
      self.cur.execute("CREATE TABLE users (username text, password text, role text, firstname text, lastname text, registeredOn text)")
      self.conn.commit()
    else:
      self.conn = sqlite3.connect(pathToDb)
      self.cur = self.conn.cursor()

  # Close connection
  def Close(self):
    self.conn.close()
