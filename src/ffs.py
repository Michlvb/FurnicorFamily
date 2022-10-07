from typing import Tuple
from Database.database import Database
from UI import ui
from os import system
from Log import log
import re
import random
from unicodedata import digit
from utils import ClearConsole
from Log.log import Decrypt, Encrypt

from user import SuperAdmin, SysAdmin, User

from utils import ClearConsole

superadmin = "superadmin"
superadminpassword = "Admin321!"
role = "superadmin"
loggedIn = False
member = ""
members = ()        

def main():
  # initialize id for logging purposes
  id = 0

  ClearConsole()
  print("Welcome to the Furnicor Family System\n\nPlease choose one of the following options:\n(Enter the corresponding number)\n")
    
  choice = "0"
  # loop for menu choices login and exit
  while not (choice == "1" or choice == "2"):
    print("[1] to login")
    print("[2] to exit")
    user_input = input()

    # try except to check if user input is int
    try:
      temp = user_input
      int(temp)
      choice = temp
    except:
      pass

    # if else statement to check whether int input matches the available choices
    # kyljan1_2 - sgtriv9_0
    # Spleetoog1! - PmttwEwztl9~
    if(choice == "1"):
      user, id = login(id)
      if (user != None):
        id = id
        indexId = log.SystemCounter(id)
        # log menu choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Main Menu login chosen", "/", "no")
        id = indexId
        ui.mainMenu(user, id)
    # exit program
    elif(choice == "2"):
      exit()
    # else statement to log incorrect user input
    else:
      print("incorrect input, please try again")
      indexId= log.SystemCounter(id)
      # log incorrect user input
      log.PrepareLog(indexId, "testname%i" % indexId, "Main Menu incorrect input", "input: '%s' used as main menu choice" % user_input, "no")
      id= indexId

def decryptUser(data):
    decryptedData = []
    user = []
    for val in data:
        decryptedData.append(Decrypt(val))
    if (decryptedData[1] == "sysadmin"):
      user = SysAdmin(decryptedData[0], decryptedData[1])
    elif (decryptedData[1] == "advisor"):
      user = User(decryptedData[0], decryptedData[1])
    return user

def login(id):
    loginAttempt = 0
    x = True
    db = Database()
    while loginAttempt < 3:
        usernameTry = input("Username: ")
        passwordTry = input("Password: ")

        if (usernameTry == superadmin and passwordTry == superadminpassword):
          indexId = log.SystemCounter(id)
            # log log in successful
          log.PrepareLog(indexId, "testname", "Logged in", "/", "no")
          id = indexId
          return superadmin, id
        else:
          # Get user
          kweerieResult = db.getUser((Encrypt(usernameTry), Encrypt(passwordTry)))

        if (kweerieResult != None):
            user = decryptUser(kweerieResult)

            loginAttempt = 0
            print(user)

            indexId = log.SystemCounter(id)
            # log log in successful
            log.PrepareLog(indexId, "testname", "Logged in", "/", "no")
            id = indexId

            return user, id
        else:
            indexId = log.SystemCounter(id)
            # log unsuccessful login
            log.PrepareLog(indexId, "testname", "Unsuccessful login", 'Username: "%s" is used for a login attempt with a wrong password' % usernameTry, "no")
            id = indexId

            loginAttempt+=1
            print("Invalid login")
            
    indexId = log.SystemCounter(id)
    # log multiple incorrect logins
    log.PrepareLog(indexId, "testname", "Unsuccessful login", "Multiple usernames and passwords are tried in a row", "yes")
    id = indexId
    loggedIn = False

    print("Too many login attempts, try again later.")
    return loggedIn, id      

main()
