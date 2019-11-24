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
    final = {}

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

        for i in range(len(words)):
            tmp = {words[i]:meanings[i]}
            final.update(tmp)

    words = []
    meanings = []

    for i in final:
        words.append(i)
        meanings.append(final[i])

    print ''

    #Printing Terms and Definitions

    while len(words) - 1 > 4:
        tmp = set()

        while len(tmp) != 4:
            num = random.randint(0, len(words) - 1)
            tmp.add(num)

        tmp = list(tmp)
        correct = tmp[0]
        random.shuffle(tmp)

        os.system('clear')

        print("%s\n" % meanings[correct])

        for i in range(1, 5):
            print("%i. %s" % (i, words[tmp[i - 1]]))

        answer = raw_input("\nAnswer (1-4): ")

        #TODO: Add difficulty

        print("\nThe correct answer is number %i, %s\n" % (tmp.index(correct) + 1, words[correct]))
        raw_input("Press Enter to Continue")
        os.system('clear')

        words.remove(words[correct])
        meanings.remove(meanings[correct])

    # while True:
    # print("Question: A trait that is not as prevalent in a species?")
    # input = raw_input("Answer: ")

    # if input.lower() != "recessive":
    #     print("WRONNGNGG!")
    #     continue
    # else:
    #     print("Yay")
    #     again = raw_input("Again? ")
    #
    #     if again.lower() == "yes":
    #         continue
    #     break

QuizletScraper()
