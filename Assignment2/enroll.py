from argon2 import PasswordHasher

ph = PasswordHasher()

db = open("database.txt","a",encoding="UTF-8")
with open("words.txt") as dc:
    lines = dc.readlines()

words = [x.strip() for x in lines]




print(words[1])


hash = ph.hash("Test")
print(hash)
print(ph.verify(hash,"Test"))

try:
    print(ph.verify(hash,"Nottest"))
except Exception as e:
    print(e)
print(ph.check_needs_rehash(hash))




db.close()