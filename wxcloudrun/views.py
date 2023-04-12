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

@app.route('/api/gpt2/status', methods=['POST'])
def gpt2_status():
    # 获取发送来的id
    data = request.get_json()
    task_id = data["task_id"]
    api_endpoint = 'http://13.114.207.202:5000/api/gpt2/status'
    # 构造请求URL
    url = f'{api_endpoint}?task_id={task_id}'
    # 发送GET请求并获取响应
    response = requests.get(url)
    # 解析JSON响应
    if response.ok:
        response_data = response.json()
        if 'error' in response_data:
            make_succ_response("failed")
        else:
            task_result = response_data
            make_succ_response(task_result)
    else:
        make_succ_response("Failed to query task status.")
    
    
    
