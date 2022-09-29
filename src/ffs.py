from typing import Tuple
from Database.database import Database
from UI import ui
from os import system
from Log import log
import re
import random
from unicodedata import digit
from Log.log import Decrypt, Encrypt

from user import SuperAdmin

username = "superadmin"
password = "Admin321!"
loggedIn = False
member = ""
members = ()

def idGenerate():
    x = True
    checkSum = 0
    while x:
        digits = ""
        first = random.randint(1,9)
        digits = digits + str(first)
        for i in range(9):  
            rest = random.randrange(0,9)
            digits = digits + str(rest)

        for q in range(len(digits)-1):
            checkSum = (checkSum + int(digits[q]))%10

        if int(digits)%10 != checkSum:
            continue
        else:
            break
    print(f"A member ID has been made with the number {digits}")

def regexID(memberID):
    memberIdRe = re.search("^[1-9]+$", memberID)
    return memberIdRe

def regexName(name):
    nameRe = re.search("^[-a-zA-Z ,']+$", name)
    return nameRe

def regexStreet(streetName):
    streetRe = re.search("^[-a-zA-Z ,.']+$", streetName)
    return streetRe

def regexNumber(houseNumber):
    numberRe = re.search("[1-9]+", houseNumber)
    return numberRe

def regexZipcode(zipcode):
    zipcodeRe = re.search("^[1-9][0-9]{3} ?(?!sa|sd|ss)[a-zA-Z]{2}$", zipcode)
    return zipcodeRe

def regexEmail(email):
    emailRe = re.search("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+((\.[A-Z|a-z]{2,})+)", email)
    return emailRe

def regexPhone(phonenumber):
    phoneRe = re.search("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", phonenumber)
    return phoneRe

def main():
  # initialize id for logging purposes
  id = 0

#   system('cls')
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
    # HelloWorld1~ - PmttwEwztl9~
    if(choice == "1"):
      role = "2" # hard coded for testing purposes
      loggedIn = login(id)
      # get user with data
      if (loggedIn[0] == True):
        id = loggedIn[1]
        indexId = log.SystemCounter(id)
        # log menu choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Main Menu login chosen", "/", "no")
        id = indexId
        # navigate to main menu from ui
        # addMember(id)
        # modifyMember(id)
        sa = SuperAdmin()
        sa.PrintUsers(1)
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

def decryptUser(data):
    user = []
    for val in data:
        user.append(Decrypt(val))
    return tuple(user)

def login(id):
    loginAttempt = 0
    x = True
    db = Database()
    while loginAttempt < 3:
        usernameTry = Encrypt(input("Username: "))
        passwordTry = Encrypt(input("Password: "))

        # Get user
        kweerieResult = db.getUser((usernameTry, passwordTry))
 
        if (kweerieResult != None):
            user = decryptUser(kweerieResult)

            loggedIn = True
            loginAttempt = 0
            print("Login succesful")

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

def addMember(id):
    while True:    
        firstName = input("What is your first name: ")
        outcomeRe = regexName(firstName)
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
        outcomeRe = regexName(lastName)
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
        outcomeRe = regexStreet(streetName)
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
        outcomeRe = regexNumber(houseNumber)
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
        outcomeRe = regexZipcode(zipcode)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input zip code", "Invalid input: %s recorded as user input" % zipcode, "no")
            id = indexId
            print("Invalid input")
        else:
            #add city
            address = f"{streetName} {houseNumber} {zipcode}"
            print(address)
            break

    while True:
        emailAddress = input("What is your email address: ")
        outcomeRe = regexEmail(emailAddress)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input email", "Invalid input: %s recorded as user input" % emailAddress, "no")
            id = indexId
            print("Invalid input")
        else:
            break
    
    while True:    
        mobilePhone = input("What is your phonenumber: ")
        outcomeRe = regexPhone(mobilePhone)
        if not outcomeRe:
            indexId = log.SystemCounter(id)
            # log invalid input
            log.PrepareLog(indexId, "testname", "Invalid input phone number", "Invalid input: %s recorded as user input" % mobilePhone, "no")
            id = indexId
            print("Invalid input")
        else:
            break

    members =  (firstName, lastName, address, emailAddress, mobilePhone)
    return members

def modifyMember(id):
    checkSum = 0;
    x = True

    while True:
        memberModified = input("Please enter the member ID of the person you wish to change information of: ")
        outcomeRE = regexID(memberModified)

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
            outcomeRE = regexName(modifiedFirstName)

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
            outcomeRE = regexName(modifiedLastName)

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
            outcomeRE = regexStreet(modifiedStreet)
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
            outcomeRE = regexNumber(modifiedNumber)
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
            outcomeRE = regexZipcode(modifiedZipcode)
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
            outcomeRE = regexEmail(modifiedEmail)
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
            outcomeRE = regexPhone(modifiedPhone)
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
                


main()

