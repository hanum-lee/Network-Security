from collections import Counter

f = open("ulysses.txt","r",encoding='UTF-8')
without_space = []
lines = f.readlines()
for line in lines:
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
