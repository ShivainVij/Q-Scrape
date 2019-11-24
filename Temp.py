import urllib, re, os, random
from bs4 import BeautifulSoup as soup

os.system('clear')

def QuizletScraper():

    #Parsing Overall Subject

    urls = []

    subject = raw_input("What would you want to learn about: ")
    subject = subject.replace(" ", "-")

    searchQ = 'https://quizlet.com/subject/%s/?price=free&type=sets&creator=all' % subject
    f = urllib.urlopen(searchQ)
    html = f.read()
    f.close()

    soup_page = soup(html, "html.parser")
    links = soup_page.findAll("div", {"class":"SearchPage-result js-setResult"})

    for link in links:
        linkHTML = link.div.div.findAll("div", {"class":"UILinkBox-link"})

        for html in linkHTML:
            urls.append(html.a["href"])

    #Parsing individual Quizlets

    words = []
    meanings = []

    for url in urls:

        print("Loading: %i Percent" % int(float((urls.index(url) + 1))/float(len(urls)) * 100))

        f = urllib.urlopen(url)
        html = f.read()
        f.close()

        soup_page = soup(html, "html.parser")
        terms = soup_page.findAll("a", {"class":"SetPageTerm-wordText"})
        definitions = soup_page.findAll("a", {"class":"SetPageTerm-definitionText"})

    #Appending Terms and Definitions

        for i in range(len(terms)):
            words.append(terms[i].text)
            meanings.append(definitions[i].text)

    print ''

    #Printing Terms and Definitions

    while len(words) - 1 != 0:
        num = random.randint(0, len(words) - 1)

        print("Define %s" % words[num])
        raw_input()
        print("Answer is %s\n" % meanings[num])

        words.remove(words[num])
        meanings.remove(meanings[num])

QuizletScraper()
