from os import system
from re import U
from time import sleep
from Log import log
from user import User, SysAdmin,SuperAdmin
from utils import ClearConsole

def menuPrint(user):
    # print advisor role
    if (user.role ==  "advisor"):
        print("Please choose one of the following options:\n(Enter the corresponding number)\n")
        print("[1]: Register new member")
        print("[2]: Update password")
        print("[3]: Modify/update member")
        print("[4]: Search for a member")
        print("[0]: Exit the system")

    # print system admin role
    if (user.role ==  "sysadmin"):
        print("Please choose one of the following options:\n(Enter the corresponding number)\n")
        print("[1]: Register new member")
        print("[2]: Update password")
        print("[3]: Modify/update member")
        print("[4]: Search for a member")
        print("[5]: Check users")
        print("[6]: Add new advisor")
        print("[7]: Update advisor")
        print("[8]: Delete advisor")
        print("[9]: Reset advisor password")
        print("[10]: Make backup")
        print("[11]: Restore backup")
        print("[12]: System logs")
        print("[13]: Delete member")
        print("[0]: Exit the system")

    # print super admin role
    if (user.role ==  "superadmin"):
        print("Please choose one of the following options:\n(Enter the corresponding number)\n")
        print("[1]: Register new member")
        print("[2]: Reset admin password")
        print("[3]: Modify/update member")
        print("[4]: Search for a member")
        print("[5]: Check users")
        print("[6]: Add new advisor")
        print("[7]: Update advisor")
        print("[8]: Delete advisor")
        print("[9]: Reset advisor password")
        print("[10]: Make backup")
        print("[11]: Restore backup")
        print("[12]: System logs")
        print("[13]: Delete member")
        print("[14]: Add new admin")
        print("[15]: Update admin")
        print("[16]: Delete admin")
        print("[0]: Exit the system")

# check which role to print to the console
def choices(roleOptions):
    if(roleOptions == "advisor"):
        return ["1", "2", "3", "4", "0"]
    elif (roleOptions == "sysadmin"):
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "0"]
    elif (roleOptions == "superadmin"):
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "0"]

# check role and print appropiate menu
def mainMenu(user, id):
    ClearConsole()
    menuPrint(user)
    menuNav(user, id)
    # if(roleParam == "0"):
    #     exit
    
# user input to navigate the printed menu
def menuNav(user, id):
    options = choices(user.role)
    choiceMenu = 0
    # loop for menu choices and exit
    while not (choiceMenu in options):
        user_input = input()
        # try except statement to check user input for int
        try:
            int(user_input)
            choiceMenu = user_input
        except:
            pass
        
        # navigate to chosen option
        if (choiceMenu in options):
            indexId = log.SystemCounter(id)
            # log chosen option
            log.PrepareLog(indexId, f"{user.username}", "Menu navigation option chosen", "/", "no")
            id = indexId
            if (choiceMenu == "0"):
                exit()
            for x in options:
                if (x == choiceMenu):
                    OptionNavigation(x, user, id)
        # else statement to log incorrect user input and print menu again
        else:
            indexId = log.SystemCounter(id)
            # log incorrect user input
            log.PrepareLog(indexId, f"{user.username}", "Menu navigation incorrect input", "input: '%s' used as main menu choice" % user_input, "no")
            id = indexId
            ClearConsole()
            print("That is not an option. Please choose one of the following options:")
            menuPrint(user)

def OptionNavigation(options, user, id):
    if (options == "1"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.addMember(id)

    if (options == "2"):
        if (user.role == "superadmin"):
            indexId = log.SystemCounter(id)
            # log user choice
            log.PrepareLog(indexId, f"{user.username}", 'Option navigation option chosen', 'input: "%s" used as choice by Super Admin' % options, 'no')
            id = indexId
            id = user.ResetPassword(id)
        else:
            indexId = log.SystemCounter(id)
            # log user choice
            log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
            id = indexId
            id = user.updatePassword(id)

    if (options == "3"):
        # ModifyMember()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.modifyMember(id)
        
    if (options == "4"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.SearchMember(id)

    if (options == "5"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.PrintUsers(id)

    if (options == "6"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.AddUser(id)

    if (options == "7"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.UpdateUser(id)

    if (options == "8"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.DeleteUser(id)

    if (options == "9"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.ResetPassword(id)

    if (options == "10"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.BackupDB(id)
    
    if (options == "11"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.Reset(id)
    
    if (options == "12"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        log.PrintLog()

    if (options == "13"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.DeleteMember(id)

    if (options == "14"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.AddUser(id)

    if (options == "15"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: %s' used as choice" % options, "no")
        id = indexId
        id = user.UpdateUser(id)

    if (options == "16"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, f"{user.username}", "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        id = user.DeleteUser(id)
    
    while True:  
        user_response = input("Press x to return to main menu: ")
        # try except to check if user input is int
        try:
            if (user_response == 'x'):
                break
        except:
            pass  

    mainMenu(user, id)