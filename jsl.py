# coding:utf8
# 获取集思路的分级数据
# 测试环境：ubuntu15.04 python3.4
# 使用方法:
# 初始化
# jsl = JSL()
# 初始化时传入利率范围和最小交易量
# jsl = JSL(range=[3, 3.2], minvolume=5000, ignore=['150209'])
# 设置分级A的利率范围
# jsl.range = [4]
# 设置之后分级A的最小交易量
# jsl.minvolume = 1000
# 设置分级A的忽略列表，默认忽略深成指A
# jsl.ignore = ['150209']
# 获取数据
# jsl.getFunda()
import time
from pprint import pprint
import requests
import json


class JSL(object):
    '''
    抓取集思路的分级A数据
    '''

    # 分级A的接口
    __funda_url = 'http://www.jisilu.cn/data/sfnew/funda_list/?___t={ctime:d}'

    # 分级A数据
    # 返回的字典格式
    # { 150020:
    # {'abrate': '5:5',
    #  'calc_info': None,
    #  'coupon_descr': '+3.0%',
    #  'coupon_descr_s': '+3.0%',
    #  'fund_descr': '每年第一个工作日定折，无下折，A不参与上折，净值<1元无定折',
    #  'funda_amount': 178823,
    #  'funda_amount_increase': '0',
    #  'funda_amount_increase_rt': '0.00%',
    #  'funda_base_est_dis_rt': '2.27%',
    #  'funda_base_est_dis_rt_t1': '2.27%',
    #  'funda_base_est_dis_rt_t2': '-0.34%',
    #  'funda_base_est_dis_rt_tip': '',
    #  'funda_base_fund_id': '163109',
    #  'funda_coupon': '5.75',
    #  'funda_coupon_next': '4.75',
    #  'funda_current_price': '0.783',
    #  'funda_discount_rt': '24.75%',
    #  'funda_id': '150022',
    #  'funda_increase_rt': '0.00%',
    #  'funda_index_id': '399001',
    #  'funda_index_increase_rt': '0.00%',
    #  'funda_index_name': '深证成指',
    #  'funda_left_year': '永续',
    #  'funda_lower_recalc_rt': '1.82%',
    #  'funda_name': '深成指A',
    #  'funda_nav_dt': '2015-09-14',
    #  'funda_profit_rt': '7.74%',
    #  'funda_profit_rt_next': '6.424%',
    #  'funda_value': '1.0405',
    #  'funda_volume': '0.00',
    #  'fundb_upper_recalc_rt': '244.35%',
    #  'fundb_upper_recalc_rt_info': '深成指A不参与上折',
    #  'last_time': '09:18:22',
    #  'left_recalc_year': '0.30411',
    #  'lower_recalc_profit_rt': '-',
    #  'next_recalc_dt': '<span style="font-style:italic">2016-01-04</span>',
    #  'owned': 0,
    #  'status_cd': 'N'}
    # }
    __funda = None

    # 设置利率范围，不设置则取全部
    # 例如: [3, 3.2]
    __range = []

    @property
    def range(self):
        return self.__range

    @range.setter
    def range(self, valuelist):
        # 转为带一个小数点的字符串列表，方便比较
        self.__range = ['%.1f' % x for x in valuelist]

    # 设置最小成交额（单位：万）
    __minvolume = 0

    @property
    def minvolume(self):
        return self.__minvolume

    @minvolume.setter
    def minvolume(self, value):
        self.__minvolume = value

    # 设置忽略的分级基金列表,默认忽略深成指
    __ignore = ['150022']

    @property
    def ignore(self):
        return self.__ignore

    @ignore.setter
    def ignore(self, ignorelist):
        self.__ignore = ignorelist

    def __init__(self, range=[], minvolume=0, ignore=[]):
        self.ignore = ignore if len(ignore) else self.__ignore
        self.range = range
        self.minvolume = minvolume

    @staticmethod
    def formatjson(fundajson):
        "格式化集思录返回的json数据,以字典形式保存"
        d = {}
        for row in fundajson['rows']:
            id = row['id']
            cell = row['cell']
            d[id] = cell
        return d

    def getFunda(self):
        '以字典形式返回分级A数据'
        # 添加当前的ctime
        self.__funda_url = self.__funda_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__funda_url)
        # 获取返回的json字符串
        fundajson = json.loads(rep.text)
        # 格式化返回的json字符串
        alladata = self.formatjson(fundajson)
        # 检查是否设置过滤条件
        if len(self.__range) or self.__minvolume or len(self.__range):
            # 过滤掉不符合条件的A
            for k in list(alladata):
                cell = alladata[k]
                # 忽略非指定利率 and 忽略小于最小成交量 and 忽略忽略列表中的分级
                if (not cell['coupon_descr_s'][1:4] in ''.join(self.__range) if len(self.__range) else False) or \
                            float(cell['funda_volume']) < self.__minvolume or \
                            k in self.__ignore:
                    alladata.pop(k)
        self.__funda = alladata
        return self.__funda


if __name__ == '__main__':
    funda = JSL()
    # 设置利率范围
    funda.range = [3]
    # 设置最小交易量
    funda.minvolume = 15000
    pprint(funda.getFunda())
