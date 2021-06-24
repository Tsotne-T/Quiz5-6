import requests
import json
from re import template
from typing import Text
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Anime'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///waifu.sqlite'

db=SQLAlchemy(app)



class Waifus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    anime = db.Column(db.String(40), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def ___str___(self):
        return f'Waifu name:{self.name}; Anime: {self.anime}; rating: {self.rating}'

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():    
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('home'))
    
    return render_template('login.html')

    



@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')

    


@app.route('/addWaifu', methods=['GET', 'POST'])
def books():
    if request.method=='POST':
        n = request.form['name']
        a = request.form['anime']
        r = request.form['rating']

        if n=='' or a== '' or r=='':
            flash('Fill the lines', 'error')
            
        elif not r.isnumeric():
            flash('In rating please enter number type value', 'error')    

        else:  
            w1 = Waifus(name=n, anime=a, rating=float(r))
            db.session.add(w1)
            db.session.commit()
            flash('Definitly a good Waifu', 'info')

    return render_template('addwaifu.html')

r =  requests.get('https://animechan.vercel.app/api/random')
res = r.json()

with open("Finaluri\Anime.Json","w") as f:
    json.dump(res, f, indent=4)

with open('Finaluri\Anime.Json') as json_file:
    data = json.load(json_file)


@app.route('/quote')
def quote():  
        return render_template('quote.html', data = data['quote'], character = data['character'],anime = data['anime'])


if __name__ == "__main__":
    app.run(debug=True)