
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