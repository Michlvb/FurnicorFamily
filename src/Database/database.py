import sqlite3
from zipfile import ZipFile
import os
from os.path import basename, exists
from utils import ClearConsole
from messages import unauthorized
from Log import log

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

  def getUser(self, data, id):
    try:
      sql = '''SELECT username, role, firstname, lastname FROM users WHERE username = ? AND password = ?'''
      self.cur.execute(sql, (data))
      user = self.cur.fetchone()
      indexId = log.SystemCounter(id)
      log.PrepareLog(indexId, "DATABASE", "fetched user from db", "/", "no")
      id = indexId
      return user, id
    except sqlite3.Error as err:
      print(err)
      indexId = log.SystemCounter(id)
      log.PrepareLog(indexId, "DATABASE", str(err), "Error occurred while getting user", "no")
      id = indexId
      return id
    

  # Close connection
  def Close(self):
    self.conn.close()
