# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 16:43:28 2021

@author: LENOVO
"""

import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

#get all the urls
links=[]
for i in range(1,26):
    page = requests.get('https://www.depensez.com/author/dominique/page/'+ str(i) +'/')
    soup = BeautifulSoup(page.text, 'html.parser')
    uls = soup.find('ul',attrs={'class':"posts-items"})
    urls = uls.find_all('a',attrs={'class':'post-thumb'})
    for s in urls:
        links.append(s['href'])

#scraping
titres=[]
categories=[]
liens=[]
#our loop through each link's page
for link in links :
    sites = requests.get(link)
    soups = BeautifulSoup(sites.text, 'html.parser')
    liens.append(link)
    titres.append(soups.find('h1',attrs={'class':'post-title entry-title'}).text.strip())
    categories.append(soups.find('h5',attrs={'class':'post-cat-wrap'}).text.strip())

#pandas dataframe
data = pd.DataFrame({'url': liens,'titre': titres,'catégorie':categories})

#cleaning data
aa=[re.findall('[A-Z-É][^A-Z-É]*', x) for x in data['catégorie']]
data['catégorie']=[','.join(a) for a in aa]
liste=[]
for ss in data['catégorie']:
    if ',-,' in ss or ' -' in ss or ',-' in ss:
        liste.append(ss.replace(',',''))
    else:
        liste.append(ss)
data['catégorie']=liste

#add dataframe to csv file named 'result.csv'
data.to_csv('result.csv',index=False)
