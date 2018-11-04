from bs4 import BeautifulSoup
import urllib.request as req

url = "https://www.alexa.com/topsites/category/Top/Games"
res = req.urlopen(url)

soup = BeautifulSoup(res, "html.parser")
sites = soup.select(" div.td.DescriptionCell > p > a")
for site in sites:
    print("Site:",site)
#print("Site",site)
