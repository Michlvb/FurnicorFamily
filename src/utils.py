import os
import re
from messages import updatePasswordMsg, validPassword, invalidPassword, createUsernameMsg, cityMsg, singleOption

def ClearConsole():
  cmd = 'clear'
  if (os.name in ('nt', 'dos')):
    cmd = 'cls'
  os.system(cmd)


def CreatePassword():
  print(updatePasswordMsg)
  while True:
    password = input("Please enter your new password: ")
    try:
      if bool(re.fullmatch(r"[A-Za-z0-9~!@#$%&_\-+=`|\\(){}[\]:;'/<>,\.\?/]{8,30}", password)):
        flag_lower = False
        flag_upper = False
        flag_number = False
        flag_character = False

        for i in password:
          if i.isalpha():
            if i.isupper():
              flag_upper = True
            elif i.islower():
              flag_lower = True
          if i.isdigit():
            flag_number = True
          if bool(re.match(r"['~!@#$%&_\-+=`|\\(){}[\]:;'/<>,\.\?/]", i)):
            flag_character = True
          
        if flag_lower and flag_upper and flag_number and flag_character:
          pass
        else:
          continue
      else:
        print(invalidPassword)
        continue
    except ValueError:
      continue
    else:
      break
  return password

def CreateUsername():
  print(createUsernameMsg)
  while True:
    username = input("Please enter your username: ").lower()
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

def verifyInput(pattern, msg):
  while True:
    value = input(msg)
    try:
      if bool(re.fullmatch(pattern, value)):
        pass
      else:
        continue
    except ValueError as err:
      print(err)
    else:
      break
  return value


def SearchParams():
  options = ["id", "firstname", "lastname", "address", "email", "phone"]
  res = []
  while True:
    num = input("Enter number: ")
    try:
      if bool(re.fullmatch("[0-6]", num)):
        num = int(num)
        if num == 0:
          break
        else:
          res.append(options[num-1])
          continue
      else:
        print("Invalid input")
    except ValueError as err:
      print(err)
  return res

def chooseCity():
  print(cityMsg)
  cities = ["Nagpur", "Montreal", "Abuja", "Peshawar", "Curitiba", "Shantou", "Dar es Salaam", "Ho Chi Minh City", "Lima", "Novosibirsk"]
  city = ""
  while True:
    num = input("Enter number of desired city: ")
    try:
      if bool(re.fullmatch("^([1-9]|1[0])$", num)):
        num = int(num)
        city += cities[num-1]
        break
      else:
        print("Invalid input")
    except ValueError as err:
      print(err)
  return city


def getValue():
  print(singleOption)
  options = ["username","role", "firstname", "lastname"]
  option  = ""
  while True:
    num = input("Enter number: ")
    try:
      if bool(re.fullmatch("[1-4]", num)):
        num = int(num)
        option += options[num-1]
        break
      else:
        print("Invalid input")
        continue
    except ValueError as err:
      print(err)
  return option

def ValidateOptionValue(option):
  if option == "id":
    res = verifyInput("^[1-9]+$", "Please enter the member Id: ")
    return res
  elif option == "firstname":
    res = verifyInput("^[-a-zA-Z,']+$", "Please enter the first name: ")
    return res
  elif option == "lastname":
    res = verifyInput("^[-a-zA-Z,'\s]+$", "Please enter the last name: ")
    return res
  elif option == "address":
    street = verifyInput("^[-a-zA-Z ,.']+$", "Please enter the street name: ")
    houseNum = verifyInput("^[0-9]{0,4}$", "Please enter the house number: ")
    zipCode = verifyInput("^[1-9][0-9]{3} ?(?!sa|sd|ss)[a-zA-Z]{2}$", "Please enter the zipCode: ")
    city    = chooseCity()
    address = f"{street} {houseNum} {zipCode} {city}"
    return address
  elif option == "email":
    res = verifyInput("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+((\.[A-Z|a-z]{2,})+)", "Please enter the email: ")
    return res
  elif option == "phone":
    res = verifyInput("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", "Please enter the number: ")
    return res