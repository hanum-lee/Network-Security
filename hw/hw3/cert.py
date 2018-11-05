from bs4 import BeautifulSoup
import urllib.request as req
import re
import requests


url = "https://www.alexa.com/topsites/category/Top/Games"
res = req.urlopen(url)

soup = BeautifulSoup(res, "html.parser")
sites = soup.select(" div.td.DescriptionCell > p > a")
truesites = []
for site in sites:
    #truesites.append(str(site))
    temp = str(site)
    #print(temp)
    m = re.search(r'(?<=siteinfo/)(.*)(?=\")', temp)
    print("Site:",m.group(1))


#for site in truesites:
#    m = re.match(r'(?<=\>)(.*?)(?=\<)', str(site))
#    print("Site:",m)
#print("Site",site)
