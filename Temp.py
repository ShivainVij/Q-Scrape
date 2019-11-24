import urllib, re, os, random
from bs4 import BeautifulSoup as soup
from flask import Flask, render_template

os.system('clear')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/QScrape")
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

    for url in urls:

        f = urllib.urlopen(url)
        html = f.read()
        f.close()

        soup_page = soup(html, "html.parser")
        terms = soup_page.findAll("a", {"class":"SetPageTerm-wordText"})
        definitions = soup_page.findAll("a", {"class":"SetPageTerm-definitionText"})

    #Printing Terms and Definitions

        for term in terms:
            print(term.text)
        print('')

        for definition in definitions:
            print(definition.text)
        print('')

if __name__ == "__main__":
    app.run(debug=True)
