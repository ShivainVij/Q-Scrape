import urllib, re, os, random
import urllib.request
from bs4 import BeautifulSoup as soup
import xlsxwriter
import pandas as pd

from urllib.request import Request, urlopen

os.system('cls')

def Convert():
    # Filenames
    excel_names = ["KahootQuizTemplate-3 (3).xlsx", "arrays.xlsx"]

    # Read them in
    excels = [pd.ExcelFile(name) for name in excel_names]

    # Turn them into dataframes
    frames = [x.parse(x.sheet_names[0], header=None,index_col=None) for x in excels]

    # Delete the first row for all frames except the first
    frames[1:] = [df[1:] for df in frames[1:]]

    # Concatenate them..
    combined = pd.concat(frames)

    # Write it out
    combined.to_excel("c.xlsx", header=False, index=False)

def Exporter(array):
    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0

    transposed_array = zip(*array)

    for col, data in enumerate(transposed_array):
        worksheet.write_column(row, col, data)
        # os.system('clear')

    workbook.close()

    print("\nKahoot File Exported!\n")

def QuizletScraper():

    #Parsing Overall Subject

    urls = []

    subject = input("What would you want to learn about: ")
    subject = subject.replace(" ", "-")

    searchQ = 'https://quizlet.com/subject/%s/?price=free&type=sets&creator=all' % subject
    f1 = Request(searchQ, headers={'User-Agent': 'Mozilla/5.0'})
    f = urllib.request.urlopen(f1)
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
        f1 = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        f = urllib.request.urlopen(f1)
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

    return words, meanings

def Singleplayer(words, meanings):

    #Printing Terms and Definitions

    while len(words) - 1 > 4:
        tmp = set()

        while len(tmp) != 4:
            num = random.randint(0, len(words) - 1)
            tmp.add(num)

        tmp = list(tmp)
        correct = tmp[0]
        random.shuffle(tmp)

        while True:

            os.system('cls')

            print("%s\n" % meanings[correct])

            for i in range(1, 5):
                print("%i. %s" % (i, words[tmp[i - 1]]))

            answer = input("\nAnswer (1-4): ")

            if answer not in ['1', '2', '3', '4']:
                print("That's not an option! Press Enter to Continue! ")
                input()
            else:
                break

        if words[tmp[int(answer) - 1]] == words[correct]:
            print("\nYou got it! The answer was %s!" % words[correct])
        else:
            print("\nOh no! That's not the correct answer! The correct answer was number %i, %s\n" % (tmp.index(correct) + 1, words[correct]))

        #TODO: Add difficulty?

        input("Press Enter to Continue")
        os.system('cls')

        words.remove(words[correct])
        meanings.remove(meanings[correct])

def Multiplayer(words, meanings):
    arr = []

    for i in range(20):
        l = [i + 1]
        tmp = set()

        while len(tmp) != 4:
            num = random.randint(0, len(words) - 1)
            if len(meanings[num]) < 95 and len(words[num]) < 60:
                tmp.add(num)

        tmp = list(tmp)
        correct = tmp[0]
        random.shuffle(tmp)

        l.append(meanings[correct])

        for i in range(1, 5):
            l.append(words[tmp[i - 1]])

        l.append(10)

        for i in range(4):

            if words[tmp[i - 1]] == words[correct]:
                if i + 1 == 1:
                    l.append(4)
                else:
                    l.append(i)

                break

        arr.append(l)

    Exporter(arr)

#Main Program

while True:
    os.system('cls')

    print("Welcome to QScraper! Please select an option: \n")

    print("1. Singleplayer Study")
    print("2. Multiplayer Kahoot Export\n")


    i = input("Option (1 or 2): ")

    if i not in ['1', '2']:
        print("Oh no! That's not an option! Press Enter to Continue")
        input()
    else:
        break

os.system('cls')

words, meanings = QuizletScraper()

os.system('cls')

if i == '1':
    Singleplayer(words, meanings)
else:
    Multiplayer(words, meanings)
    Convert()
