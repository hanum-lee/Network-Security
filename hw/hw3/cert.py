from bs4 import BeautifulSoup
import urllib.request as req
import re
import requests
import ssl
import socket
import OpenSSL


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
            break
        else:
            print("Not Exist:",site)
    except Exception as e:
        print(e)

print("Amount of website works:",len(existsite))

m = re.search(r'(?<=http://www.)(.*)',existsite[0])
justurl = m.group(1)
print("just url",justurl)
print(type(existsite[0]))
print(existsite[0])
adds = socket.gethostbyname(justurl)
print("IP:",adds)
tempcert = ssl.get_server_certificate((adds,443))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
x509.get_subject().get_components()
print("Cert:",ssl.get_server_certificate((adds,443)))
#for site in truesites:
#    m = re.match(r'(?<=\>)(.*?)(?=\<)', str(site))
#    print("Site:",m)
#print("Site",site)
