import re
import random

def idGenerate():
    checkSum = 0
    digits = ""
    first = random.randint(1,9)
    digits = digits + str(first)
    for i in range(8):  
      rest = random.randrange(0,9)
      digits = digits + str(rest)
    for i in range(len(digits)):
      checkSum += int(digits[i])
    digits += str(checkSum%10)
    print(digits)
    return digits

def regexID(memberID):
    memberIdRe = re.search("^[0-9]+$", memberID)
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

#TODO: Needs to be changed - Accepts dashes and other stuff (should only accept numbers)
def regexPhone(phonenumber):
    phoneRe = re.search("(^[0-8]{8}$)", phonenumber)
    return phoneRe

def regexUsername():
  while True:
    username = input("Please enter your username: ")
    try:
      if bool(re.search(r"^[a-zA-Z]", username)):
        if bool(re.fullmatch(r"[A-Za-z0-9_'\.]{6,10}", username)):
          pass
        else:
          continue
      else:
        print("Must start with a letter")
        continue
    except ValueError as err:
      print(err)
      continue
    else:
      break
  return username

def regexPassword():
  while True:
    password = input("Please enter your password: ")
    try:
      if bool(re.fullmatch(r"[A-Za-z0-9~!@#$%&_\-+=`|\\(){}[\]:;'/<>,\.\?/]{8,30}", password)):
        pass
      else:
        continue
    except ValueError:
      continue
    else:
      break
  return password