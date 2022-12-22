# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 11:02:34 2022

@author: SMRUTI
"""

#import all files
from bs4 import BeautifulSoup
import requests
import json

tags = ['programming', 'tech', 'javascript', 'web-development', 
            'technology', 'react', 'startup', 'python', 
            'software-development', 'design', 'life-lessons',
            'productivity']

def existence(url):
    if url is not None:
        return url.text.strip()
    else:
        return None



#function to scrap the required information
def scrapInfo(aTag):
    
    arts = []

     
    for t in aTag:
        i = 1       #page number traverser
        print(t)

        url = requests.get(f'https://www.freecodecamp.org/news/tag/{t}/{i}')

        soup = BeautifulSoup(url.content, 'html.parser')
        #print(soup.find_all('section', class_ = 'error-message'))
        
        while(soup.find_all('section', class_ = 'error-message') == []):
            
            print("fetching ", i)
            news = soup.find_all('article', class_ = 'post-card')

            for (art) in (news):
                
                temp_title = art.find('h2', class_ ='post-card-title').text.replace('"','').strip()
                
                temp_author = existence(art.find('a', class_ = 'meta-item'))
                
                temp_time = existence(art.find('time', class_ = 'meta-item'))

                temp_imgurl = "https://www.freecodecamp.org"+art.a.img['srcset']
                
                descrip = "https://www.freecodecamp.org"+art.div.div.header.h2.a['href']
                
                descr = requests.get(descrip).content
                des = BeautifulSoup(descr, 'html.parser')
                temp_des = des.find('section', class_ = 'post-content').p.text
                
                article = {'Title': temp_title, 'Author': temp_author,
                           'Description': temp_des, 'Time': temp_time,
                           'Image URL': temp_imgurl,
                           'Link': descrip}
                
                #print(article)
                arts.append(article)
                
                #writing to json file
                      
            i = i+1
            url = requests.get(f'https://www.freecodecamp.org/news/tag/{t}/{i}')
            soup = BeautifulSoup(url.content, 'html.parser')
            
        json_obj = json.dumps(arts, indent = 4)
        with open(f'{t}.json', 'a') as tag:
            tag.write(json_obj)
            #print("File saved as sample.json") 
        

#main function
scrapInfo(tags)
