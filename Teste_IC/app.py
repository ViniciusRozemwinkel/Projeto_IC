from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("Homepage.html")

@app.route('/item')
def itempage():
    return render_template("itens.html")

@app.route('/solver')
def solverpage():
    return render_template("Solver.html")



if __name__ == '__main__':
    app.run(debug=True)
