
from flask import Flask, render_template, request, Response
import json
import pdb

# other parts of 
import analyze
import bag


################ FLASK PROTOCOL BEGINS ###################
app = Flask(__name__)

# example - by Jonathan
@app.route('/add', methods=['POST'])
def add():
    #pdb.set_trace()
    if request.method == 'POST':
        # download html, parse text into individual words
        #print "generating response for URL: " + response.form['site']
        article_bag = bag.get_bag(request.form['site'])

        # analysis is done as part of generating output

        data = {
            'input' : request.form,
            'output' : analyze.run_analysis(article_bag)
        }
        js = json.dumps(data)

        return Response(js, status=200, mimetype='application/json')
    else:
        return "Must POST for this method to work"


@app.route('/hello')
def hello_world():
    return 'Hello World test successful'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)

