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
        log.PrepareLog(indexId, f"{self.username}", "Member added to database", "/", "yes")
        id = indexId
        print("Member added\n")
      except sqlite3.Error as err:
        indexId = log.SystemCounter(id)
        # log database error
        log.PrepareLog(indexId, f"{self.username}", "Add user database error", "/", "yes")
        id = indexId
      return id

  def modifyMember(self, id):
      checkSum = 0
      x = True

      while True:
        memberModified = input("Please enter the member ID of the person you wish to change information of: ")
        uniqueID = regex.regexID(memberModified)
        checkSum = memberModified[-1]
        verifyCheckSum = 0

        for i in range(len(memberModified) - 1):
          verifyCheckSum += int(memberModified[i])

        if not uniqueID:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input member ID", "Invalid input: %s recorded as user input" % memberModified, "no")
            id = indexId
            print("Invalid member ID")
        elif (verifyCheckSum%10) != int(checkSum):
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input member ID", "Invalid input: %s recorded as user input" % memberModified, "no")
            id = indexId
            print("Invalid member ID")
        else:
            break
      #TODO: REMOVE ALL COMMENTS ABOUT USER SUCCESSFULLY CHANGED
      modifyChoice = input("[1] First name\n[2] Last name\n[3] Address\n[4] Email address\n[5] Phone Number\nPress [0] to return to main menu.\nWhat would you like to change: ")
      res = ""
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
                  sql = "UPDATE MEMBERS SET firstname = ? where id = ?"
                  res = modifiedFirstName
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
                  sql = "UPDATE members SET Lastname = ? WHERE id = ?"
                  res = modifiedLastName
                  break
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input last name", "Invalid input: %s recorded as user input" % modifiedLastName, "no")
                  id = indexId
                  print("Invalid input")
      
      if modifyChoice == "3":
          while True:
              modifiedStreet = input("Please enter new streetname: ")
              outcomeRE = regex.regexStreet(modifiedStreet)
              res = modifiedStreet
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input street name", "Invalid input: %s recorded as user input" % modifiedStreet, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  break
          while True:
              modifiedNumber = input("Please enter new house number: ")
              outcomeRE = regex.regexNumber(modifiedNumber)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input house number", "Invalid input: %s recorded as user input" % modifiedNumber, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  break

          while True:
              modifiedZipcode = input("And please enter the new zipcode: ")
              outcomeRE = regex.regexZipcode(modifiedZipcode)
              if not outcomeRE:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input zip code", "Invalid input: %s recorded as user input" % modifiedZipcode, "no")
                  id = indexId
                  print("Invalid input")
              elif outcomeRE:
                  res = f"{modifiedStreet} {modifiedNumber} {modifiedZipcode}"
                  sql = "UPDATE members SET Address = ? WHERE id = ?"
                  indexId = log.SystemCounter(id)
                  # log changed address
                  log.PrepareLog(indexId, "testname", "Successful change address", "Member address changed to: %s" % res, "no")
                  id = indexId
                  print(f"The address of member {memberModified} has been changed to {res}")
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
                  sql = "UPDATE members SET Email = ? WHERE id = ?"
                  res = modifiedEmail
                  break
              else:
                  indexId = log.SystemCounter(id)
                  # log invalid input
                  log.PrepareLog(indexId, "testname", "Invalid input email", "Invalid input: %s recorded as user input" % modifiedEmail, "no")
                  id = indexId
                  print("Invalid member ID")
                  
      if modifyChoice == "5":
        while True:
            modifiedPhone = input("Please enter new phonenumber (+31-6-DDDDDDDD): ")
            outcomeRE = regex.regexPhone(modifiedPhone)
            res = modifiedPhone
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
                sql = "UPDATE members SET MobileNumber = ? WHERE id = ?"
                res = modifiedPhone
                break 
      
      if modifyChoice == "0":
        return

      try:
        self.dbConn.cur.execute(sql, (Encrypt(res), memberModified))
        self.dbConn.conn.commit()
      except sqlite3.Error as err:
        print(err)
        indexId = log.SystemCounter(id)
        # log database error
        log.PrepareLog(indexId, f"{err}", "Update user database error", "/", "yes")
        id = indexId
        return id

      # Check if executed.
      if self.dbConn.cur.rowcount > 0:
        print("User updated\n")
        indexId = log.SystemCounter(id)
        # log user added
        log.PrepareLog(indexId, f"{self.username}", "User updated", "/", "no")
        id = indexId
      else:
        print("No rows affected\n")
        indexId = log.SystemCounter(id)
        # log user not added
        log.PrepareLog(indexId, f"{self.username}", "Updating user failed", "/", "no")
        id = indexId
        sleep(100)
      return id

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
    res = self.dbConn.cur.execute(sql, data)
    if res is None:
      print("Member not found.")
      indexId = log.SystemCounter(id)
      # log Search member
      log.PrepareLog(indexId, f"{self.username}", "Member not found", "/", "no")
      id = indexId

      return id

    for row in res:
      arr = []
      for i in range(len(row)):
        if (i == 0):
          arr.append(str(row[i]))
        else:
          arr.append(Decrypt(str(row[i])))
      user.append(arr)
  
    for row in user:
      print(row)
    exit(1)
    indexId = log.SystemCounter(id)
    # log Search member
    log.PrepareLog(indexId, f"{self.username}", "Members searched", "/", "no")
    id = indexId

    return id

    

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
    except sqlite3.Error as err:
      indexId = log.SystemCounter(id)
      # log invalid input
      log.PrepareLog(indexId, f"{self.username}", "Print users", "Error printing users", "yes")
      id = indexId
    return id
  
  def AddUser(self, id):
    # Clear console
    ClearConsole()

    # Create user profile
    while True:
      username     = CreateUsername()
      username     = Encrypt(username.lower())
      if (self.CheckUnique(username) == 1):
        indexId = log.SystemCounter(id)
        # log username
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
      role         = verifyInput("(advisor)", "Please enter the role of the user: ").lower()
    else:
      role       = verifyInput("(sysadmin|advisor|Advisor|Sysadmin)", "Please enter the role of the user: ").lower()
    firstname    = verifyInput("^[-a-zA-Z,']+$", "Please enter your first name: ").lower()
    lastname     = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter your last name: ").lower()
    registration = datetime.today().strftime('%d-%m-%Y')

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
      log.PrepareLog(indexId, f"{self.username}", "Add user database error", "/", "yes")
      id = indexId
      return id

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
    return id

  def GetUser(self, data, id):
    try:
      sql = '''SELECT * FROM users WHERE username = ? AND lastname = ?'''
      self.dbConn.cur.execute(sql, data)
      user = self.dbConn.cur.fetchone()

      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, f"{self.username}", "User fetched", "/", "no")
      id = indexId
    except sqlite3.Error as err:
      print(err)
      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, f"{self.username}", str(err), "Error occurred while fetching user", "no")
      id = indexId
    return user, id

  def UpdateUser(self, id):
    username = Encrypt(regex.regexUsername())
    lastname = Encrypt(verifyInput("^[-a-zA-Z,'\s]+$", "Please enter the lastname: "))
    user, id = self.GetUser((username, lastname), id)

    if user is None:
      print("User not found.")
      return id

    option = getValue()
    if option == 'role':
      sql = '''UPDATE users SET role = ? WHERE username = ? AND lastname = ?'''
      if self.role == "sysadmin":
        newValue     = verifyInput("(advisor)", "Please enter the role of the user: ")
      else:
        newValue     = verifyInput("(sysadmin|advisor)", "Please enter the role of the user: ") 
    elif option == 'lastname':
      sql = '''UPDATE users SET lastname = ? WHERE username = ? AND lastname = ?'''
      newValue = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter your last name: ")
    elif option == 'username':
      sql = '''UPDATE users SET username = ? WHERE username = ? AND lastname = ?'''
      newValue = regex.regexUsername()
    elif option == 'firstname':
      sql = '''UPDATE users SET firstname = ? WHERE username = ? AND lastname = ?'''
      newValue = verifyInput("^[-a-zA-Z,']+$", "Please enter the first name of the user: ")

    try:
      self.dbConn.cur.execute(sql, (Encrypt(newValue), username, lastname))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:
      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, f"{self.username}", str(err), "Error occurred while updating user", "no")
      id = indexId
      return id

    # Check if executed.
    if self.dbConn.cur.rowcount > 0:
      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, f"{self.username}", "User information updated", "", "no")
      id = indexId
      print("User updated\n")
    else:
      indexId = log.SystemCounter(id)
      # log user added
      log.PrepareLog(indexId, f"{self.username}",  "No information updated", "", "no")
      id = indexId
      print("No rows affected\n")
    return id

  def DeleteUser(self, id):
    # Clear console
    ClearConsole()

    username  = regex.regexUsername()
    firstname = verifyInput("^[-a-zA-Z,']+$", "Please enter the firstname of the user to be deleted: ")

    if self.role == "sysadmin":
      role = verifyInput("(advisor)", "Please enter the role of the user: ")
    else:
      role = verifyInput("(sysadmin|advisor)", "Please enter the role of the user: ")

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
    
    if self.dbConn.cur.rowcount > 0:
      print("User deleted\n")
      indexId = log.SystemCounter(id)
      # log Advisor deleted
      log.PrepareLog(indexId, f"{self.username}", "user deleted", f"Advisor: {username} deleted", "no")
      id = indexId
    else:
      print("No user deleted\n")
      indexId = log.SystemCounter(id)
      # log no advisor deleted
      log.PrepareLog(indexId, f"{self.username}", "No user deleted", f"Username: {username} was not deleted", "no")
      id = indexId

    return id

  def ResetPassword(self, id):
    tempPassword = "test123!"

    # Get username
    username = Encrypt(regex.regexUsername())

    # Get role
    role = verifyInput("(sysadmin|advisor|Sysadmin|Advisor)", "Please enter the role of the user: ").lower()

    if self.role == "sysadmin" and role != 'advisor':
      indexId = log.SystemCounter(id)
      # log incorrect password reset
      log.PrepareLog(indexId, f"{self.username}", "Reset password unauthorized", f"User tried to reset password of {username}", "yes")
      id = indexId

      print(unauthorized) #Remove statement for logging
      return id
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
        return id
      
      # Check if executed.
      if self.dbConn.cur.rowcount > 0:
        indexId = log.SystemCounter(id)
        # log password changed
        log.PrepareLog(indexId, f"{self.username}", "Password changed", f"User: {username}'s password was changed", "no")
        id = indexId
        print("The following password is set: test123!")
      else:
        indexId = log.SystemCounter(id)
        # log no password reset
        log.PrepareLog(indexId, f"{self.username}", "Password reset failed", f"Password of user {username} was not changed", "no")
        id = indexId
        print("Failed to change password")
      return id

  def BackupDB(self, id):
    # Log
    indexId = log.SystemCounter(id)
    log.PrepareLog(indexId, f"{self.username}", "Backup of system made", f"User {self.username} made a backup of the system", "no")
    id = indexId

    dst = "backup.db"

    # Create backup
    with sqlite3.connect(dst) as bck:
      self.dbConn.conn.backup(bck, pages=-1)
    
    # # Create zip
    with ZipFile("Backup.zip", 'w') as zip:
      zip.write("log.txt")
      zip.write(dst)
    
    # Remove backup file when zip created
    if (exists("Backup.zip") and exists(dst)):
      os.remove(dst)

  def RestoreBackup(self, id):
    backupName = "backup.db"
    standardName = "highlyClassified.db"
    if (not exists("Backup.zip")):
      # Log
      indexId = log.SystemCounter(id)
      log.PrepareLog(indexId, f"{self.username}", "No backup file found", "/", "no")
      id = indexId

      print(zipNotFound)
      return id

    if (exists(standardName)):
      os.remove(standardName)

    with ZipFile("Backup.zip") as zip:
      zip.extract("log.txt")
      zip.extract(backupName)

    os.rename(backupName, standardName)

    # Log
    indexId = log.SystemCounter(id)
    log.PrepareLog(indexId, f"{self.username}", "Backup restored", f"User {self.username} restored the system", "no")
    id = indexId
    return id
  
  #Is this relevant?
  def PrintLog(self):
    ClearConsole()
    if (exists("log.txt")):
      with open("log.txt", "r") as logfile:
        for line in logfile.readlines():
          print(line)
    else:
      print(genericError)

  def CheckUnique(self, data):
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

  def DeleteMember(self, id):
    # Clear the console
    ClearConsole()

    # Get user info
    firstname = verifyInput("^[-a-zA-Z,']+$", "Please enter the firstname: ").lower()
    lastname  = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter the lastname: ").lower()
    memberid  = verifyInput("^[0-9]+$", "Please enter the member ID: ")

    firstname = Encrypt(firstname)
    lastname  = Encrypt(lastname)
    memberid  = Encrypt(memberid)

    try:
      sql = '''DELETE FROM members WHERE firstname = ? AND lastname = ? AND id = ?'''
      self.dbConn.cur.execute(sql, (firstname, lastname, memberid))
      self.dbConn.conn.commit()
    except sqlite3.Error as err:
      indexId = log.SystemCounter(id)
      log.PrepareLog(indexId, f"{self.username}", str(err), "Error occurred while deleting member", "no")
      id = indexId
      return id

    if self.dbConn.cur.rowcount > 0:
      print("Member deleted\n")
      indexId = log.SystemCounter(id)
      log.PrepareLog(indexId, f"{self.username}", f"Member {firstname}", f"User {self.username} deleted a member", "no")
      id = indexId
    else:
      print("No rows affected\n")
      indexId = log.SystemCounter(id)
      log.PrepareLog(indexId, f"{self.username}", "No member deleted", f"User {self.username} tried to delete a member", "no")
      id = indexId
    return id



class SuperAdmin(SysAdmin):
  def __init__(self):
    super().__init__(username="superadmin", role="superadmin")




