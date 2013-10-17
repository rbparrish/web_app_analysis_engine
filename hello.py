
from flask import Flask, render_template, request, Response
import json
import pdb

#this python
import analyze

#### TOKENIZE AND NORMALIZE FUNCTION ####
import nltk
from nltk import tokenize
from nltk.corpus import stopwords
import unicodedata
wnl = nltk.WordNetLemmatizer()


def tokenize_and_normalize(chunks):
    words = [ tokenize.word_tokenize(sent) for sent in tokenize.sent_tokenize("".join(chunks)) ]
    flatten = [ inner for sublist in words for inner in sublist ]
    stripped = [] 

    for word in flatten: 
        if word not in stopwords.words('english'):
            try:
                stripped.append(word.encode('latin-1').decode('utf8').lower())
            except:
                print "Cannot encode: " + word
            
    no_punks = [ word for word in stripped if len(word) > 1 ] 
    return [wnl.lemmatize(t) for t in no_punks]


#### CREATE BAG FUNCTION ####
import requests
from bs4 import BeautifulSoup

def get_bag(html_full_page):
    raw_html = requests.get(html_full_page)
    soup_html = BeautifulSoup(raw_html.text)

    l = []
    article_string = ""
    web_text = soup_html.find_all('div', class_="articleBody")
    
    for each in web_text:
        res = each.find_all('p')
        for i in res:
            l.append(i)

    #pulling out all except last 'mini-paragraph' that contains author's name
    for n in range(len(l)-2):
        article_string = article_string + l[n].get_text()

    #article_string now ready for tokenization

    print "article downloaded and text extracted"

    return tokenize_and_normalize(article_string)


################ FLASK PROTOCOL BEGINS ###################
app = Flask(__name__)

# example - by Jonathan
@app.route('/add', methods=['POST'])
def add():
        

        if request.method == 'POST':
                # download html, parse text into individual words
                article_bag = get_bag(request.form['site'])

                # analysis is done as part of generating output

                data = {
                 'input' : request.form,
                 'output' : analyze.run_analysis(article_bag)
                }
                js = json.dumps(data)
                return Response(js, status=200, mimetype='application/json')
        else:
                return "POST NUMBERBERSBERS!!!"


@app.route('/hello')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)

