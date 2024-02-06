# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:25:10 2024

@author: Josh Berger
"""

import requests
from bs4 import BeautifulSoup

def question2(site):
    """ Function to answer Question 2 """
    # get the response and BeautifulSoup
    rs = getResponseAndSoup(site)

    # check if you got the BeautifulSoup
    # if not, alert the user that the response was invalid
    if len(rs) == 1:
        print("Invalid Response Status Code: " + rs[0])
    # if so, proceed
    else:
        refs = getReferencesResponses(rs[1])

def getResponseAndSoup(site):
    """ Gets a request and (maybe) a BeautifulSoup for a given website """
    # make a list to be returned
    lst = []

    # get the response and set it to be returned
    response = requests.get(site)
    lst.append(response)

    # if there is a valid response, return the BeautifulSoup and response
    if response.status_code == 200:
        # grab the HTML text from the response to pass to the constructor
        text = response.text
        # create a BeautifulSoup for the response
        soup = BeautifulSoup(text, 'html.parser')
        # add theBeautifulSoup to the return
        lst.append(soup)

    # if not, return just the response
    return lst


def getReferencesResponses(soup: BeautifulSoup):
    """ Gets an array of all embedded references for a BeautifulSoup as responses """
    # get all the src tags from the website
    srcs = soup.find_all(attrs={'src':True})

    # gather all the urls from the src tags
    # create a response for them and add them to a list
    refs = []
    for i in range(0, len(srcs)):
        refs.append(requests.get(srcs[i].get('src')))

    # return the list
    return refs

def main():
    question2('https://www.youtube.com')
    
if __name__ == '__main__':
    main()
    