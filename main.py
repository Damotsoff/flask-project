from flask import Flask, render_template, request, escape
from search import search4letters
from dbcm import UseDatabase
from cheker import check_logged_in


app = Flask(__name__)
app.config['dbconfig'] = {
    'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'vsearchpasswd',
            'database': 'vsearchlogDB'
}


def log_request(req: 'flask_request', res: str) -> None:
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
                    (phrase, letters, ip, browser_string, result)
                    values(%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res, ))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your result'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('result.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,
                           the_title=title)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to Search Leaters on the Web')


@app.route('/viewlog')
@check_logged_in
def view_log() -> 'html':
    contents = []
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, result from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Phrase', 'Letters',
              'Remote_addr', 'User_agent', 'Result')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=contents
                           )


app.secret_key = 'mysecretKey'
print('We start off in:', __name__)
if __name__ == '__main__':
    app.run(debug=True)
