import random


currenttime = 0
random.seed(1)
class Service:
    occupided = False


class User:
    issuedtime = 0
    expirytime = 0
    ticket = False
    requesttime = 0
    def checkval():
        if(expirytime - currenttime > 0):
            ticket = True

for x in range(10):
    print(random.randint(1,9))

users = [User() for count in range(100)]
print(len(users))
