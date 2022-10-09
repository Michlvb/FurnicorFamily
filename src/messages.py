updatePasswordMsg = """The password requires the following:
- Must have a length of at least 8 characters and not longer than 30 characters
- Can contain letters (a-z), (A-Z), numbers (0-9), special characters such as ~!@#$%&_-+=`|\\(){}[]:;'<>,.?/
- Must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one special character!
"""
createUsernameMsg = """The username requires the following:
- Must have a length of at least 6 characters
- Must be no longer than 10 characters
- Can contain letters (a-z), numbers (0-9), underscores (_), apostrophes('), and periods(.)
"""

searchMsg = """Press one or multiple of the following numbers to choose the options to search on:
[0] - To stop adding search options
[1] - Member ID
[2] - First name
[3] - Last name
[4] - Address
[5] - Email
[6] - Phone number
"""

singleOption = """Press one of the following numbers to update the value
[1] - Username
[2] - Role
[3] - First name
[4] - Last name
"""

cityMsg = """The following cities can be chosen:
[1] - Nagpur
[2] - Montreal
[3] - Abuja
[4] - Peshawar
[5] - Curitiba
[6] - Shantou
[7] - Dar es Salaam
[8] - Ho Chi Minh City
[9] - Lima
[10] - Novosibirsk
"""

# Error messages
invalidPassword = """
Password does not match the requirements, please try again.
"""
unauthorized = """
User not authorized
"""
genericError = """
An error occurred
"""
zipNotFound = """
Zipfile not found
"""

# Succes messages
validPassword = """
Password is successfully updated!
"""