import requests
import threading as thrd

USER_EMAIL = 'subhro.acharjee@blkbox.ai'
USER_PASSWORD = 'password@123'

API_BASE_URL = 'https://server.blkbox.ai/api/v0.1/facebook'

class Communication:
    '''
    This class will handle the communication with backend.
    '''

    def __init__(self, adaccount_id, start_date, end_date) -> None:
        self.token  = self.get_token()
        self.adaccount_id = adaccount_id
        self.start_date = start_date
        self.end_date = end_date
        self.response_arr = [None, None,None,None, None,None]
        pass

    def get_token(self):
        '''
        Returns:
            string: access_token from backend server.
        '''
        login_data = {
            'email': USER_EMAIL,
            'password': USER_PASSWORD
        }

        uri = f'{API_BASE_URL}/user/login'
        response = requests.post(uri, login_data)
        print(response.ok)
        if (response.ok):
            data = response.json()
            if (data.get('status') == 'success'):
                return data.get('token').get('token')
        
        raise Exception('Something went wrong!')
    
    def make_requests_data(self):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        creatives_uri_phase1  = f'{API_BASE_URL}/box/creativeTesting/executiveReport/creatives?adaccount_id={self.adaccount_id}&start_date={self.start_date}&end_date={self.end_date}&phase_name=PHASE_ONE'
        metric_uri_phase1 = f'{API_BASE_URL}/box/creativeTesting/executiveReport/metrics?adaccount_id={self.adaccount_id}&start_date={self.start_date}&end_date={self.end_date}&phase_name=PHASE_ONE'
        graph_uri_phase1  = f'{API_BASE_URL}/box/creativeTesting/executiveReport/graphs?adaccount_id={self.adaccount_id}&start_date={self.start_date}&end_date={self.end_date}&phase_name=PHASE_ONE'
        creatives_uri_phase2  = f'{API_BASE_URL}/box/creativeTesting/executiveReport/creatives?adaccount_id={self.adaccount_id}&start_date={self.start_date}&end_date={self.end_date}&phase_name=PHASE_TWO'
        metric_uri_phase2 = f'{API_BASE_URL}/box/creativeTesting/executiveReport/metrics?adaccount_id={self.adaccount_id}&start_date={self.start_date}&end_date={self.end_date}&phase_name=PHASE_TWO'
        graph_uri_phase2  = f'{API_BASE_URL}/box/creativeTesting/executiveReport/graphs?adaccount_id={self.adaccount_id}&start_date={self.start_date}&end_date={self.end_date}&phase_name=PHASE_TWO'
        return header, (metric_uri_phase1 , graph_uri_phase1, creatives_uri_phase1,metric_uri_phase2 , graph_uri_phase2, creatives_uri_phase2)
    
    @staticmethod
    def get_data_from_server(header, uri, arr:list, index):
        print(index)
        '''
        calls the metrics api to get all the metrics data.
        '''
        try:
            res = requests.get(uri[index], headers=header)
            if res.ok:
                if res.json().get('status') == 'success':
                    arr[index] = res.json().get('data')
        except Exception as e:
            print(e)
            pass
        pass

    def make_async_requests(self):
        '''
        Thread handler
        '''
        header, uris = self.make_requests_data()
        thread_arr = []
        print(uris)
        for i,uri in enumerate(uris):
            print(i)
            print(uri)
            th = thrd.Thread(target=Communication.get_data_from_server, args=(header, uris, self.response_arr, i), daemon=True, name= f'Async request {i}')
            th.start()
            thread_arr.append(th)
            print(self.response_arr)
        
        for thread in thread_arr:
            thread.join()
        
        return self.response_arr


if __name__ == '__main__':
    com = Communication('act_2747337658924217', '2022-05-01', '2022-05-20')
    data_arr = com.make_async_requests()
    #print(data_arr)
    

