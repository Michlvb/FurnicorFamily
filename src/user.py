import os
from os.path import exists
from datetime import datetime
import sqlite3
from time import sleep
from Database.database import Database
from messages import unauthorized, genericError, zipNotFound, searchMsg
from utils import ClearConsole, CreatePassword, CreateUsername, verifyInput, SearchParams, ValidateOptionValue, chooseCity, getValue
from zipfile import ZipFile
from Log.log import Encrypt, Decrypt
from Log import log
import regex
from regex import idGenerate

class User:
  def __init__(self, username="", role="advisor"):
    self.username = username
    self.role     = role
    self.dbConn   = Database()

  def addMember(self, id):
      while True:    
        firstName = input("What is your first name: ")
        outcomeRe = regex.regexName(firstName)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input first name", "Invalid input: %s recorded as user input" % firstName, "no")
            id = indexId
            print("Invalid input")
        else:
            break

      while True:    
        lastName = input("What is your last name: ")
        outcomeRe = regex.regexName(lastName)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input last name", "Invalid input: %s recorded as user input" % lastName, "no")
            id = indexId
            print("Invalid input")
        elif len(lastName) == 1:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input last name", "Invalid input: %s recorded as user input" % lastName, "no")
            id = indexId
            print("Invalid input")
        else:
            break

      while True:     
        streetName = input("What is your streetname: ")
        outcomeRe = regex.regexStreet(streetName)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input address", "Invalid input: %s recorded as user input" % streetName, "no")
            id = indexId
            print("Invalid input")
        elif len(streetName) <= 3:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input address", "Invalid input: %s recorded as user input" % streetName, "no")
            id = indexId
            print("Invalid Input")
        else:
            break

      while True:
        houseNumber = input("What is your house number: ")
        outcomeRe = regex.regexNumber(houseNumber)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input house number", "Invalid input: %s recorded as user input" % houseNumber, "no")
            id = indexId
            print("Invalid Input")
        else:
            break

      while True:
        zipcode = input("What is your zipcode (XXXX YY): ")
        outcomeRe = regex.regexZipcode(zipcode)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input zip code", "Invalid input: %s recorded as user input" % zipcode, "no")
            id = indexId
            print("Invalid input")
        else:
            break
        
      # Another input field to ask the user from which city they are.(at least they can choose from 10 different cities)
      city = chooseCity()
      address = f"{streetName} {houseNumber} {zipcode} {city}"

      while True:
        emailAddress = input("What is your email address: ")
        outcomeRe = regex.regexEmail(emailAddress)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input email", "Invalid input: %s recorded as user input" % emailAddress, "no")
            id = indexId
            print("Invalid input")
        else:
            break
      
      #TODO: Check add mobile number
      while True:    
        mobilePhone = input("Enter your phone number (+31-6-DDDDDDDD): ")
        outcomeRe = regex.regexPhone(mobilePhone)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input phone number", "Invalid input: %s recorded as user input" % mobilePhone, "no")
            id = indexId
            print("Invalid input")
        else:
            break

      #Created ID and registration
      uniqueId = idGenerate()
      registration = datetime.today().strftime('%d-%m-%Y')

      sql = """INSERT INTO members VALUES (?, ?, ?, ?, ?, ?, ?)"""
      try:
        self.dbConn.cur.execute(sql, (uniqueId, Encrypt(firstName), Encrypt(lastName), Encrypt(address), 
                                      Encrypt(emailAddress), Encrypt(mobilePhone), registration))
        self.dbConn.conn.commit()

        indexId = log.SystemCounter(id)
        # log member add. KYLIAN WHY IS THIS "YES"?
        log.PrepareLog(indexId, f"{self.username}", "Member added to database", "/", "yes")
        id = indexId
      except sqlite3.Error as err:
        indexId = log.SystemCounter(id)
        # log database error
        log.PrepareLog(indexId, f"{self.username}", "Add user database error", "/", "yes")
        id = indexId

  def modifyMember(self, id):
      checkSum = 0;
      x = True

      while True:
          memberModified = input("Please enter the member ID of the person you wish to change information of: ")
          outcomeRE = regex.regexID(memberModified)

          for i in (range(len(memberModified)-1)):
              checkSum = (checkSum + int(memberModified[i]))%10

          if not outcomeRE:
              indexId = log.SystemCounter(id)
              # log invalid input
              log.PrepareLog(indexId, "testname", "Invalid input member ID", "Invalid input: %s recorded as user input" % memberModified, "no")
              id = indexId
              print("Invalid member ID")
          elif len(memberModified) != 10:
              indexId = log.SystemCounter(id)
              # log invalid input
              log.PrepareLog(indexId, "testname", "Invalid input member ID", "Invalid input: %s recorded as user input" % memberModified, "no")
              id = indexId
              print("Invalid member ID")
          elif int(memberModified)%10 != checkSum:
              indexId = log.SystemCounter(id)
              # log invalid input
              log.PrepareLog(indexId, "testname", "Invalid input member ID", "Invalid input: %s recorded as user input" % memberModified, "no")
              id = indexId
              print("Invalid member ID")
          else:
              break

      modifyChoice = input("[1] First name\n[2] Last name\n[3] Address\n[4] Email address\n[5] Phone Number\nPress [0] to return to main menu.\nWhat would you like to change:")
      if modifyChoice == "1":
          while True:
              modifiedFirstName = input("Please enter new first name: ")
              outcomeRE = regex.regexName(modifiedFirstName)

              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input first name", "Invalid input: %s recorded as user input" % modifiedFirstName, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log first name change
                  log.PrepareLog(indexId, "testname", "Member first name changed", "Member first name changed to: %s" % modifiedFirstName, "no")
                  id = indexId
                  print(f"First name of member {memberModified} has been changed to {modifiedFirstName}")
                  break
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input first name", "Invalid input: %s recorded as user input" % modifiedFirstName, "no")
                  id = indexId
                  print("Invalid input")
                  
      if modifyChoice == "2":
          while True:
              modifiedLastName = input("Please enter new last name: ")
              outcomeRE = regex.regexName(modifiedLastName)

              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input last name", "Invalid input: %s recorded as user input" % modifiedLastName, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log first name change
                  log.PrepareLog(indexId, "testname", "Member last name changed", "Member last name changed to: %s" % modifiedLastName, "no")
                  id = indexId
                  print(f"Last name of member {memberModified} has been changed to {modifiedLastName}")
                  break
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input last name", "Invalid input: %s recorded as user input" % modifiedLastName, "no")
                  id = indexId
                  print("Invalid input")
                  
      if modifyChoice == "3":
          while x:
              modifiedStreet = input("Please enter new streetname: ")
              outcomeRE = regex.regexStreet(modifiedStreet)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input street name", "Invalid input: %s recorded as user input" % modifiedStreet, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  x = False
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input street name", "Invalid input: %s recorded as user input" % modifiedStreet, "no")
                  id = indexId
                  print("Invalid member ID")

              modifiedNumber = input("Please enter new house number: ")
              outcomeRE = regex.regexNumber(modifiedNumber)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input house number", "Invalid input: %s recorded as user input" % modifiedNumber, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  x = False
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input house number", "Invalid input: %s recorded as user input" % modifiedNumber, "no")
                  id = indexId
                  print("Invalid input")

              modifiedZipcode = input("And please enter the new zipcode: ")
              outcomeRE = regex.regexZipcode(modifiedZipcode)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input zip code", "Invalid input: %s recorded as user input" % modifiedZipcode, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  address = f"{modifiedStreet} {modifiedNumber} {modifiedZipcode}"
                  indexId = log.SystemCounter(id)
                  # log changed address
                  log.PrepareLog(indexId, "testname", "Successful change address", "Member address changed to: %s" % address, "no")
                  id = indexId
                  print(f"The address of member {memberModified} has been changed to {address}")
                  break
              
      if modifyChoice == "4":
          while True:
              modifiedEmail = input("Please enter new email: ")
              outcomeRE = regex.regexEmail(modifiedEmail)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input email", "Invalid input: %s recorded as user input" % modifiedEmail, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log email changed
                  log.PrepareLog(indexId, "testname", "Successful change email", "Member email changed to: %s" % modifiedEmail, "no")
                  id = indexId
                  print(f"The email of member {memberModified} has been changed into {modifiedEmail}")
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input email", "Invalid input: %s recorded as user input" % modifiedEmail, "no")
                  id = indexId
                  print("Invalid member ID")
                  
      if modifyChoice == "5":
          while True:
              modifiedPhone = input("Please enter new phonenumber: ")
              outcomeRE = regex.regexPhone(modifiedPhone)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input phone number", "Invalid input: %s recorded as user input" % modifiedPhone, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log changed phone number
                  log.PrepareLog(indexId, "testname", "Successful change phone number", "Member phone number changed to: %s" % modifiedPhone, "no")
                  id = indexId
                  print(f"The phonenumber of member {memberModified} has been changed into {modifiedPhone}")
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input phone number", "Invalid input: %s recorded as user input" % modifiedPhone, "no")
                  id = indexId
                  print("Invalid member ID")   
      
      if modifyChoice == "0":
        return    

  def updatePassword(self, id):
    if not (self.role == 'superadmin'):
      password = Encrypt(CreatePassword())
      try:
        # Check what happens when password not equal
        self.dbConn.cur.execute('SELECT password FROM users WHERE username = ? AND role = ?', (Encrypt(self.username), Encrypt(self.role)))
        oldPassword = self.dbConn.cur.fetchone()

        if oldPassword is None:
          indexId = log.SystemCounter(id)
          # log password updated
          log.PrepareLog(indexId, f"{self.username}", "User not found", "", "no")
          id = indexId
          return
        
        sql = '''UPDATE users SET password = ? WHERE username = ? AND password = ?'''
        self.dbConn.cur.execute(sql, (password, Encrypt(self.username), oldPassword[0]))
        self.dbConn.conn.commit()

        indexId = log.SystemCounter(id)
        # log password updated
        log.PrepareLog(indexId, f"{self.username}", f"User: {self.username}'s password updated", "", "no")
        id = indexId
      except sqlite3.Error as err:

        indexId = log.SystemCounter(id)
        # log incorrect input update password
        log.PrepareLog(indexId, f"{self.username}", "Incorrect input", f"Attempt to change password to {password}", "yes")
        id = indexId

        print(err)
    else:
      indexId = log.SystemCounter(id)
      # log Super admin tried to change password
      log.PrepareLog(indexId, f"{self.username}", "Incorrect menu choice", "Super Admin attempted to access update password", "no")
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
    # Still need to check with mail setup correctly
    user = []
    for res in self.dbConn.cur.execute(sql, data):
      for value in res:
        user.append(Decrypt(str(value)))
    
    if user == []:
      print("User not found.")
      indexId = log.SystemCounter(id)
      # log Search member
      log.PrepareLog(indexId, f"{self.username}", "Member not found", "/", "no")
      id = indexId
      while True:
        user_response = input("Press x to return to main menu: ")
        # try except to check if user input is int
        try:
            if (user_response == 'x'):
              break
        except:
            pass
      return
    
    print(f"User details:\nId: {user[0]}\nFirstname: {user[1]}\nLastname: {user[2]}\nAddress: {user[3]}\nEmail: {user[4]}\nMobileNumber: {user[5]}\n")

    indexId = log.SystemCounter(id)
    # log Search member
    log.PrepareLog(indexId, f"{self.username}", "Members searched", "/", "no")
    id = indexId

    while True:  
      user_response = input("Press x to return to main menu: ")
      # try except to check if user input is int
      try:
          if (user_response == 'x'):
            break
      except:
          pass
    

class SysAdmin(User):
  def __init__(self, username, role):
    super().__init__(username, role)
  
  def PrintUsers(self, id):
    ClearConsole()
    sql = '''SELECT username, role FROM users'''
    try:
      for username, role in self.dbConn.cur.execute(sql):
        print(f"Username: {Decrypt(username)} has role: {Decrypt(role)}\n")
  
      indexId = log.SystemCounter(id)
      # log print users
      log.PrepareLog(indexId, f"{self.username}", "Print users", "/", "no")
      id = indexId

      while True:  
        user_response = input("Press x to return to main menu: ")
        # try except to check if user input is int
        try:
            if (user_response == 'x'):
                break
        except:
            pass  

    except sqlite3.Error as err:
      indexId = log.SystemCounter(id)
      # log invalid input
      log.PrepareLog(indexId, f"{self.username}", "Print users", "Error printing users", "yes")
      id = indexId

      print(err)
  
  def AddUser(self, id):
    # Clear console
    ClearConsole()

    # Create user profile
    while True:
      username     = CreateUsername()
      username     = Encrypt(username.lower())
      if (self.CheckUnique(username) == 1):
        #Mayb add prepare log here?
        indexId = log.SystemCounter(id)
        # log username was taken
        log.PrepareLog(indexId, f"{self.username}", f"{username} created", "username ", "no")
        id = indexId
        break
      else:
        indexId = log.SystemCounter(id)
        # log username was taken
        log.PrepareLog(indexId, f"{self.username}", "Add user username taken", f"username {username} was taken", "no")
        id = indexId

        print("Taken.")
        continue
    
    password     = CreatePassword()
    if self.role == "sysadmin":
      role         = verifyInput("(advisor)", "Please enter the role of the user: ")
    else:
      role       = verifyInput("(sysadmin|advisor|Advisor|Sysadmin)", "Please enter the role of the user: ")
    firstname    = verifyInput("^[-a-zA-Z,']+$", "Please enter your firstname: ")
    lastname     = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter your lastname: ")
    registration = datetime.today().strftime('%d-%m-%Y')

    # TODO: add encryption - DONE
    password     = Encrypt(password)
    role         = Encrypt(role.lower())
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
      log.PrepareLog(indexId, f"{self.username}", "Add user database error", "/", "yes")
      id = indexId
      return

    # Check if executed.
    if self.dbConn.cur.rowcount > 0:
      print("User added\n")

      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, f"{self.username}", "New user added", f"Member {username} added to the system", "no")
      id = indexId

    else:
      print("No rows affected\n")

      indexId = log.SystemCounter(id)
      # log user not added
      log.PrepareLog(indexId, f"{self.username}", "Add user failed", "/", "no")
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
      newValue = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter your lastname: ")

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

    username  = regex.regexUsername()
    firstname = verifyInput("^[-a-zA-Z,']+$", "Please enter the firstname of the user: ")

    if self.role == "sysadmin":
      role = verifyInput("(advisor)", "Please enter the role of the user: ")
    else:
      role = verifyInput("(sysadmin|advisor)", "Please enter the role of the user: ")

    #TODO: add encrypt
    username  = Encrypt(username)
    firstname = Encrypt(firstname)
    role      = Encrypt(role)

    try:
      sql = '''DELETE FROM users WHERE username = ? AND role = ? AND firstname = ?'''
      self.dbConn.cur.execute(sql, (username, role, firstname))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:
      indexId = log.SystemCounter(id)
      # log incorrect input
      log.PrepareLog(indexId, f"{self.username}", "Delete user failed", "Incorrect input", "yes")
      id = indexId
    
    # TODO: Add logging under both prints
    if self.dbConn.cur.rowcount > 0:
      indexId = log.SystemCounter(id)
      # log Advisor deleted
      log.PrepareLog(indexId, f"{self.username}", "Advisor deleted", f"Advisor: {username} deleted", "no")
      id = indexId
    else:
      indexId = log.SystemCounter(id)
      # log no advisor deleted
      log.PrepareLog(indexId, f"{self.username}", "No Advisor deleted", f"Username: {username} was not deleted", "no")
      id = indexId

    return id

  def ResetPassword(self, id):
    tempPassword = "test123!"

    # # Get username
    username = Encrypt(regex.regexUsername())

    # Get role
    role = verifyInput("(sysadmin|advisor|Sysadmin|Advisor)", "Please enter the role of the user: ").lower()

    if self.role == "sysadmin" and role != 'advisor':
      indexId = log.SystemCounter(id)
      # log incorrect password reset
      log.PrepareLog(indexId, f"{self.username}", "Reset password error", f"User tried to reset password of {username}", "yes")
      id = indexId

      print(unauthorized) #Remove statement for logging
      return
    else:
      try:
        sql = '''UPDATE USERS SET password = ? WHERE username = ? AND role = ?'''
        self.dbConn.cur.execute(sql, (tempPassword, username, Encrypt(role)))
        self.dbConn.conn.commit()
      except sqlite3.Error as err:
        indexId = log.SystemCounter(id)
        # log invalid input
        log.PrepareLog(indexId, f"{self.username}", f"{err}", "/", "yes")
        id = indexId
      
      # Check if executed.
      if self.dbConn.cur.rowcount > 0:
        indexId = log.SystemCounter(id)
        # log password changed
        log.PrepareLog(indexId, f"{self.username}", "Password changed", f"User: {username}'s password was changed", "no")
        id = indexId
        print("password successfully changed")

      else:
        indexId = log.SystemCounter(id)
        # log no password reset
        log.PrepareLog(indexId, f"{self.username}", "Password reset failed", f"Password of user {username} was not changed", "no")
        id = indexId
        print("Failed to change password")
    

  def LogBackup(self, status, remaining, total):
    # TODO: Add logging
    # Send data to log function
    print(f'Copied {total-remaining} of {total} pages...')

  def BackupDB(self, id):
    # Log
    indexId = log.SystemCounter(id)
    log.PrepareLog(indexId, f"{self.username}", "Backup of system made", f"User {self.username} made a backup of the system", "no")
    id = indexId

    backupName = "BackUp.db"

    # Create backup
    with sqlite3.connect(backupName) as bck:
      self.dbConn.conn.backup(bck, pages=-1, progress=self.LogBackup)
    
    # Create zip
    with ZipFile("Backup.zip", 'w') as zip:
      zip.write("log.txt")
      zip.write(backupName)
    
    # Remove backup file when zip created
    if (exists("Backup.zip") and exists(backupName)):
      os.remove(backupName)

  def RestoreBackup(self, id):
    # Log
    indexId = log.SystemCounter(id)
    log.PrepareLog(indexId, f"{self.username}", "Backup restored", f"User {self.username} restored the system", "no")
    id = indexId
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
    super().__init__(username="superadmin", role="superadmin")




