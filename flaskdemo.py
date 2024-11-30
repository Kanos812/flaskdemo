from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# Set the secret key. Keep this really secret:
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return "I am still working on this"

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")

@app.route('/results')
@app.route('/results')
def results():
    # Check if the user selected a disambiguation option
    search_term = request.args.get('search')
    if search_term:
        session['search_term'] = search_term  # Update the session with the new term

    # Get the term from the session (updated or original)
    search_term = session.get('search_term')
    if not search_term:
        return render_template("results.html", page={"error": "no_results"})

    # Fetch the page or disambiguation options
    page = get_page(search_term)
    return render_template("results.html", page=page)



def get_page(search_term):
    try:
        # Search for possible matches
        search_results = wikipedia.search(search_term)
        if not search_results:
            return {"error": "no_results"}  # No results found

        # Attempt to fetch the most relevant page
        page = wikipedia.page(search_results[0])
    except wikipedia.exceptions.DisambiguationError as e:
        # Return the list of options for user selection
        return {"error": "disambiguation", "options": e.options}
    except wikipedia.exceptions.PageError:
        # Page does not exist
        return {"error": "page_error"}
    except wikipedia.exceptions.WikipediaException as e:
        # Catch-all for other Wikipedia-related errors
        return {"error": "unexpected", "message": str(e)}

    return {"title": page.title, "summary": page.summary, "url": page.url}

if __name__ == '__main__':
    app.run()
