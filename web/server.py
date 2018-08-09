from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    print("At home page")
    return render_template("homePage.html")

@app.route('/results/', methods=['GET', 'POST'])
def results():
    if (request.method == 'POST'):
        data = request.form
    else:
        data = request.args
    
    query = data.get('searchterm')
    print("You searched for: " + query)
    return render_template('results.html', query=query)

if (__name__ == '__main__'):
    app.run(debug=True)