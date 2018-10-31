from argon2 import PasswordHasher
import sys
import string
import re

ph = PasswordHasher()  #setting up password hashing. Hashing password 2 times
database = []
# Importing database as list of tuple
with open("database.txt") as fp:
    for i in fp.readlines():
        tmp = i.split()
        try:
            database.append((tmp[0], tmp[1]))
        except:pass
# Importing dictionary
with open("words.txt") as dc:
    lines = dc.readlines()
words = [x.strip() for x in lines]
for x in words:
    x.lower()
# Checking if the dictionary contains inputed word
def checkDic(inputwd):
    try:
        words.index(inputwd)
        print("Password in dictionary")
        return True
    except:
        return False
# Check if the ID inputed by user is valid
def checkValidID(inputid):
    if(len([item for item in database if item[0] == inputid]) > 0):
        return False
    else:
        return True
# Check if the password inputed by user is valid
def checkValidPassword(inputpw):
    # Checks if the password only contains numbers
    if(re.match(r'^([\s\d]+)$',inputpw)):
        print("Only numbers")
        return False
    # Check if the password only contains word that is in dictionary
    if(checkDic(inputpw)):
        return False
    try:
        # Checks if the password is the type of [wordnum] where word is in dictionary
        m = re.match(r"(\d+)(\w+)", inputpw)
        if(checkDic(m.group(2))):
            return False
    except:
        pass
    try:
        # Checks if the password is the type of [numword] where word is in dictionary
        m = re.match(r"(\w+)(\d+)", inputpw)
        if(checkDic(m.group(1))):
            return False
    except:
        pass
    return True


def main():
    # Gets user inputed ID and password
    userid = sys.argv[1]
    userpw = sys.argv[2]
    # Runs through the validation methods for ID and password
    if(not checkValidID(userid)):
        print("Invalid ID. Rejected")
        return -1
    if(not (checkValidPassword(userpw))):
        print("Invalid Password. Rejected")
        return -1
    # If everything is fine, hash the password and save it to database
    hash = ph.hash(userpw)
    userpair = "\n"+userid+" "+hash
    print("Accept")
    with open("database.txt", "a") as db:
        db.write(userpair)

    return 0

if __name__ == "__main__":
    main()
