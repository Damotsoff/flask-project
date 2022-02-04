from crypt import methods
from distutils.log import debug
from unittest import result
from flask import Flask,render_template,request
from search import search4letters


app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return 'Hello world'


@app.route('/search4',methods=['POST'])
def do_search() -> 'html':
    phrase =request.form['phrase']
    letters =request.form['letters']
    title = 'Here are your result'
    results = str(search4letters(phrase,letters))
    return render_template('result.html',the_phrase =phrase,the_letters = letters,\
        the_results =results,the_title =title)


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title = 'Welcome to Search Leaters on the Web')


app.run(debug=True)