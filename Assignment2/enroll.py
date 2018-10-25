from argon2 import PasswordHasher
import sys
import string


def checkValid(inputid):

    if(len([item for item in database if item[0] == inputid]) > 0):
        return False
    else:
        return True


#Basic setup
ph = PasswordHasher()
database = []
with open("database.txt") as fp:
    for i in fp.readlines():
        tmp = i.split()
        try:
            database.append((tmp[0], tmp[1]))
            #result.append((eval(tmp[0]), eval(tmp[1])))
        except:pass

#with open("database.txt") as db:
#    database = [tuple(map(string, i.split(","))) for i in db]
#database = result
with open("words.txt") as dc:
    lines = dc.readlines()

words = [x.strip() for x in lines]

print(checkValid(sys.argv[1]))

print(sys.argv[0],sys.argv[1],sys.argv[2])
print(words[1])
print(database[1])

hash = ph.hash("Test")
print(hash)
print(ph.verify(hash,"Test"))

try:
    print(ph.verify(hash,"Nottest"))
except Exception as e:
    print(e)
print(ph.check_needs_rehash(hash))



