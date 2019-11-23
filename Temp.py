import urllib, re

url = "https://quizlet.com/410470979/ropa-for-exam-flash-cards/"

f = urllib.urlopen(url)
html = f.read()

x = re.split('TermText notranslate lang-">', html)
x.remove(x[0])

# for i in range(len(x)):
#     x[i] = x[i][]

print(x)

exit()

final = []

for i in range(len(x)):
    tmp = ""
    for j in range(len(x[i])):
        if x[i][j] == '<' and x[i][j + 1] == '/':
            final.append(tmp)
            break
        tmp += x[i][j]

print(final)

# dict = {}
#
# for i in range(0, len(final), 2):
#     tmp = {final[i]:final[i+1]}
#     dict.update(tmp)
#
# print(dict)


# start = '"SetPageTerms-termsList"'
# key = 'TermText notranslate lang-en">'
