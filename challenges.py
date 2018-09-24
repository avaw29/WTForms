#import statements go here
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email

import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

#create class to represent WTForm that inherits flask form
class songForm(FlaskForm):
    artist = StringField('What artist do you want to search for?', validators=[Required()])
    results = StringField('How many results do you want to see?', validators=[Required()])
    email = StringField('Email:', validators=[Required(), Email()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    simpleForm = songForm()
    #what code goes here?
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    form = songForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        artist = form.artist.data
        results = form.results.data
        email = form.email.data
        base_url = 'https://itunes.apple.com/search'
        params_d = {}
        params_d['term'] = artist
        params_d['limit'] = results
        req = requests.get(base_url, params = params_d)
        s = json.loads(req.text)
        return render_template('itunes-result.html', res=s['results'], form=form)
    #what code goes here?
    # HINT : create itunes-results.html to represent the results and return it
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
