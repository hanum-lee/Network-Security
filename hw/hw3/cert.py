from bs4 import BeautifulSoup
import urllib.request as req
import re
import requests
import ssl
import socket
import M2Crypto
from datetime import datetime as dt
from collections import Counter


url = "https://www.alexa.com/topsites/category/Top/Games"
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
res = req.urlopen(url,context=gcontext)

soup = BeautifulSoup(res, "html.parser")
sites = soup.select(" div.td.DescriptionCell > p > a")
sitesurl = []
for site in sites:
    temp = str(site)
    m = re.search(r'(?<=siteinfo/)(.*)(?=\")', temp)
    urlsite = "http://www." + m.group(1)
    sitesurl.append(urlsite)
    #print("url:",urlsite)
existsite = []

for site in sitesurl:
    try:
        request = requests.get(site)
        if (request.status_code == 200) | (request.status_code == 300):
            print("Exist:",site)
            existsite.append(site)
            #break
        else:
            print("Not Exist:",site)
    except Exception as e:
        print(e)

print("Amount of website works:",len(existsite))

issuers=[]
dates=[]

for site in existsite:
    m = re.search(r'(?<=http://www.)(.*)',site)
    justurl = m.group(1)
    print("just url",justurl)
    try:
        adds = socket.gethostbyname(justurl)
        print("IP:",adds)
        tempcert = ssl.get_server_certificate((adds,443))
        x509 = M2Crypto.X509.load_cert_string(tempcert)
        ssl.get_server_certificate((adds,443))
        issuer = str(x509.get_issuer())
        print("Issuer:",issuer)
        issuers.append(issuer)
        validdate = str(x509.get_not_after())
        print("Not after:",validdate)
        #print(type(str(validdate)))
        certval = dt.strptime(validdate,"%b %d %H:%M:%S %Y %Z")
        if certval  > dt(2019,12,31):
            dates.append(validdate)
    except Exception as e:
        print(e)

print(len(dates))
count = Counter(issuers)
print(count.most_common(1))
#print("Cert:")
#print("Cert info:",x509.get_subject().as_text())

#for site in truesites:
#    m = re.match(r'(?<=\>)(.*?)(?=\<)', str(site))
#    print("Site:",m)
#print("Site",site)
