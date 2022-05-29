from cProfile import label
from dataclasses import dataclass
import json
from re import L
from urllib import response
from flask import Flask, make_response, render_template, request
import pdfkit
import datetime

import urllib.parse



app = Flask(__name__)
data = {}
#Read Data from Json
with open('Data/data.json', 'r') as f:
  data = json.load(f)


@app.route('/',methods=['GET','POST'])
def index():

    p_data,label=process_data(data)

    img_list=[]
    for i in p_data:
        img_list.append(chartjs(p_data[i],label['label'],i))

    rendered = render_template('index.html',img=img_list)
    
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



def process_data(data):
    keys=data['data']['filter_metrics']
    print(keys)
    process_data=data['data']['time_series_graph']
    label=dict()
    temp_dict=dict()
    for i in keys:
        label['label']=[]
        temp_dict[i]=[]
        for d in process_data:
            if i in d.keys():
                temp_dict[i].append(d[i])
                label['label'].append(urllib.parse.quote("'" + date_time(d['label']) + "'"))
    return temp_dict,label



def chartjs(data,label,key):

    key=key.upper()


    label = ','.join([str(a) for a in label])
    data = ','.join([str(a) for a in data])
    chart="http://localhost:3400/chart?v=3&c={ type: 'line', data: { labels: ["+label +"], datasets: [ { label: '"+key+"', backgroundColor: 'rgb(204,229,255)', borderColor: 'rgb(0,191,255)', data: ["+data+"], fill: true, borderWidth:1,pointRadius:1}, ], }, options: {plugins: { legend: {position: 'top',align: 'start',labels: { boxWidth: 0,} }, } } }"

    return chart




def date_time(date):
    cr_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    cr_date = cr_date.strftime("%d %b")
    return cr_date


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)