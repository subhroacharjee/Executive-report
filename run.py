import base64
import json
from locale import YESEXPR
from flask import Flask, jsonify, make_response, render_template, request
import pdfkit
import datetime
from quickchart import QuickChart, QuickChartFunction

from src.communication import Communication
from src.parser import get_data_from_request
#config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf') 

import base64
import plotly.graph_objects as go
import plotly.io as pio


app = Flask(__name__)
data = {}

graph_data_phase_1 = None
metrics_phase_1= None
top_creative_phase_1= None

graph_data_phase_2 = None
metrics_phase_2 = None
top_creative_phase_2= None

@app.route('/',methods=['GET','POST'])
def index():
    req_data = get_data_from_request(request)
    if not req_data:
        raise Exception('Invalid data')
    comm = Communication(req_data['adaccount_id'], req_data['start_date'], req_data['end_date'])
    server_data = comm.make_async_requests()

    for i in range(5):
        if server_data[i]:
            print("")
        else:
            server_data[i]=[]

    metrics_phase_1=server_data[0]
    graph_data_phase_1 =server_data[1]
   
    top_creative_phase_1= server_data[2]

    metrics_phase_2 = server_data[3]
    graph_data_phase_2 = server_data[4] 
    top_creative_phase_2= server_data[5]
    
    print(metrics_phase_1['creative_metrics']['win_rate_percent'])

    phase_1_data,label_1=process_data(graph_data_phase_1)
    chart_list_phase_1=[]
    for i in phase_1_data:
        chart_list_phase_1.append(chartjs(phase_1_data[i],label_1['label'],i))

    phase_2_data,label_2=process_data(graph_data_phase_2)
    chart_list_phase_2=[]
    for i in phase_2_data:
        chart_list_phase_2.append(chartjs(phase_2_data[i],label_2['label'],i))
    
    final_data={
        'index_date':index_date(metrics_phase_1['date_range']),
        'phase1':{
            'charts':chart_list_phase_1,
            'metrics':metrics_phase_1,
            'top_creative':top_creative_phase_1,
            'win_rate_chart':win_rate_chart()
        },
        'phase2':{
            'charts':chart_list_phase_2,
            'metrics':metrics_phase_2,
            'top_creative':top_creative_phase_2,
            'win_rate_chart':win_rate_chart()
        }
    }
    rendered = render_template('index.html',final_data=final_data)
    
    options = {
    'page-size': 'A4',
    'margin-right': '0.20in',
    'margin-bottom': '0.20in',
    'margin-left': '0.20in',
    'margin-top':'0.20in',
    }


    pdf=pdfkit.from_string(rendered,options=options, verbose=True)

    response = make_response(pdf)
    response.headers['Content-type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=Blkbox-Report.pdf'

    return response



def process_data(data):
    keys=data['filter_metrics']
    if len(data['show_metrics'])>0:
        keys.remove(data['show_metrics'][0])
        keys.insert(0,data['show_metrics'][0]) 
    print("f",keys)
    process_data=data['time_series_graph']
    label=dict()
    temp_dict=dict()
    for i in keys:
        label['label']=[]
        temp_dict[i]=[]
        for d in process_data:
            if i in d.keys():
                temp_dict[i].append(d[i])
                label['label'].append(date_time(d['label']))
    return temp_dict,label



def chartjs(data,label,key):
    key=key.upper()
    qc = QuickChart()
    qc.width = 900
    qc.height = 400
    qc.device_pixel_ratio = 3.0
    qc.version=3
    
    qc.config = {
         'type': 'line', 
         'data': { 
             'labels': label, 
             'datasets': [ 
                 { 
                 'label':key,
                 'backgroundColor':'rgb(204,229,255)', 
                 'borderColor': 'rgb(30,144,255)', 
                  'data': data, 
                  'fill': True, 
                  'backgroundColor':QuickChartFunction("getGradientFillHelper('vertical', ['rgba(63, 100, 249, 0.2)', 'rgba(255, 255, 255, 0.2)'])"),
                  'borderWidth':2,
                  'pointRadius':2}, ],}, 
                  'options': { 'scales': {'x': {'grid': {'display': False}}}, 'plugins': { 'legend': {'position': 'top','align': 'start','labels': { 'boxWidth': 0,'font': {'size': 17} }, } 
                  } }}
    return qc.get_url()




def date_time(date):
    cr_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    cr_date = cr_date.strftime("%d %b")
    return cr_date

def index_date(date):
    start_date = datetime.datetime.strptime(date['start_date'], '%Y-%m-%d')
    start_date = start_date.strftime("%d %B")
    end_date = datetime.datetime.strptime(date['end_date'], '%Y-%m-%d')
    end_date = end_date.strftime("%d %B")
    year= datetime.datetime.strptime(date['start_date'], '%Y-%m-%d')
    year = year.strftime("%Y")

    d=start_date+" - "+end_date

    final={'day':d,'year':year}

    return final


def win_rate_chart():
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = 80,
        mode = "gauge+number",
        gauge = {'axis': {'range': [None, 100]},
                'bar': {'color': "#0099ff"},
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 80}}))
        

    png =pio.to_image(fig)
    png_base64 = base64.b64encode(png).decode('ascii')
    return png_base64



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    app.run(debug=True)