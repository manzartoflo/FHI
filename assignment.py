#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 23:19:25 2019

@author: manzar
"""

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re
url = "https://fhi.nl/ledenlijst/?page="

req = requests.get(url)
soup = BeautifulSoup(req.text, "lxml")
div = soup.findAll('div', {"class": "panel panel-default"})
k = 0
file = open('assignment.csv', 'w')
header = "Company Name, Phone, Email\n"
file.write(header)
for i in range(1, 22):
    req = requests.get(url + str(i))
    soup = BeautifulSoup(req.text, "lxml")
    divs = soup.findAll('div', {"class": "panel panel-default"})
    for div in divs:
        req_inside = requests.get(urljoin(url, div.a.attrs['href']))
        soup_inside = BeautifulSoup(req_inside.text, "lxml")
        d = soup_inside.findAll('div', {'class': 'block'})
        try:
            name = d[0].h1.text
        except:
            name = 'NaN'
        r = re.compile("(?:\+?1[ .*-]?)?(?:\(? ?)?\d{3}(?: ?\)?)? ?(?:\*|(?:\.|-){1,2})? ?\d{3} ?(?:\*|(?:\.|-){1,2})? ?\d{4}")
        try:
            telephone = r.findall(d[1].address.text)
        except:
            telephone = ['NaN']
        try:
            email = d[1].address.a.text
        except:
            email = 'NaN'
        try:
            if(name != 'NaN'):
                print(name, telephone[0], email)
                file.write(name.replace(',', '') + ", " + telephone[0].replace(',', '') + ", " + email.replace(',', '') + "\n")
        except:
            if(name != 'NaN'):
                print(name, 'NaN', email)
                file.write(name.replace(',', '') + ", " + "NaN" + ", " + email.replace(',', '') + "\n")
            
file.close()

import pandas
file = pandas.read_csv('assignment.csv')