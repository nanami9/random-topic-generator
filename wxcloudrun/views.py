from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import requests
import json

@app.route('/api/gpt', methods=['POST'])
def gpt():
    # 获取请求体参数
    data = request.get_json()
    msg = data["message"]
    setup = data["setup"]
    url = 'http://13.114.207.202:5000/api/gpt'
    headers = {'Content-Type': 'application/json'}
    data = {'message': msg,
            'setup': setup
            }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        reply = response.text
    else:
        print('Error:', response.status_code)
 
    return make_succ_response(reply)

@app.route('/api/gpt2', methods=['POST'])
def gpt2():
    data = request.get_json()
    msg = data["message"]
    setup = data["setup"]
    url = 'http://13.114.207.202:5000/api/gpt2'
    headers = {'Content-Type': 'application/json'}
    data = {'message': msg,
            'setup': setup
            }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        task_id = response_dict['task_id']
    else:
        print('Error:', response.status_code)
        
    return make_succ_response(task_id)
    
    
    
