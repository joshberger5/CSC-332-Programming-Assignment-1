# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 16:25:10 2024

@author: Josh Berger and Matt Keller
did it work
"""

import requests
from bs4 import BeautifulSoup
import time

def question2(site):
    """ Answer Question 2 """
    # print the sitename
    print(site)

    # get the response and BeautifulSoup
    rs = getResponseAndSoup(site)

    # check if you got the BeautifulSoup
    # if not, alert the user that the response was invalid
    if len(rs) == 1:
        print("Invalid Response Status Code: " + rs[0])
    # if so, proceed
    else:
        # get all the embedded references on the website
        refs = getReferencesResponses(rs[1])

        # calculate and print the total size, in bytes, of the base HTML
        # page and all its embedded objects
        totalSize = 0
        contentList = {}
        
        totalSize += len(rs[0].content)
        contentType = rs[0].headers.get('Content-Type')
        contentList[contentType] = contentList.get(contentType,0) + 1
        for ref in refs:
            totalSize += len(ref.content)
            contentType = ref.headers.get('Content-Type')
            contentList[contentType] = contentList.get(contentType,0) +1
            
        print("Total Size: " + str(totalSize))

        for contentType, count in contentList.items():
            percentage = (count/len(refs)) * 100 if len(refs) > 0 else 0
            print(f"{contentType}: {percentage:}%")

        print(domainPercentages(site, rs[1]))

        
        

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
    urls = getSourcesURLs(soup)

    # gather all the urls from the src tags
    # create a response for them and add them to a list
    refs = []
    for url in urls:
        try:
        # if the request for the source url is valid, add it to the list
            r = requests.get(url)
            if r.status_code == 200:
                refs.append(r)
        except:
        # if the url is invalid, move on    
            pass

    # return the list
    return refs

def getSourcesURLs(soup: BeautifulSoup):
    """ Returns all the embedded references on a BeautifulSoup """
    srcs = srcs = soup.find_all(attrs={'src':True})
    urls = []
    for i in range(0, len(srcs)):
        urls.append(srcs[i].get('src'))
    return urls


def domainPercentages(site: str, soup: BeautifulSoup):
    """ Calculates the percentage of references that use each domain for a given soup """
    # get the URL for the site and its references
    urls = getSourcesURLs(soup)
    urls.append(site)

    # make a dictionary to hold the domain names with their respective counts
    domainCounts = dict()

    # add a domain to the dictionary or increase its count
    for url in urls:
        # extract the domain from the URL 
        firstSlash = url.find('/')
        secondSlash = url.find('/', firstSlash+1)
        thirdSlash = url.find('/', secondSlash+1)
        if thirdSlash == -1: thirdSlash = len(url)
        domain = url[secondSlash+1:thirdSlash]

        # if a given domain is not already in the dictionary, add it with a count of 1
        # if it already is, increase the count by 1
        if domain not in domainCounts:
            domainCounts[url[secondSlash+1:thirdSlash]] = 1
        else:
            domainCounts[url[secondSlash+1:thirdSlash]] += 1

    # convert the counts to percentages
    for key in domainCounts.keys():
        domainCounts[key] = domainCounts[key] / len(urls) * 100

    return domainCounts
    

def main():
    question2('https://www.youtube.com')
    # question2('https://beautiful-soup-4.readthedocs.io/en/latest/')
    # question2('https://requests.readthedocs.io/en/latest/')
    
if __name__ == '__main__':
    main()
    