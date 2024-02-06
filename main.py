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
    print('Site:\n' + site)

    # get the response and BeautifulSoup
    rs = getResponseAndSoup(site)

    # check if you got the BeautifulSoup
    # if not, alert the user that the response was invalid
    if len(rs) == 1:
        print('Invalid Response Status Code: ' + rs[0])
    # if so, proceed
    else:
        # get all the embedded references on the website
        refs = getReferencesResponses(rs[1])

        # calculate and print the total size, in bytes, of the base HTML page 
        totalSize = 0
        contentList = {}
        totalSize += len(rs[0].content)
        # and all its embedded objects
        for ref in refs:
            totalSize += len(ref.content)
            contentType = ref.headers.get('Content-Type')
            contentList[contentType] = contentList.get(contentType,0)+ 1
        print('Total size, in bytes, of the base HTML page and all its embedded objects:\n' + str(totalSize))

        # calculate and print the percentage of objects for each Content-Type category
        print('Percentage of objects on the page that fall into each Content-Type category:')
        for contentType, count in contentList.items():
            percentage = (count/len(refs)) * 100 
            print(f"{contentType}: {percentage:}%")

        # calculate and print the percentage of objects on the site that aren't from the base domain
        print('Percentage of objects on the page that are hosted on a different domain than the base HTML page:')
        print(differentDomainPercentage(site, rs[1]))

        
        

def getResponseAndSoup(site):
    """ Gets a request and (maybe) a BeautifulSoup for a given website """
    # make a list to be returned
    lst = []

    # get the response and set it to be returned
    response = requests.get(site)
    lst.append(response)

    # if there is a valid response, return the BeautifulSoup and response
    if response.status_code == 200:
        text = response.text                        # grab the HTML text from the response to pass to the constructor
        soup = BeautifulSoup(text, 'html.parser')   # create a BeautifulSoup for the response
        lst.append(soup)                            # add theBeautifulSoup to the return

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
        try:                            # if the request for the source url is valid, add it to the list
            r = requests.get(url)
            if r.status_code == 200:
                refs.append(r)
        except: pass                    # if the url is invalid, move on    

    # return the list
    return refs

def getSourcesURLs(soup: BeautifulSoup):
    """ Returns all the embedded references on a BeautifulSoup """
    srcs = srcs = soup.find_all(attrs={'src':True}) # get all the URLs from the src objects
    urls = []
    for i in range(0, len(srcs)):
        urls.append(srcs[i].get('src'))
    return urls


def differentDomainPercentage(site: str, soup: BeautifulSoup):
    """ Gets the percentage of objects on the page that are hosted on a different domain than the base HTML page """
    urls = getSourcesURLs(soup)          # get the URL for the site's references
    baseDomain = getDomainFromURL(site)  # get the domain for the site
    count = 0                            # number of references whose domain does not match the base domain

    for url in urls:                     # check the domain for each reference against the base domain
        domain = getDomainFromURL(url)   # extract the domain from the refernce URL
        if domain != baseDomain:              
            count += 1                   # if the URL's domain is different than the base domain, increase the count

    return count / len(urls) * 100       # return the percentage

def getDomainFromURL(url: str)->str:
    """ 
        Returns the domain from a given URL
        Assuming it is in the form https://domain..., http://domain...
    """
    firstSlash = url.find('/')                  # the domain should be in between the first and third slashes in the URL
    secondSlash = url.find('/', firstSlash+1)
    thirdSlash = url.find('/', secondSlash+1)
    if thirdSlash == -1: thirdSlash = len(url)          
    return url[secondSlash+1:thirdSlash]
    

def main():
    question2('https://www.youtube.com')
    # question2('https://beautiful-soup-4.readthedocs.io/en/latest/')
    # question2('https://requests.readthedocs.io/en/latest/')
    
if __name__ == '__main__':
    main()
    