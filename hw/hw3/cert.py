from bs4 import BeautifulSoup
import urllib.request as req
import re
import requests


url = "https://www.alexa.com/topsites/category/Top/Games"
res = req.urlopen(url)

soup = BeautifulSoup(res, "html.parser")
sites = soup.select(" div.td.DescriptionCell > p > a")
sitesurl = []
for site in sites:
    temp = str(site)
    m = re.search(r'(?<=siteinfo/)(.*)(?=\")', temp)
    urlsite = "https://www." + m.group(1)
    sitesurl.append(urlsite)
    #print("url:",urlsite)
existsite = []
for site in sitesurl:
    try:
        request = requests.get(site)
        if request.status_code == 200:
            print("Exist:",site)
            existsite.append(site)
        else:
            print("Not Exist:",site)
    except Exception as e:
        print(e)

print("Amount of website works:",len(existsite))
#for site in truesites:
#    m = re.match(r'(?<=\>)(.*?)(?=\<)', str(site))
#    print("Site:",m)
#print("Site",site)
