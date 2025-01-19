from flask import Flask, render_template, request
from .modele import db_identification

app = Flask(__name__)
@app.route('/')
def index(erreur=False):
    return render_template('index.html', erreur=erreur)

@app.route('/admin/authentifier/', methods=['GET','POST'])
def reponse():
    if request.method == 'POST':
        resultat = request.form
        rows = db_identification(resultat)
        if rows != []:
            return render_template('apres_auth.html', rows=rows)
        else:
            return render_template('index.html', erreur=True)
