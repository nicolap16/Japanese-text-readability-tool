from flask import render_template, url_for
from readability import app


from readability.models import Word

@app.route('/')
def home():
  return render_template('home.html', title='Home')

@app.route("/results")
def results(): 
  return render_template('results.html', title='Results') 

@app.route("/vocab_list")
def vocab_list():
  words=Word.query.all()
  return render_template('vocab_list.html', title='Vocab List', words = words) 