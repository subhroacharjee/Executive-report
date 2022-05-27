from crypt import methods
from distutils.dir_util import remove_tree
import json
import re
import time
from urllib import response
from flask import Flask, make_response, render_template, request
import pdfkit 
import os



app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    print(request.method)  
    if request.method=='GET':
        rendered = render_template('chart.html')
        data=request.data.decode('UTF-8')  
    if request.method=='POST':
        print()
        rendered = render_template('index.html',img=data)
    
    options = {
        
    'page-size': 'A4',
    'margin-right': '0.25in',
    'margin-bottom': '0.25in',
    'margin-left': '0.30in',
    'margin-top':'0.25in',
    }

    
    


    pdf=pdfkit.from_string(rendered,options=options)

    response = make_response(pdf)
    response.headers['Content-type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=Blkbox-Report.pdf'

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)