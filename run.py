import json
from locale import YESEXPR
from flask import Flask, jsonify, make_response, render_template
import pdfkit
import datetime
from quickchart import QuickChart, QuickChartFunction



app = Flask(__name__)
data = {}
#Read Data from Json
with open('Data/Time series graph.json', 'r') as f1:
  data = json.load(f1)

with open('Data/Metrics.json', 'r') as f2:
  metrics = json.load(f2)

with open('Data/Top Creative Insights.json', 'r') as f3:
  top_creative = json.load(f3)


@app.route('/',methods=['GET','POST'])
def index():

    p_data,label=process_data(data)

    date=index_date(metrics['data']['date_range'])
    print(date)
    img_list=[]
    for i in p_data:
        img_list.append(chartjs(p_data[i],label['label'],i))

    rendered = render_template('index.html',index_date=date,img=img_list,metrics=metrics,top_creative=top_creative)
    
    options = {
        
    'page-size': 'A4',
    'margin-right': '0.20in',
    'margin-bottom': '0.20in',
    'margin-left': '0.20in',
    'margin-top':'0.20in',
    }


    pdf=pdfkit.from_string(rendered,options=options)

    response = make_response(pdf)
    response.headers['Content-type']='application/pdf'
    response.headers['Content-Disposition']='inline; filename=Blkbox-Report.pdf'

    return response



def process_data(data):
    keys=data['data']['filter_metrics']
    process_data=data['data']['time_series_graph']
    label=dict()
    temp_dict=dict()
    for i in keys:
        label['label']=[]
        temp_dict[i]=[]
        for d in process_data:
            if i in d.keys():
                temp_dict[i].append(d[i])
                label['label'].append(date_time(d['label']))
                #label['label'].append(urllib.parse.quote("'" + date_time(d['label']) + "'"))
    return temp_dict,label



def chartjs(data,label,key):
    key=key.upper()
    #label = ','.join([str(a) for a in label])
    #data = ','.join([str(a) for a in data])

    qc = QuickChart()
    qc.width = 800
    qc.height = 480
    qc.device_pixel_ratio = 3.0
    qc.version=3
    qc.scheme='http'
    qc.host='localhost:3400'
    
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


    #chart="http://localhost:3400/chart?v=3&c={ type: 'line', data: { labels: ["+label+"], datasets: [ { label: '"+key+"',backgroundColor: 'rgb(204,229,255)', borderColor: 'rgb(0,191,255)', data: ["+data+"], fill: false, borderWidth:1,pointRadius:2}, ], }, options: { scales: { x: {grid: {display: false}}}, plugins: { legend: {position: 'top',align: 'start',labels: { boxWidth: 0,} }, } } }"
    
    
    #chart="https://quickchart.io/chart?v=3&c=%7B%0A%20%20type%3A%20%27line%27%2C%0A%20%20data%3A%20%7B%0A%20%20%20%20labels%3A%20%5B%27January%27%2C%20%27February%27%2C%20%27March%27%2C%20%27April%27%2C%20%27May%27%2C%20%27June%27%2C%20%27July%27%5D%2C%0A%20%20%20%20datasets%3A%20%5B%0A%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20label%3A%20%27My%20First%20dataset%27%2C%0A%20%20%20%20%20%20%20%20backgroundColor%3A%20%27rgb(255%2C%2099%2C%20132)%27%2C%0A%20%20%20%20%20%20%20%20borderColor%3A%20%27rgb(255%2C%2099%2C%20132)%27%2C%0A%20%20%20%20%20%20%20%20data%3A%20%5B93%2C%2029%2C%2017%2C%208%2C%2073%2C%2098%2C%2040%5D%2C%0A%20%20%20%20%20%20%20%20fill%3Atrue%2C%0A%20%20%20%20%20%20%20%20backgroundColor%3A%20getGradientFillHelper(%27vertical%27%2C%20%5B%27%236287a2%27%2C%20%27%23e9ecf4%27%5D)%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%5D%2C%0A%20%20%7D%2C%0A%20%20options%3A%20%7B%0A%20%20%20%20title%3A%20%7B%0A%20%20%20%20%20%20display%3A%20true%2C%0A%20%20%20%20%20%20text%3A%20%27Chart.js%20Line%20Chart%27%2C%0A%20%20%20%20%7D%2C%0A%20%20%7D%2C%0A%7D%0A"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)