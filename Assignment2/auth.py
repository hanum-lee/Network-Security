from argon2 import PasswordHasher
import sys

ph = PasswordHasher()
database = []
with open("database.txt") as fp:
    for i in fp.readlines():
        tmp = i.split()
        try:
            database.append((tmp[0], tmp[1]))
        except:pass

def checkValidID(inputid):

    #print(database[0])
    for i, tup in enumerate(database):
        if tup[0] == inputid:
            return i
    return -1

def authen(userid,inputpw):
    index = checkValidID(userid)
    if(index < 0):
        print("Not valid")
        return -1
    savedhash = database[index][1]
    if(ph.verify(inputpw,savedhash)):
        print("Mached!")
        if(ph.check_needs_rehash(savedhash)):
            database[index][1] = ph.hash(inputpw)
            with open("database.txt","w") as db:
                for tup in database:
                    db.write(tup[0]+" "+tup[1]+"\n")
    return 0


def main():
    userid = sys.argv[1]
    userpw = sys.argv[2]
    print("index:",checkValidID(userid))
    pos = checkValidID(userid)
    #print("hash:",database[pos][1])
    authen(userid,userpw)

    



if __name__ == "__main__":
    main()