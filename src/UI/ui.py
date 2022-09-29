# TODO: Create ui
from os import system
from Log import log
from user import User, SysAdmin,SuperAdmin
from utils import ClearConsole

def menuPrint(printRole):
    # print advisor role
    if (printRole ==  "1"):
        print("Please choose one of the following options:\n(Enter the corresponding number)\n")
        print("[1]: Register new member")
        print("[2]: Update password")
        print("[3]: Modify/update member")
        print("[4]: Search for a member")
        print("[0]: Exit the system")

    # print system admin role
    if (printRole ==  "2"):
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
        print("[10]: Make/restore backup")
        print("[11]: System logs")
        print("[12]: Delete member")
        print("[0]: Exit the system")

    # print super admin role
    if (printRole ==  "3"):
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
        print("[10]: Make/restore backup")
        print("[11]: System logs")
        print("[12]: Delete member")
        print("[13]: Add new admin")
        print("[14]: Update admin")
        print("[15]: Delete admin")
        print("[0]: Exit the system")

# check which role to print to the console
def choices(roleOptions):
    if(roleOptions == "1"):
        return ["1", "2", "3", "4", "0"]
    elif (roleOptions == "2"):
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "0"]
    elif (roleOptions == "3"):
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "0"]

# check role and print appropiate menu
def mainMenu(roleParam, id):
    ClearConsole()
    menuPrint(roleParam)
    menuNav(roleParam, id)
    if(roleParam == "0"):
        exit
    
# user input to navigate the printed menu
def menuNav(role, id):
    options = choices(role)
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
            if (choiceMenu == "0"):
                exit()
            indexId = log.SystemCounter(id)
            # log chosen option
            log.PrepareLog(indexId, "testname%i" % indexId, "Menu navigation option chosen", "/", "no")
            id = indexId
            for x in options:
                if (x == choiceMenu):
                    OptionNavigation(x, role, id)
        # else statement to log incorrect user input and print menu again
        else:
            indexId = log.SystemCounter(id)
            # log incorrect user input
            log.PrepareLog(indexId, "testname%i" % indexId, "Menu navigation incorrect input", "input: '%s' used as main menu choice" % user_input, "no")
            id = indexId
            ClearConsole()
            print("That is not an option. Please choose one of the following options:")
            menuPrint(role)

def OptionNavigation(options, role, id):
    if (options == "1"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        SysAdmin.AddUser(id)

    if (options == "2"):
        if (role == "3"):
            # ResetAdminPassword()
            indexId = log.SystemCounter(id)
            # log user choice
            log.PrepareLog(indexId, 'testname%i' % indexId, 'Option navigation option chosen', 'input: "%s" used as choice by Super Admin' % options, 'no')
            id = indexId
        else:
            indexId = log.SystemCounter(id)
            # log user choice
            log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
            id = indexId
            User.updatePassword(id)

    if (options == "3"):
        # ModifyMember()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        
    if (options == "4"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        User.SearchMember(id)

    if (options == "5"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        SysAdmin.PrintUsers(id)

    if (options == "6"):
        # AddAdvisor()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId

    if (options == "7"):
        # UpdateAdvisor()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId

    if (options == "8"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        SysAdmin.DeleteUser(id)

    if (options == "9"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        SysAdmin.ResetPassword(id)

    if (options == "10"):
        # Backup()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId

    if (options == "11"):
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId
        log.PrintLog()

    if (options == "12"):
        # DeleteMember()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId

    if (options == "13"):
        # AddAdmin()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId

    if (options == "14"):
        # UpdateAdmin()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: %s' used as choice" % options, "no")
        id = indexId

    if (options == "15"):
        # DeleteAdmin()
        indexId = log.SystemCounter(id)
        # log user choice
        log.PrepareLog(indexId, "testname%i" % indexId, "Option navigation option chosen", "input: '%s' used as choice" % options, "no")
        id = indexId

    

