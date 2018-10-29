from argon2 import PasswordHasher
import sys
import string
import re

ph = PasswordHasher()
database = []
with open("database.txt") as fp:
    for i in fp.readlines():
        tmp = i.split()
        try:
            database.append((tmp[0], tmp[1]))
        except:pass

with open("words.txt") as dc:
    lines = dc.readlines()

words = [x.strip() for x in lines]

for x in words:
    x.lower()

def checkDic(inputwd):
    try:
        words.index(inputwd)
        print("Password in dictionary")
        return True
    except:
        return False


def checkValidID(inputid):

    if(len([item for item in database if item[0] == inputid]) > 0):
        return False
    else:
        return True


def checkValidPassword(inputpw):
#    try:
#        float(inputpw)
#        return False
#    except ValueError:
#        pass
    if(re.match(r'^([\s\d]+)$',inputpw)):
        print("Only numbers")
        return False
#    try:
#        words.index(inputpw)
#        print("Password in dictionary")
#        return False
#    except:
        #return True
#        pass
    if(checkDic(inputpw)):
        return False
    try:
        m = re.match(r"(\d+)(\w+)", inputpw)
#        print("Group1:", m.group(1))
#        print("Groupt2:" ,m.group(2))
#        print("Num first")
        if(checkDic(m.group(2))):
            return False
    except:
        pass
    try:
        m = re.match(r"(\w+)(\d+)", inputpw)
#        print("Group1:", m.group(1))
#        print("Groupt2:" ,m.group(2))
#        print("Word First")
        if(checkDic(m.group(1))):
            return False
    except:
        pass
    return True
    #if():


def main():
    print("Testing")
    userid = sys.argv[1]
    userpw = sys.argv[2]

    if(not checkValidID(userid)):
        print("Invalid ID")
        return -1

    #print("Check pw:",checkValidPassword(sys.argv[2]))
    if(not (checkValidPassword(userpw))):
        print("Invalid Password")
        return -1
    
    hash = ph.hash(userpw)

    userpair = "\n"+userid+" "+hash
    print("UserPair:",userpair)
    with open("database.txt", "a") as db:
        db.write(userpair)

    return 0



#Basic setup

#print("Check id:",checkValidID(sys.argv[1]))

if __name__ == "__main__":
    main()



#print(sys.argv[0],sys.argv[1],sys.argv[2])
#print(words[1])
#print(database[1])

hash = ph.hash("Test")
print(hash)
print(ph.verify(hash,"Test"))

try:
    print(ph.verify(hash,"Nottest"))
except Exception as e:
    print(e)
print(ph.check_needs_rehash(hash))
