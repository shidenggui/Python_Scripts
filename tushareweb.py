# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import tushare

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def intro():
    intro_info = u'使用说明：调用tushare获取指定数据  返回类型为JSON 调用格式如下: /tushare/?func=函数名&参数1=值1&参数2=值2'
    return intro_info


@app.route('/tushare')
def tushareapi():
    params = request.args.copy();
    func = params.pop('func')
    tusharefunc = getattr(tushare, func)
    params = {k: str(v) for k, v in params.items()}
    try:
        return tusharefunc(**params).to_json()
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run()
