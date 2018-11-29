import sys
import binascii



def filterRule(file):
    with open(file,"rb") as fp:
        chunk = iter(lambda: fp.read(32), b'')
        print(binascii.hexlify(chunk))



def main():
    filterFile = sys.argv[1]
    packetFile = sys.argv[2]
    filterRule(packetFile)
    
main()