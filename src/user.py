import re
import os
from os.path import exists
from datetime import datetime
import sqlite3
from Database.database import Database
from messages import unauthorized, genericError, zipNotFound, searchMsg
from utils import ClearConsole, CreatePassword, CreateUsername, verifyInput, SearchParams, ValidateOptionValue, chooseCity, getValue
from zipfile import ZipFile
from Log.log import Encrypt, Decrypt
from Log import log

class User:
  def __init__(self, username="", password="", role="advisor"):
    self.username = username #Add validate username check
    self.password = password #Add password validate check
    self.role     = role
    self.dbConn   = Database()

  # TODO: Validate func
  def updatePassword(self, id):
    if not (self.role == 'superadmin'):
      password = Encrypt(CreatePassword())
      try:
        # Check what happens when password not equal
        sql = '''UPDATE users SET password = ? WHERE username = ? AND password = ?'''
        self.dbConn.cur.execute(sql, (password, Encrypt(self.username), Encrypt(self.password)))
        self.dbConn.conn.commit()
        self.password = password

        indexId = log.SystemCounter(id)
        # log password updated
        log.PrepareLog(indexId, "{self.username}", "User: {self.username}'s password updated", "", "no")
        id = indexId

      except sqlite3.Error as err:

        indexId = log.SystemCounter(id)
        # log incorrect input update password
        log.PrepareLog(indexId, "{self.username}", "Incorrect input", "Attempt to change password to {password}", "yes")
        id = indexId

        print(err)
    else:
      indexId = log.SystemCounter(id)
      # log Super admin tried to change password
      log.PrepareLog(indexId, "{self.username}", "Incorrect menu choice", "Super Admin attempted to access update password", "no")
      id = indexId

      print(unauthorized)
  
  def SearchMember(self, id):
    ClearConsole()
    print(searchMsg)
    
    # Get options
    options = SearchParams()

    # Create dict (easy to add the right input from user later)
    memberInfo = {"id": "", "firstname": "", "lastname": "", "address": "", "email": "", "phone": ""}

    # Check if options not equal 0. If not, then loop over the options and ask user input
    if len(options) == 0:
      print("No options provided")
      return
    else:
      for i in range(len(options)):
        # Setting Encryption
        memberInfo[options[i]] = Encrypt(ValidateOptionValue(options[i]))

    # This should be illegal
    data = tuple(memberInfo.values())

    sql = """
      SELECT * FROM members
      WHERE (Id LIKE '%' || ? || '%')
        AND (firstname LIKE '%' || ? || '%')
        AND (lastname LIKE '%' || ? || '%')
        AND (address LIKE '%' || ? || '%')
        AND (email LIKE '%' || ? || '%')
        AND (mobilenumber LIKE '%' || ? || '%')
      """
    # Execute sql and loop over the result
    for res in self.dbConn.cur.execute(sql, data):
      print(res)

    indexId = log.SystemCounter(id)
    # log Search member
    log.PrepareLog(indexId, "{self.username}", "Members searched", "/", "no")
    id = indexId

class SysAdmin(User):
  def __init__(self, username="", password="", role=""):
    super().__init__(username, password, role)
  
  def PrintUsers(self, id):
    ClearConsole()
    sql = '''SELECT username, role FROM users'''
    try:
      for username, role in self.dbConn.cur.execute(sql):
        print(f"Username: {Decrypt(username)} has role: {Decrypt(role)}\n")

      indexId = log.SystemCounter(id)
      # log print users
      log.PrepareLog(indexId, "{self.username}", "Print users", "/", "no")
      id = indexId

    except sqlite3.Error as err:
      indexId = log.SystemCounter(id)
      # log invalid input
      log.PrepareLog(indexId, "{self.username}", "Print users", "Error printing users", "yes")
      id = indexId

      print(err)
  
  def AddUser(self, id):
    # Clear console
    ClearConsole()

    # Create user profile
    while True:
      username     = CreateUsername()
      username     = Encrypt(username)
      if (self.CheckUnique(username) == 1):
        break
      else:

        indexId = log.SystemCounter(id)
        # log username was taken
        log.PrepareLog(indexId, "{self.username}", "Add user username taken", "username {username} was taken", "no")
        id = indexId

        print("Taken.")
        continue
    
    password     = CreatePassword()
    if self.role == "sysadmin":
      role         = verifyInput("(advisor)", "Please enter the role of the user: ")
    else:
      role         = verifyInput("(sysadmin|advisor)", "Please enter the role of the user: ")
    firstname    = verifyInput("^[-a-zA-Z,']+$", "Please enter your firstname: ")
    lastname     = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter youir lastname: ")
    registration = datetime.today().strftime('%d-%m-%Y')

    # TODO: add encryption - DONE
    password     = Encrypt(password)
    role         = Encrypt(role)
    firstname    = Encrypt(firstname)
    lastname     = Encrypt(lastname)
    registration = Encrypt(registration)

    # Send data to db
    try:
      sql = """INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)"""
      self.dbConn.cur.execute(sql, (username, password, role, firstname, lastname, registration))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:

      indexId = log.SystemCounter(id)
      # log database error
      log.PrepareLog(indexId, "{self.username}", "Add user database error", "/", "yes")
      id = indexId

      print(err)
      return

    # Check if executed.
    if self.dbConn.cur.rowcount > 0:
      print("User added\n")

      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, "{self.username}", "New user added", "Member {username} added to the system", "no")
      id = indexId

    else:
      print("No rows affected\n")

      indexId = log.SystemCounter(id)
      # log user not added
      log.PrepareLog(indexId, "{self.username}", "Add user failed", "/", "no")
      id = indexId

  def GetUser(self, data):
    try:
      sql = '''SELECT * FROM users WHERE username = ? AND lastname = ?'''
      self.dbConn.cur.execute(sql, data)
      user = self.dbConn.cur.fetchone()
    except sqlite3.Error as err:
      # TODO: Add Logging
      print(err)
    return user

  #TODO:  CHECK UPDATE USER
  def UpdateUser(self):
    username = Encrypt(CreateUsername())
    lastname = Encrypt(verifyInput("^[-a-zA-Z,'\s]+$", "Please enter the lastname: "))
    user = self.GetUser((username, lastname))

    if user is None:
      # TODO: Log
      # BAsically user not found
      return

    option = getValue()
    if option == 'role':
      sql = '''UPDATE users SET role = ?'''
      if self.role == "sysadmin":
        newValue     = verifyInput("(advisor)", "Please enter the role of the user: ")
      else:
        newValue     = verifyInput("(sysadmin|advisor)", "Please enter the role of the user: ") 
    elif option == 'lastname':
      sql = '''UPDATE users SET lastname = ?'''
      newValue = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter youir lastname: ")

    try:
      self.dbConn.cur.execute(sql, (newValue, ))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:
      # TODO: Add logging
      print(err)
   

    # Check if executed.
    if self.dbConn.cur.rowcount > 0:
      # TODO: Add logging
      print("User updated\n")
    else:
      print("No rows affected\n")

  def DeleteUser(self, id):
    # Clear console
    ClearConsole()

    # TODO: MAYBE CHANGE CHECK FOR ATTEMPTS WITH ROLE, SO THAT YOU CAN'T TRY INDEFINITELY
    # TODO: Use sys exit maybe?
    # TODO: Add firstname or lastname,extra security?
    username  = CreateUsername()
    firstname = verifyInput("^[-a-zA-Z,']+$", "Please enter your firstname: ")

    if self.role == "sysadmin":
      role         = verifyInput("(advisor)", "Please enter the role of the user: ")
    else:
      role         = verifyInput("(sysadmin|advisor)", "Please enter the role of the user: ")

    #TODO: add encrypt
    username  = Encrypt(username)
    firstname = Encrypt(firstname)
    role      = Encrypt(role)

    try:
      sql = '''DELETE FROM users WHERE username = ?, role = ?, firstname = ?'''
      self.dbConn.cur.execute(sql, (username, role, firstname))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:

      indexId = log.SystemCounter(id)
      # log incorrect input
      log.PrepareLog(indexId, "{self.username}", "Delete user failed", "Incorrect input", "yes")
      id = indexId
      print(err)
    
    # TODO: Add logging under both prints
    if self.dbConn.cur.rowcount > 0:
      print("Advisor deleted\n")

      indexId = log.SystemCounter(id)
      # log Advisor deleted
      log.PrepareLog(indexId, "{self.username}", "Advisor deleted", "Advisor: {username} deleted", "no")
      id = indexId

    else:
      print("No rows affected\n")

      indexId = log.SystemCounter(id)
      # log no advisor deleted
      log.PrepareLog(indexId, "{self.username}", "No Advisor deleted", "Username: {username} was not deleted", "no")
      id = indexId

  def ResetPassword(self, id):
    tempPassword = "test123!"

    # Get username
    username = Encrypt(CreateUsername())

    # Get role
    role = Encrypt(verifyInput("(sysadmin|advisor)", "Please enter the role of the user: "))

    if self.role == "sysadmin" and role != "advisor":
      indexId = log.SystemCounter(id)
      # log incorrect password reset
      log.PrepareLog(indexId, "{self.username}", "Reset password error", "User tried to reset password of {username}", "yes")
      id = indexId

      print(unauthorized) #Remove statement for logging
      return
    else:
      try:
        sql = '''UPDATE USERS SET password = ? WHERE username = ? AND role = ?'''
        self.dbConn.cur.execute(sql, (tempPassword, username, role))
        self.dbConn.conn.commit()
      except sqlite3.Error as err:
        indexId = log.SystemCounter(id)
        # log invalid input
        log.PrepareLog(indexId, "{self.username}", "Reset password invalid input", "/", "yes")
        id = indexId

        print(err)
      
      # Check if executed.
      if self.dbConn.cur.rowcount > 0:
        print("Pass changed\n")

        indexId = log.SystemCounter(id)
        # log password changed
        log.PrepareLog(indexId, "{self.username}", "Password changed", "User: {username}'s password was changed", "no")
        id = indexId

      else:
        print("No rows affected\n")

        indexId = log.SystemCounter(id)
        # log no password reset
        log.PrepareLog(indexId, "{self.username}", "Password reset failed", "Password of user {username} was not changed", "no")
        id = indexId
    

  def LogBackup(self, status, remaining, total):
    # TODO: Add logging
    # Send data to log function
    print(f'Copied {total-remaining} of {total} pages...')

  def BackupDB(self):
    backupName = "highlyClassified.db"

    # Create backup
    with sqlite3.connect(backupName) as bck:
      self.dbConn.conn.backup(bck, pages=1, progress=self.LogBackup)
    
    # Create zip
    with ZipFile("Backup.zip", 'w') as zip:
      zip.write("log.txt")
      zip.write(backupName)
    
    # Remove backup file when zip created
    if (exists("Backup.zip") and exists(backupName)):
      os.remove(backupName)

  def RestoreBackup(self):
    # Restore files (it overrides the current files)
    backupName = "highlyClassified.db"
    if (not exists("Backup.zip")):
      print(zipNotFound)
      return

    PathToUnzip = "Database"
    with ZipFile("Backup.zip") as zip:
      zip.extract("log.txt")
      zip.extract(backupName, path=PathToUnzip)

  def PrintLog(self):
    ClearConsole()
    if (exists("log.txt")):
      with open("log.txt", "r") as logfile:
        for line in logfile.readlines():
          print(line)
    else:
      print(genericError)

  def CheckUnique(self, data):
    # TODO: Add check to see if user is unique
    sql = """
      SELECT username FROM users
      WHERE username = ?
    """
    for res in self.dbConn.cur.execute(sql, (data,)):
      if res[0] == data:
        return 0
      else:
        return 1
    return 1

  def DeleteMember(self):
    # Clear the console
    ClearConsole()

    # Get user info
    firstname = verifyInput("^[-a-zA-Z,']+$", "Please enter the firstname: ")
    lastname  = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter the lastname: ")
    memberid  = verifyInput("^[1-9]+$", "Please enter the member ID: ")

    # TODO: Add encryption
    firstname = Encrypt(firstname)
    lastname  = Encrypt(lastname)
    memberid  = Encrypt(memberid)

    try:
      sql = '''DELETE FROM members WHERE Firstname = ? AND Lastname = ? AND Id = ?'''
      self.dbConn.cur.execute(sql, (firstname, lastname, memberid))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:
      print(err) 

    # Check if executed.
    # TODO: Logging
    if self.dbConn.cur.rowcount > 0:
      print("Member deleted\n")
    else:
      print("No rows affected\n")



class SuperAdmin(SysAdmin):
  def __init__(self):
    super().__init__(username="superadmin", password="Admin321!", role="superadmin")




