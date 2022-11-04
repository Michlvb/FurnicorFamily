from time import sleep
from typing import Tuple
from Database.database import Database
from UI import ui
from Log import log
from unicodedata import digit
from regex import regexPhone, idGenerate
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
    try:
      temp = user_input
      int(temp)
      choice = temp
    except:
      pass

    # if else statement to check whether int input matches the available choices
    if(choice == "1"):
      user, id = login(id)
      if (user != None):
        id = id
        indexId = log.SystemCounter(id)
        # log menu choice
        log.PrepareLog(indexId, f"{user.username}", "Main Menu login chosen", "/", "no")
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
      log.PrepareLog(indexId, f"Suspicious user", "Main Menu incorrect input", "", "yes")
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
    db = Database()
    while loginAttempt < 3:
        usernameTry = input("Username: ")
        passwordTry = input("Password: ")

        if (usernameTry == superadmin and passwordTry == superadminpassword):
          user = SuperAdmin()
          indexId = log.SystemCounter(id)
            # log log in successful
          log.PrepareLog(indexId, f"{user.username}", "Logged in", "/", "no")
          id = indexId
          return user, id
        else:
          # Get user
          kweerieResult, id = db.getUser((Encrypt(usernameTry), Encrypt(passwordTry)), id)

        if (kweerieResult != None):
            user = decryptUser(kweerieResult)

            loginAttempt = 0

            indexId = log.SystemCounter(id)
            # log log in successful
            log.PrepareLog(indexId, f"{user.username}", "Logged in", "/", "no")
            id = indexId

            return user, id
        else:
            indexId = log.SystemCounter(id)
            # log unsuccessful login
            log.PrepareLog(indexId, f"{usernameTry}", "Unsuccessful login", 'Username: "%s" is used for a login attempt with a wrong password' % usernameTry, "no")
            id = indexId

            loginAttempt+=1
            print("Invalid login")
            
    indexId = log.SystemCounter(id)
    # log multiple incorrect logins
    log.PrepareLog(indexId, f"{usernameTry}", "Unsuccessful login", "Multiple usernames and passwords are tried in a row", "yes")
    id = indexId

    print("Too many login attempts, try again later.")
    exit(1)

main()
