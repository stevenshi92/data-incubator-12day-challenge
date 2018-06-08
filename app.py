import quandl
import pandas as pd
from bokeh.plotting import figure, output_file, show
#import datetime 
#from dateutil.relativedelta import relativedelta
import requests

from flask import Flask,render_template, request,redirect

import numpy as np
from bokeh.embed import components,file_html
from bokeh.resources import CDN

app = Flask(__name__)
app.vars = {}
@app.route('/index', methods =['GET', 'POST'])

def index():
    if request.method == 'GET':
    	return render_template('Search.html')
    else:
        app.vars['ticker'] = request.form['TickerChoice']
        print("User Requested: "+request.form['TickerChoice'])
 #       now = datetime.datetime.now()
        quandl.ApiConfig.api_key = 'bq-fGp51WgjKuyvZagZm'
        stockDF = quandl.get("WIKI/"+app.vars['ticker'], returns='pandas', end_date='2018-01-01', start_date='2017-01-01')
 #       columns =['Adj. Open','Open','Adj. Close','Close']
#        subDF=stockDF[columns]
#        feature_names=subDF.columns.values.tolist()
        select_feature_name = request.form.get("feature_name")
        #if select_feature_name == None:
 #           select_feature_name = "Close"
        window_size = 30
        window = np.ones(window_size)/float(window_size)    
        p = figure(plot_width=800, plot_height=400, 
            x_axis_type = 'datetime', x_axis_label="The Past Year",
            y_axis_label=app.vars["ticker"]+' '+select_feature_name+" Price")
        p.line(stockDF.index, stockDF[select_feature_name].values.tolist())

        script, div = components(p)
        return render_template('Plot.html', script=script, div=div)
        
    
@app.route('/', methods=['GET','POST'])
def main():
    return redirect('/index')

if __name__ == "__main__":
    app.run(port=33508, debug = True)
