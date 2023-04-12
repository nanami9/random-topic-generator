from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import requests
import json
import aiohttp
import asyncio

@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)

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

async def send_async_http_request(url, headers, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                return await response.text()
            else:
                print('Error:', response.status)
                return None
           
@app.route('/api/gpt2', methods=['POST'])
def gpt2():
    # 获取请求体参数
    data = request.get_json()
    msg = data["message"]
    setup = data["setup"]
    url = 'http://13.114.207.202:5000/api/gpt'
    headers = {'Content-Type': 'application/json'}
    data = {'message': msg,
            'setup': setup
            }
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    reply = loop.run_until_complete(send_async_http_request(url, headers=headers, data=json.dumps(data)))
    
    return make_succ_response(reply)
