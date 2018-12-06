import sys
import binascii
import re
import base64
from binascii import hexlify
from struct import *

rules = []
packets = []

class Rule():
    allow = ''
    tcp = False
    source = ''
    sourceport = ''
    dest = ''
    destport = ''

    def setRule(self,allow, tcp, source, dest):
        if (allow == "allow"):
            self.allow = "allow"
        elif (allow == "deny"):
            self.allow = "deny"
        if (tcp == "tcp"):
            self.tcp = True

        m = re.match(r'([0-9]+(?:\.[0-9]+){3}):([0-9]+)',source)
        self.source = m.group(1)
        self.sourceport = m.group(2)
        #print(m.group(1))
        #print(m.group(2))
        m = re.match(r'([0-9]+(?:\.[0-9]+){3}):([0-9]+)',dest)
        self.dest = m.group(1)
        self.destport = m.group(2)
        #print(m.group(1))
        #print(m.group(2))

    def printRule(self):
        print("allow",self.allow)
        print("tcp",self.tcp)
        print("source",self.source)
        print("sourceport",self.sourceport)
        print("dest",self.dest)
        print("destport",self.destport)

class Packet():
    ip_proto = ''
    ip_saddr = ''
    ip_daddr = ''
    pro_src = ''
    pro_dest = ''
    tcp = False
    

    def setPacket(self,ip_proto,ip_saddr,ip_daddr,pro_src,pro_dest):
        self.ip_proto = ip_proto
        self.ip_saddr = ip_saddr
        self.ip_daddr = ip_daddr
        self.pro_src = pro_src
        self.pro_dest = pro_dest
        if(ip_proto == 6):
            tcp = True
    def printPac(self):
        print("ip_proto:",self.ip_proto)
        print("ip_source:",self.ip_saddr)
        print("ip_dest:",self.ip_daddr)
        print("pro_src:",self.pro_src)
        print("pro_dest:",self.pro_dest)


def packetProc(file):
    data = []
    with open(file,"rb") as fp:
        byte = fp.read(1)
        while byte:
            print(byte)
            data.append(byte)
            byte = fp.read(1)
        #print(data)
    print(data)
    print(data.index(b'\x08'))
    ipheaderStart = data.index(b'\x08') + 3
    ip_ser = data[ipheaderStart]
    print(ip_ser)
    print("data",data[ipheaderStart])
    print("num",int.from_bytes(data[ipheaderStart],byteorder = 'big'))
    #print("num",int(hexlify(data[ipheaderStart]),16) )
        #for bytes in data:
        #    byte = bytes.encode("hex")
        #    print(byte)
        #lines = fp.readline()
        #print(lines[])


def packetTest(file):
    with open(file, 'rb') as f:
        data = f.read()
        binval = binascii.hexlify(data)
    print(binval)
    hexvalue = binascii.hexlify(data).decode()
    hexarr = [hexvalue[i:i+2] for i in range(0, len(hexvalue), 2)]
    print(hexarr)
    #print(hexarr.index("45"))
    ipheadS = 54
    ip_proto = hexarr[ipheadS + 9]
    ip_saddr = hexarr[ipheadS+12 :ipheadS+16 ]
    ip_daddr = hexarr[ipheadS+16 :ipheadS+20 ]
    pro_src = hexarr[ipheadS+20:ipheadS+22]
    pro_dest = hexarr[ipheadS+22:ipheadS+24]
    #print(int(ip_proto,16))
    #print(int(ip_saddr[0],16),".",int(ip_saddr[1],16),".",int(ip_saddr[2],16),".",int(ip_saddr[3],16))
    #print(int(pro_src[0]+pro_src[1],16))
    #print(int(ip_daddr[0],16),".",int(ip_daddr[1],16),".",int(ip_daddr[2],16),".",int(ip_daddr[3],16))
    #print(int(pro_dest[0]+pro_dest[1],16))
    pac = Packet()
    ip_pro = int(ip_proto,16)
    ip_sr = str(int(ip_saddr[0],16))+"."+str(int(ip_saddr[1],16))+"."+str(int(ip_saddr[2],16))+"."+str(int(ip_saddr[3],16))
    ip_dr = str(int(ip_daddr[0],16))+"."+str(int(ip_daddr[1],16))+"."+str(int(ip_daddr[2],16))+"."+str(int(ip_daddr[3],16))
    pro_s = int(pro_src[0]+pro_src[1],16)
    pro_d = int(pro_dest[0]+pro_dest[1],16)
    #print(ip_sr)
    pac.setPacket(ip_pro,ip_sr,ip_dr,pro_s,pro_d)
    packets.append(pac)



def filterRule(file):
    with open(file, "r") as fp:
        for lines in fp.readlines():
            line = lines.split()
            #als = line[0]
            #print(line[0])
            #print(line[1])
            #print(line[2])
            #print(line[4])
            rule = Rule()
            rule.setRule(line[0],line[1],line[2],line[4])
            rules.append(rule)

    #for rule in rules:
        #rule.printRule()


def decide():
    for packet in packets:
        #print(packet.printPac())
        sorted = False
        for rule in rules:
            if(rule.tcp == packet.tcp and rule.source == packet.ip_saddr and rule.sourceport == packet.pro_src and rule.dest == packet.ip_daddr and rule.destport == packet.pro_dest):
                if(rule.allow == "allow"):
                    print("Allow")
                    sorted = True
                    break;
                elif (rule.allow == "deny"):
                    print("Deny")
                    sorted = True
                    break;
        if (sorted == False):
                print("unspecified")    


def main():
    filterFile = sys.argv[1]
    packetFile = sys.argv[2]
    filterRule(filterFile)
    #packetProc(packetFile)
    packetTest(packetFile)
    #pac = Packet()
    #pac.setPacket("tcp","127.0.0.1","127.0.0.1","55555","55551")
    #packets.append(pac)
    decide()


main()
