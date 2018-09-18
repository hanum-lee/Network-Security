from collections import Counter


f = open("ulysses.txt","r",encoding='UTF-8')
lines = f.readlines()
for line in lines:
    print(line)
#print(line)
f.close()
