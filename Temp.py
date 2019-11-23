import urllib, re, os
import random

def QuizletScam(subject):



    os.system('clear')

    url1 = "https://quizlet.com/subject/"
    url2 = url1 + subject

    f = urllib.urlopen(url2)
    html = f.read()

    x = re.split('class="UILink" data-sourcename="" href="', html)
    x.remove(x[0])

    urls = []

    for i in range(len(x)):
        tmp = ""
        for j in range(len(x[i])):
            if x[i][j] == '"' and x[i][j + 2] == 't':
                urls.append(tmp)
                break
            tmp += x[i][j]

    for url in urls:
        f = urllib.urlopen(url)
        html = f.read()

        x = re.split('TermText notranslate lang-', html)
        x.remove(x[0])

        for i in range(len(x)):
            x[i] = x[i][4:]

        final = []

        for i in range(len(x)):
            tmp = ""
            for j in range(len(x[i])):
                if x[i][j] == '<' and x[i][j + 1] == '/':
                    if '<br>' in tmp:
                        tmp = tmp.replace('<br>', " ")
                    final.append(tmp)
                    break
                tmp += x[i][j]

        dict = {}

        for i in range(0, len(final), 2):
            tmp = {final[i]:final[i+1]}
            dict.update(tmp)

        keys = []

        for i in dict:
            keys.append(i)

        # for i in dict:
        #     #print("%s: %s" % (i, dict[i]))
    tmp = random.randint(0,len(keys))
    print("Define: %s" % (keys[tmp]))
    raw_input()
    print("Answer: %s" % (dict[keys[tmp]]))
    print('')

#TODO: Set loop, remove key from used questions

QuizletScam(raw_input("What subject would you like to see: "))
