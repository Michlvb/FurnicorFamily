# TODO: Setup logging functionality
import logging
from datetime import datetime

# initialize logger and log.txt
logger = logging.getLogger('systemlogger')
logger.setLevel(logging.DEBUG)
# Changed path for Filehandler, on my laptop it gave an error. Needs to be verified if it  works though.
fileHandler = logging.FileHandler('log.txt', mode='w')
fileHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

def Encrypt(text):
    temp = ""
    for i in text:
        char = i
        if (char.isupper()):
            # ord is used to convert a character to Unicode value, chr does the opposite
            temp += chr((ord(char) + 8-65) % 26 + 65)
        elif (char.isdigit()):
            temp += str((int(char) + 8) % 10)
        elif (char.islower()):
            temp += chr((ord(char) + 8-97)% 26+ 97)
        else:
            temp += char

    return temp

def Decrypt(text):
    temp = ""
    for i in text:
        for j in i:
            for element in j:
                char = element
                if (char.isupper()):
                    # ord is used to convert a character to Unicode value, chr does the opposite
                    temp += chr((ord(char) - 8-65) % 26 + 65)
                elif (char.isdigit()):
                    temp += str((int(char) - 8) % 10)
                elif (char.islower()):
                    temp += chr((ord(char) - 8-97)% 26+ 97)
                else:
                    temp += char
    return temp

# initialize headers for the table
encryptedHeader = Encrypt("No., Username, Date, Time, Description of activity, Additional information, suspicious")
logger.info(encryptedHeader)

# system counter to count first column of the table
def SystemCounter(id):
    id += 1
    return id

# add the prepared statement to the log file
def AddToLog(encryptedMessage):
    logger.info(encryptedMessage)

# prepare statement and add the statement to the table
def PrepareLog(id, username, description, additional, suspicious):
    encryptedMessage = Encrypt("%s, %s, %s, %s, %s, %s, %s" % (str(id), username, str(datetime.now().strftime('%Y-%m-%d')), str(datetime.now().strftime('%H:%M:%S')), description, additional, suspicious))
    AddToLog(encryptedMessage)

# print log file to console
def PrintLog():
    print("Printing the system logs:")
    table= []
    # read contents of encrypted file
    f = open('log.txt', 'r')
    while True:
        #read line by line
        line = f.readline()

        # end of file or empty file
        if not line:
            break
        # decrypt the line
        x = Decrypt(line)
        # convert decrypted string into a list
        temp = list(x.split(","))
        # add created list to the big table
        table.append(temp)

    f.close()
    # print table and its contents with specific format to the console
    for v in table:
        no, username, date, time, description, additional, suspicious = v
        print("{:<8} {:<15} {:<15} {:<15} {:<40} {:<80} {:<8}".format(no, username, date, time, description, additional, suspicious))








