from flask import Request


def get_data_from_request(rqst: Request):
    '''
    args:
        rqst (Flask.Request) contains the request variable
    '''
    data = {}
    if rqst.method == 'POST':
        data = rqst.get_json()
    else:
        data = rqst.args.to_dict()
    
    verify_data(data)
    return data
    
def verify_data(data):
    if not isinstance(data,dict):
        raise Exception('Verify the input parameters')
    
    if data.get('adaccount_id', None) == None:
        raise Exception('Verify adaccount_id')
    
    if data.get('start_date') == None or data.get('end_date') == None:
        raise Exception('Verify date range')
    
    if data.get('phase_name') == None:
        raise Exception('Verify phase name')
