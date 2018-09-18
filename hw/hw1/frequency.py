from collections import Counter

f = open("ulysses.txt","r",encoding='UTF-8')
without_space = []
lines = f.readlines()
for line in lines:
    temp = line.split()
    without_space += temp
frequency = Counter(without_space)
print(frequency.most_common(2))
#print(line)
f.close()
