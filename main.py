# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:25:10 2024

@author: Josh Berger
"""

import requests
from bs4 import BeautifulSoup

def placeholder(site):
    """ Function to answer question 2 """
    soup = getSoup(site)
    refs = getReferences(soup)
    for ref in refs:
        print(ref)

    
def getSoup(site):
    """ Gets a Beautiful Soup obect for a given website """
    response = requests.get(site)
    if response.status_code == 200:
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        return soup

def getReferences(soup: BeautifulSoup):
    """ Gets an array of referenced URLs for a BeautifulSoup """
    srcs = soup.find_all(attrs={'src':True})
    refs = list()
    for i in range(0, len(srcs)):
        # refs.append(getSoup(srcs[i].get('src')))
        refs.append(srcs[i].get('src'))
    return refs

def main():
    placeholder('https://www.youtube.com')
    #placeholder('https://www.amazon.com')
    #placeholder('https://www.twitter.com')
    
if __name__ == '__main__':
    main()
    