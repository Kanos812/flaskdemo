"""
CP1404 Practical 10 - Flask Demo
Integrating Wikipedia API onto a Flask application
Harrison O'Kane
"""

from flask import Flask, render_template, request, redirect, url_for, session
import wikipediaapi

app = Flask(__name__)
# Set the secret key. Keep this really secret:
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'

# Create an instance of the Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='YourAppName/1.0 (Your Contact Info)')

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")

@app.route('/results')
def results():
    search_term = session.get('search_term', None)
    if search_term:
        page = get_page(search_term)
        return render_template("results.html", title=page.title, summary=page.summary[:500], url=page.fullurl)
    return redirect(url_for('search'))

def get_page(search_term):
    page = wiki_wiki.page(search_term)
    if page.exists():
        return page
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
