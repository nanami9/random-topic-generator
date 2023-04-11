from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import clueai
import requests
import json
import asyncio
import aiohttp

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

@app.route('/api/hello', methods=['POST'])
def hello():
    # 获取请求体参数
    data = request.get_json()
    # 测试小元模型
    cl = clueai.Client('0c78ipY1FPR7vuB73L0f8101001111010', check_api_key=True)
    prediction = cl.generate(
        model_name='ChatYuan-large',
        prompt = data["message"]
        )
    reply = prediction.generations[0].text

    # 返回结果
    return make_succ_response(reply)

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
