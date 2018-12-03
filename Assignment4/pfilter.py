import sys
import binascii
import re
import base64


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
        else if (allow == "deny")
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
    tcp = True

    def setPacket(self,ip_proto,ip_saddr,ip_daddr,pro_src,pro_dest):
        self.ip_proto = ip_proto
        self.ip_saddr = ip_saddr
        self.ip_daddr = ip_daddr
        self.pro_src = pro_src
        self.pro_dest = pro_dest


def packetProc(file):
    with open(file,"rb") as fp:
        lines = fp.readlines()
        for line in lines:
            pfile = base64.decodebytes(line)
            print(pfile)



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

    for rule in rules:
        rule.printRule()


def decide():
    for packet in packets:
        sorted = False
        for rule in rules:
            if(rule.tcp == packet.tcp and rule.source == packet.ip_saddr and rule.sourceport == packet.pro_src and rule.dest == packet.ip_daddr and rule.destport == packet.pro_dest)
                if(rule.allow == "allow"):
                    print("Allow")
                    sorted = True
                else if (rule.allow == "deny"):
                    print("Deny")
                    sorted = True
            if (sorted == False):
                print("unspecified")


def main():
    filterFile = sys.argv[1]
    packetFile = sys.argv[2]
    filterRule(filterFile)
    #packetProc(packetFile)
    decide()


main()
