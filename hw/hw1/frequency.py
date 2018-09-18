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
longestfrequent = sorted(frequency, key = lambda t: len(t[0]), reverse=True)
#print(longestfrequent[1])
#print(line)
f.close()
