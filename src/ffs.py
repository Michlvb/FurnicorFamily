from UI import ui
from os import system
from Log import log
import re
import random
from unicodedata import digit
from utils import ClearConsole
from user import SuperAdmin

username = "superadmin"
password = "Admin321!"
role = "SuperAdmin"
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
    if(choice == "1"):
      role = "SuperAdmin" # hard coded for testing purposes
      loggedIn = login(id)
      if (loggedIn[0] == True):
        id = loggedIn[1]
        indexId = log.SystemCounter(id)
        # log menu choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Main Menu login chosen", "/", "no")
        id = indexId
        # navigate to main menu from ui
        # addMember(id)
        user = SuperAdmin()
        user.modifyMember(id)
        ui.mainMenu(role, id)
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

def login(id):
    loginAttempt = 0
    x = True
    while loginAttempt < 3:
        usernameTry = input("Username: ") # TODO: REGEX
        passwordTry = input("Password: ") # TODO: REGEX
        # TODO: if else statement
        if usernameTry == username and passwordTry == password:
            loggedIn = True
            loginAttempt = 0
            print("Login succesful")

            indexId = log.SystemCounter(id)
            # log log in successful
            log.PrepareLog(indexId, "testname", "Logged in", "/", "no")
            id = indexId
            return loggedIn, id
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

