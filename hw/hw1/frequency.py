from collections import Counter
from itertools import cycle

f = open("ulysses.txt","r",encoding='UTF-8')
without_space = []
textwithspace = ""
lines = f.readlines()
for line in lines:
    textwithspace += line
    temp = line.split()
    without_space += temp
frequency = Counter(without_space)
print("Frequent: " + str(frequency.most_common(2)) )
sortedwords = sorted(without_space,key=len)
print("Longest: " + str(sortedwords[-1]))
#longestfrequent = sorted(frequency, key = lambda t: len(t[0]), reverse=True)
longestfrequent = frequency.most_common()
longestfrequent.sort(key = lambda t: len(t[0]), reverse=True)
for tup in longestfrequent:
    if(tup[1] > 24 ):
        print("Longest that occurs more than 25 times: " + tup[0])
        break
#use xxd to view transimtions
#transmittion files are in binary
f.close()
#print(textwithspace)
transfile = []
pineindex = textwithspace.find("Pineapple rock")
#print(textwithspace.find("[ 8 ]"))

with open("transmission1", "rb") as b:
    byte = b.read(1)
    while byte:
        #print(byte)
        transfile+=byte
        # Do stuff with byte.
        byte = b.read(1)

#print(textwithspace[pineindex:(len(transfile)+ pineindex)])
transtext = textwithspace[pineindex:(len(transfile)+ pineindex)]
key = [ chr(ord(a) ^ b) for (a,b) in zip(transtext, transfile) ]
print(key)
predictedkey = "snowboard"

t2 = open("transmission2","rb")
trans2 = [ chr(ord(a) ^ ord(b)) for (a,b) in zip(var, cycle(predictedkey)) ]

#key for transmission 1 and 2 is snowboard
#print(len(transfile))