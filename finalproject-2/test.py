from splinter import Browser
from bs4 import BeautifulSoup
import re
from flask import Flask, request, jsonify, render_template
import requests

url_cal = 'https://ndb.nal.usda.gov/ndb/search/list?fgcd=&manu=&lfacet=&count=&max=25&sort=default&qlookup={}&offset=&format=Abridged&new=&measureby=&ds=SR&order=asc&qt=&qp=&qa=&qn=&q=&ing='.format('ice cream')
response1 = requests.get(url_cal)
soup = BeautifulSoup(response1.text, 'lxml')
row = soup.findAll('td')[2]
newurl = 'https://ndb.nal.usda.gov'+ row.find('a')['href']
newresponse = requests.get(newurl)
newsoup = BeautifulSoup(newresponse.text, 'lxml')
unit = newsoup.find('td', text = 'kcal')

unitstr = str(unit)

numkcal= str(unit.find_next_sibling("td"))

unit = re.sub("<.*?>", "", unitstr)
numkcal = re.sub("<.*?>", "", numkcal)

print(numkcal)