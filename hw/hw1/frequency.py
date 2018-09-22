from collections import Counter
from itertools import cycle
import string
import re

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

#https://stackoverflow.com/questions/29408173/byte-operations-xor-in-python

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

#section 13

#key for transmission 1 and 2 is snowboard

transmission2 = []
#t2 = open("transmission2","rb")
with open("transmission2", "rb") as t2:
    byte = t2.read(1)
    while byte:
        #print(byte)
        transmission2+=byte
        # Do stuff with byte.
        byte = t2.read(1)
trans2 = [ chr((a) ^ ord(b)) for (a,b) in zip(transmission2, cycle(predictedkey)) ]

print(trans2)

#https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python

question3 = textwithspace
question3.strip()
exclude = set(string.punctuation)
#table = string.maketrans("","")
#question3.translate(table, string.punctuation)
quest3 = ''.join(ch for ch in question3 if ch not in exclude)
quest3 = ''.join(quest3.split())
quest3 = quest3.upper()


t3 = open("transmission3.txt","r")
trans3 = ""
lines = t3.readlines()
for line in lines:
    trans3 += line

#print(trans3)

trans3t =  ''.join(chr(ord(a) ^ ord(b)) for (a,b) in zip(quest3, cycle(trans3)))
#indexthe = [m.start() for m in re.finditer('the', trans3t)]
#print(indexthe)
'''for oc in indexthe:
    print(oc)
    print(trans3t[oc:oc+100])'''
#print(trans3t[indexthe:indexthe + 100])
#question3.replace("\n","")
print("Trans3" + str(trans3t))
t3.close()
#print(quest3)

'''
for n in range(1, len(trans3t)):
    substr_counter = Counter(trans3t[i: i+n] for i in range(len(trans3t) - n))
    phrase, count = substr_counter.most_common(1)[0]
    if count == 1:      # early out for trivial cases
        break
    print ('Size: %3d:  Occurrences: %3d  Phrase: %r' % (n, count, phrase))

'''
