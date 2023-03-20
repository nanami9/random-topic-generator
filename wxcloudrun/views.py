from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import clueai
import openai

openai.api_key = "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"

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
    # 测试小元模型1
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
    setup = ""
    messages = [
                    {"role": "system", "content": setup},
                    {"role": "user", "content": msg},
                    {"role": "assistant", "content": ""},
                ]

    # gpt-3.5-turbo
    prediction = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        )
    reply = prediction['choices'][0]['message']['content']
    
    return make_succ_response(reply)

