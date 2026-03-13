from flask import Flask, render_template, request

app = Flask(__name__)

EMAIL = "manager@staffly.com"
MOT_DE_PASSE = "staffly123"

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/connexion', methods=['POST'])
def connexion():
    email = request.form['email']
    mdp = request.form['mdp']
    if email == EMAIL and mdp == MOT_DE_PASSE:
        return render_template('bravo.html')
    else:
        return render_template('login.html', erreur="Email ou mot de passe incorrect !")

if __name__ == '__main__':
    app.run(debug=True)