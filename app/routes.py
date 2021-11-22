from flask import render_template, request
from app import app
import functions

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    startdate = request.form.get('startdate')
    enddate = request.form.get('enddate')
    results = functions.get_btc_data(startdate, enddate)
    return render_template('result.html', results=results)