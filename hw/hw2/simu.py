import random


global currenttime 
currenttime = 0
random.seed(2)
class Service:
    numOfTicektIssued = 0

class User:
    issuedtime = 0
    expirytime = 0
    ticket = False
    next_request = 0
    def checkval(self):
        if((self.expirytime - currenttime) > 0):
            self.ticket = True
        else:
            self.ticket = False


    def setIssuedTime(self,time):
        self.issuedtime = time
        self.expirytime = self.issuedtime + 30
    
    def issueTicket(self):
        service_num = -1
        self.checkval()
        if (self.ticket == False):
            if(currenttime >= self.expirytime + self.next_request):
                service_num = random.randint(0,9)
                self.next_request = int(random.expovariate(0.25))
                self.setIssuedTime(currenttime)
        return service_num

#for x in range(20):
    #print(random.randint(1,9))
    #print("Exp: " , int(random.expovariate(0.25)))

users = [User() for count in range(100)]
services = [Service() for count in range(10)]

while currenttime <= 480:

    for i in range(len(users)):
        serviceNum = users[i].issueTicket()
        if(serviceNum >= 0):
            services[serviceNum].numOfTicektIssued += 1
    
    currenttime += 1

total = 0
for i in range (len(services)):
    print("Service",i," number of ticket issued: ",services[i].numOfTicektIssued)
    total += services[i].numOfTicektIssued

print("Total number of ticket issued: ", total)
