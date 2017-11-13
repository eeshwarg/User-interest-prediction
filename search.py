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
    result = u''
    try:
        session = requests.Session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
        req = session.get(url, verify=False)
        soup = BeautifulSoup(req.text, 'lxml')
        texts = soup.findAll(text=True)
        visible_texts = filter(tagVisible, texts)
        result = u" ".join(t.strip() for t in visible_texts)
    except:
        result = u''
    return result

def savePageText(url, filename):
    pageText = getPageText(url)
    if pageText!= u'':
        f = open(filename, 'w')
        f.write(pageText.encode('utf-8'))
        f.close()
    return

def searchAndStore(querySet, resultsPerQuery=5, savepath="/home/keerthan/Coursework/DWDM/", saveURL=False):
    urlVisited = set()
    h = hashlib.md5()

    def hashIt(url):
        h.update(url)
        return h.hexdigest()

    print "Extracting result urls...",
    for query in querySet:
        urlList = retrieveURLs(query, results=resultsPerQuery)
        urlVisited.update(urlList)
    urlVisited = list(urlVisited)
    print "Done"
    print str(len(urlVisited)) + " distinct urls extracted."

    if saveURL:
        print "Saving result urls...",
        filename = savepath + "urls.txt"
        f = open(filename, 'w')
        for url in urlVisited:
            f.write('%s\n' % urlVisited)
        f.close()
        print "Done."

    print "Extracting and saving page texts...",
    hashedUrl = map(hashIt, urlVisited)
    for i, url in enumerate(urlVisited):
        filename = savepath + str(hashedUrl[i]) + '.txt'
        savePageText(url, filename)
    print "Done."

if __name__ == '__main__':
    searchAndStore(['hello world', 'HELLO WORLD'])
