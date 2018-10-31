from argon2 import PasswordHasher
import sys


ph = PasswordHasher()   # Setting password hasher
# Importing database as list of tuple
database = []
with open("database.txt") as fp:
    for i in fp.readlines():
        tmp = i.split()
        try:
            database.append((tmp[0], tmp[1]))
        except:pass
# Checks if the inputed ID is in database. If it is, return the index value of the ID
def checkValidID(inputid):
    for i, tup in enumerate(database):
        if tup[0] == inputid:
            return i
    return -1
# Checks if the inputed pair of ID and password by user is valid
def authen(userid,inputpw):
    index = checkValidID(userid)
    if(index < 0):
        print("Not valid ID. Access Denied")
        return -1
    savedhash = database[index][1]
    try:
        # Verifies if the inputed password matches the hash value saved in the database
        ph.verify(savedhash,inputpw)
        print("Access Granted")
        # If it needs rehashing, rehash the password
        if(ph.check_needs_rehash(savedhash)):
            database[index][1] = ph.hash(inputpw)
            with open("database.txt","w") as db:
                for tup in database:
                    db.write(tup[0]+" "+tup[1]+"\n")
        return 0
    except Exception as e:
        print("Not correct password. Access Denied")
    return -1

def main():
    # Get user inputed ID and password
    userid = sys.argv[1]
    userpw = sys.argv[2]
    authen(userid,userpw)

if __name__ == "__main__":
    main()
