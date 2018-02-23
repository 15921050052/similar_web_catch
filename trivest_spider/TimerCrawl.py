# -*- coding: utf-8 -*-

import datetime
import subprocess

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from StatusCache import clearAllStatus, getSpiderStatus
from GlobleConfig import getSpiderDetail, projectIdentify
from trivest_data.dal import SpiderMonitorDao

import logging

# 为了处理：No handlers could be found for logger “apscheduler.scheduler”
# logging.basicConfig(level=logging.DEBUG)  # 不设置，就不打印


logging.basicConfig()


def heartBeat():
    SpiderMonitorDao.projectHeatBeat(projectIdentify, heartBeatTimeSpace=60)
    pass


def startSpider(spiderName):
    heartBeatTimeSpace = 10*60
    if spiderName == 'weixin_source':
        heartBeatTimeSpace = 1*60*60
    elif spiderName == 'weixin_public_article':
        heartBeatTimeSpace = 3*60*60
    SpiderMonitorDao.spiderHeatBeat(projectIdentify, spiderName, getSpiderDetail(spiderName),
                                    heartBeatTimeSpace=heartBeatTimeSpace)
    print '执行', spiderName
    # return
    if getSpiderStatus(spiderName) != 'running':
        command = "scrapy crawl " + spiderName
        out_bytes = subprocess.check_output(command, shell=True)
        # print('end')
    else:
        print(spiderName + u' 还在抓取，跳过这轮start')


def diyicaijing_news():
    startSpider('diyicaijing_news')


def fenghuang_finance_bond_news():
    startSpider('fenghuang_finance_bond_news')


def fenghuang_finance_quoted_company():
    startSpider('fenghuang_finance_quoted_company')


def fenghuang_game_e_sports():
    startSpider('fenghuang_game_e_sports')


def fenghuang_game_hot_news():
    startSpider('fenghuang_game_hot_news')


def fenghuang_game_product_news():
    startSpider('fenghuang_game_product_news')


def fenghuang_tech_news():
    startSpider('fenghuang_tech_news')


def hexun_tech_main_news():
    startSpider('hexun_tech_main_news')


def hexun_tech_scroll_news():
    startSpider('hexun_tech_scroll_news')


def jiemian_news():
    startSpider('jiemian_news')


def jinrongjie_main_news():
    startSpider('jinrongjie_main_news')


def jinrongjie_quoted_company():
    startSpider('jinrongjie_quoted_company')


def kuaixun_quoted_company():
    startSpider('kuaixun_quoted_company')


def kuaixun_world_live():
    startSpider('kuaixun_world_live')


def sina_finance_main_news():
    startSpider('sina_finance_main_news')


def sina_finance_ssgs_scroll_news():
    startSpider('sina_finance_ssgs_scroll_news')


def sina_finance_stock_main_news():
    startSpider('sina_finance_stock_main_news')


def sina_tech_scroll_news():
    startSpider('sina_tech_scroll_news')


def sina_tech_scroll_news_2():
    startSpider('sina_tech_scroll_news_2')


def sohu_a_stock_hu_shen():
    startSpider('sohu_a_stock_hu_shen')


def sohu_tech_news():
    startSpider('sohu_tech_news')


def taoguba_core_post():
    startSpider('taoguba_core_post')


def taoguba_day_recommend():
    startSpider('taoguba_day_recommend')


def tengxun_finance_main_news():
    startSpider('tengxun_finance_main_news')


def tengxun_stock_main_news():
    startSpider('tengxun_stock_main_news')


def tengxun_stock_quoted_company():
    startSpider('tengxun_stock_quoted_company')


def tengxun_tech_scroll_news():
    startSpider('tengxun_tech_scroll_news')


def wangyi_finance_scroll_news():
    startSpider('wangyi_finance_scroll_news')


def wangyi_stock_news():
    startSpider('wangyi_stock_news')


def wangyi_tech_scroll_news():
    startSpider('wangyi_tech_scroll_news')


def weixin_public_article():
    startSpider('weixin_public_article')


def weixin_source():
    startSpider('weixin_source')


def xueqiu_tou_tiao():
    startSpider('xueqiu_tou_tiao')


def xueqiu_yan_bao():
    startSpider('xueqiu_yan_bao')


def xueqiu_hu_shen():
    startSpider('xueqiu_hu_shen')


def fenghuang_digital_news():
    startSpider('fenghuang_digital_news')


def ke_36_news():
    startSpider('ke_36_news')


def sina_digital_news():
    startSpider('sina_digital_news')


def tengxun_digital_news():
    startSpider('tengxun_digital_news')


def xinwenyan_tech_news():
    startSpider('xinwenyan_tech_news')


def kuwan_digital_news():
    startSpider('kuwan_digital_news')


def a5_chuangye_tech_news():
    startSpider('a5_chuangye_tech_news')


def citnews_tech_news():
    startSpider('citnews_tech_news')


def cn_qingnian_tech_news():
    startSpider('cn_qingnian_tech_news')


def cn_touzi_tech_news():
    startSpider('cn_touzi_tech_news')


def cn_wang_tech_news():
    startSpider('cn_wang_tech_news')


def cn_wang_tech_scroll_news():
    startSpider('cn_wang_tech_scroll_news')


def cnbeta_tech_news():
    startSpider('cnbeta_tech_news')


def renmin_tech_news():
    startSpider('renmin_tech_news')


def sina_tags():
    startSpider('sina_tags')


def tom_tech_news():
    startSpider('tom_tech_news')


def xinhua_tech_news():
    startSpider('xinhua_tech_news')


def zhonghua_tech_scroll_news():
    startSpider('zhonghua_tech_scroll_news')


def techweb_yejie_news():
    startSpider('techweb_yejie_news')


def kuaikeji_all_news():
    startSpider('kuaikeji_all_news')


def itbear_yejie_news():
    startSpider('itbear_yejie_news')


def cn_digital_tech_news():
    startSpider('cn_digital_tech_news')


def itbear_digital_news():
    startSpider('itbear_digital_news')


def cn21tech_it_news():
    startSpider('cn21tech_it_news')


def cn21tech_tech_news():
    startSpider('cn21tech_tech_news')


def cn21tech_digital_news():
    startSpider('cn21tech_digital_news')


def nanfang_it_news():
    startSpider('nanfang_it_news')


def qingdao_digital_news():
    startSpider('qingdao_digital_news')

def leifeng_yejie_news():
    startSpider('leifeng_yejie_news')


def leifeng_ai_news():
    startSpider('leifeng_ai_news')


def leifeng_ai_juejin_news():
    startSpider('leifeng_ai_juejin_news')

def leifeng_driver_news():
    startSpider('leifeng_driver_news')

def leifeng_ar_news():
    startSpider('leifeng_ar_news')

def leifeng_robot_news():
    startSpider('leifeng_robot_news')


def jiqiren_yejie_news():
    startSpider('jiqiren_yejie_news')

def it_times_yejie_news():
    startSpider('it_times_yejie_news')


def zol_yejie_news():
    startSpider('zol_yejie_news')

def start():
    # 当项目重新启动，清除所有状态
    clearAllStatus()

    def add_job(func, timeSpace, delaySeconds=0):
        # 先马上开始执行
        # scheduler.add_job(func, 'date',misfire_grace_time=120) #misfire_grace_time=120,
        # 后再抓取之后的某个时间段开始间隔执行
        # next_run_time:设置下一轮开始时间
        # max_instances：如 1：表示当前方法正在执行还没有执行完，则不能再次启动这个方法，需等待完成，同理其他数
        # misfire_grace_time:120代表2分钟，当一个任务missing之后，在两分钟内会被重试
        scheduler.add_job(func, 'interval', seconds=timeSpace, misfire_grace_time=120,
                          next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=delaySeconds),
                          start_date=datetime.datetime.now() + datetime.timedelta(seconds=timeSpace), max_instances=1)

    timeSpace = 10 * 60
    sina_tag_timeSpace = 10 * 60 * 6 * 3 # 新浪 Tag3小时走一次
    wx_timeSpace = 10 * 60 * 6 * 3  # 微信文章 3个小时走一次
    wx_source_timeSpace = 60 * 60  # 微信源 1个小时走一次
    heartTime = 1 * 60  # 心跳跳动时间间隔
    # executors不设置，就会出现只能默认有5个线程
    executors = {
        'default': ThreadPoolExecutor(53+19),  # 根据任务数来定，每增加一个任务，就需要增加这个数量
        'processpool': ProcessPoolExecutor(53+19)
    }
    scheduler = BlockingScheduler(daemonic=False, executors=executors)
    # 心跳
    add_job(heartBeat, heartTime)

    add_job(a5_chuangye_tech_news, timeSpace)
    add_job(citnews_tech_news, timeSpace)
    add_job(cn_qingnian_tech_news, timeSpace)
    add_job(cn_touzi_tech_news, timeSpace)
    add_job(cn_wang_tech_news, timeSpace)
    add_job(cn_wang_tech_scroll_news, timeSpace)
    add_job(cnbeta_tech_news, timeSpace)
    add_job(diyicaijing_news, timeSpace)
    add_job(fenghuang_digital_news, timeSpace)
    add_job(fenghuang_finance_bond_news, timeSpace)
    add_job(fenghuang_finance_quoted_company, timeSpace)
    add_job(fenghuang_game_e_sports, timeSpace)
    add_job(fenghuang_game_hot_news, timeSpace)
    add_job(fenghuang_game_product_news, timeSpace)
    add_job(fenghuang_tech_news, timeSpace)
    add_job(hexun_tech_main_news, timeSpace)
    add_job(hexun_tech_scroll_news, timeSpace)
    add_job(jiemian_news, timeSpace)
    add_job(jinrongjie_main_news, timeSpace)
    add_job(jinrongjie_quoted_company, timeSpace)
    add_job(ke_36_news, timeSpace)
    add_job(kuaixun_quoted_company, timeSpace)
    add_job(kuaixun_world_live, timeSpace)
    add_job(kuwan_digital_news, timeSpace)
    add_job(renmin_tech_news, timeSpace)
    add_job(sina_digital_news, timeSpace)
    add_job(sina_finance_main_news, timeSpace)
    add_job(sina_finance_ssgs_scroll_news, timeSpace)
    add_job(sina_finance_stock_main_news, timeSpace)
    add_job(sina_tags, sina_tag_timeSpace)
    add_job(sina_tech_scroll_news, timeSpace)
    add_job(sina_tech_scroll_news_2, timeSpace)
    add_job(sohu_a_stock_hu_shen, timeSpace)
    add_job(sohu_tech_news, timeSpace)
    add_job(taoguba_core_post, timeSpace)
    add_job(taoguba_day_recommend, timeSpace)
    add_job(tengxun_digital_news, timeSpace)
    add_job(tengxun_finance_main_news, timeSpace)
    add_job(tengxun_stock_main_news, timeSpace)
    add_job(tengxun_stock_quoted_company, timeSpace)
    add_job(tengxun_tech_scroll_news, timeSpace)
    add_job(tom_tech_news, timeSpace)
    add_job(wangyi_finance_scroll_news, timeSpace)
    add_job(wangyi_stock_news, timeSpace)
    add_job(wangyi_tech_scroll_news, timeSpace)
    add_job(weixin_public_article, wx_timeSpace, delaySeconds=120)
    add_job(weixin_source, wx_source_timeSpace)
    add_job(xinhua_tech_news, timeSpace)
    add_job(xinwenyan_tech_news, timeSpace)
    add_job(xueqiu_hu_shen, timeSpace)
    add_job(xueqiu_tou_tiao, timeSpace)
    add_job(xueqiu_yan_bao, timeSpace)
    add_job(zhonghua_tech_scroll_news, timeSpace)

    add_job(techweb_yejie_news, timeSpace)
    add_job(kuaikeji_all_news, timeSpace)
    add_job(itbear_digital_news, timeSpace)
    add_job(itbear_yejie_news, timeSpace)
    add_job(cn_digital_tech_news, timeSpace)
    add_job(cn21tech_it_news, timeSpace)
    add_job(cn21tech_tech_news, timeSpace)
    add_job(cn21tech_digital_news, timeSpace)
    add_job(nanfang_it_news, timeSpace)
    add_job(qingdao_digital_news, timeSpace)
    add_job(leifeng_yejie_news, timeSpace)
    add_job(leifeng_ai_news, timeSpace)
    add_job(leifeng_ai_juejin_news, timeSpace)
    add_job(leifeng_driver_news, timeSpace)
    add_job(leifeng_ar_news, timeSpace)
    add_job(leifeng_robot_news, timeSpace)
    add_job(jiqiren_yejie_news, timeSpace)
    add_job(it_times_yejie_news, timeSpace)
    add_job(zol_yejie_news, timeSpace)


    scheduler.start()


if __name__ == '__main__':
    start()
