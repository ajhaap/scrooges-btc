from flask import render_template, request
import functions


def index():
    return render_template('index.html')

def result():
    startdate = request.form.get('startdate')
    enddate = request.form.get('enddate')
    results = functions.get_btc_data(startdate, enddate)
    return render_template('result.html', results=results)