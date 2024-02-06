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
        try:
        # if the request for the source url is valid, add it to the list
            r = requests.get(srcs[i].get('src'))
            if r.status_code == 200:
                refs.append(r)
        except:
        # if the url is invalid, move on    
            pass

    # return the list
    return refs

def main():
    question2('https://www.youtube.com')
    # question2('https://beautiful-soup-4.readthedocs.io/en/latest/')
    # question2('https://requests.readthedocs.io/en/latest/')
    
if __name__ == '__main__':
    main()