import random


currenttime = 0
random.seed(1)
class Service:
    occupided = False
    numOfTicektIssued = 0


class User:
    issuedtime = 0
    expirytime = 0
    ticket = False
    requesttime = 0
    def checkval():
        if(expirytime - currenttime > 0):
            ticket = True

    def issueTicket():
        service_num = -1
        checkval()
        if (ticket == False):
            service_num = random.randin(0,9)
        return service_num



for x in range(10):
    print(random.randint(1,9))

users = [User() for count in range(100)]
print(len(users))
