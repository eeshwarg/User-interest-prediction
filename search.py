import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import lxml
import urllib2
import hashlib

# REVIEW: The HTML webpage provides different results from original page. Also, SafeSearch is on. Must change URL.
def retrieveURLs(query, results=5):
    query = query.replace(' ', '+')
    req = requests.get('https://www.duckduckgo.com/html/?q=' + query)
    soup = BeautifulSoup(req.text, 'lxml')
    # print soup.prettify()
    urlList = []
    count = 0
    for link in soup.find_all('a', class_ = 'result__url'):
        urlString = link['href']
        encodedUrl = urlString.split('uddg=')[1]
        decodedUrl = urllib2.unquote(encodedUrl).decode('utf8')
        urlList.append(decodedUrl)
        count+=1
        if count == results:
            break
    return urlList

def tagVisible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def getPageText(url):
    # print url
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tagVisible, texts)
    result = u" ".join(t.strip() for t in visible_texts)
    # print result
    return result

def searchAndStore(querySet, resultsPerQuery=5, savepath="/home/keerthan/Coursework/DWDM/"):
    urlVisited = set()
    h = hashlib.md5()

    def hashIt(url):
        h.update(url)
        return h.hexdigest()

    for query in querySet:
        urlList = retrieveURLs(query, results=resultsPerQuery)
        urlVisited.update(urlList)

    urlVisited = list(urlVisited)
    print urlVisited
    hashedUrl = map(hashIt, urlVisited)
    pageText = map(getPageText, urlVisited)
    for i, text in enumerate(pageText):
        filename = savepath + str(hashedUrl[i]) + '.txt'
        f = open(filename, 'w')
        f.write(text.encode('utf-8'))
        f.close()


if __name__ == '__main__':
    searchAndStore(['hello world', 'HELLO WORLD'])
