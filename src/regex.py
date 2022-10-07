import re

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

def regexUsername():
  while True:
    username = input("Please enter your username: ")
    try:
      if bool(re.search(r"^[a-zA-Z]", username)):
        if bool(re.fullmatch(r"[A-Za-z0-9_'\.]{6,10}", username)):
          print("VALID")
        else:
          print("Invalid")
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
        print("Valid")
      else:
        print("Invalid")
        continue
    except ValueError:
      continue
    else:
      break
  return password