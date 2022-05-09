from flask import Flask, render_template
from logging.config import dictConfig
import json

with open('logging.json', 'rt') as file :
    dictConfig(json.load(file))

app = Flask(__name__)

@app.context_processor
def date_formatter() :
    def format_date(date) :
        if date is not None :
            TIME_FORMAT = '%Y-%m-%d, %H:%M:%S'
            return date.strftime(TIME_FORMAT)
        else :
            return '' 
    return dict(format_date=format_date)

@app.route('/')
def messages() :
    return render_template('tatort.html')

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=8000, debug=True)
