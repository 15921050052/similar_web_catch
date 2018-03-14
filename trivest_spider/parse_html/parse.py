# -*- coding: utf-8 -*-
import json
import os

import datetime
from pyexcel_xls import save_data
from scrapy import Selector

from trivest_data.dal.trivest_spider import SimilarSrc


def get_all_file_path(path):
    path_list = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        # print ''.join(os.path.splitext(file))
        file_name = os.path.splitext(file)[0]
        file_name_all = ''.join(os.path.splitext(file))
        if os.path.isdir(file_path):
            get_all_file_path(file_path)
        else:
            path_list.append([file_path, file_name, file_name_all])
    return path_list


def i_e(condition, yes, no):
    if condition:
        return yes
    else:
        return no


def check(spiderName):
    # 判断当前文件是否存在，不存在，则新建
    fileName = spiderName + '.json'
    filePath = os.path.join(os.path.dirname(__file__) + '/status/')

    if not os.path.exists(filePath):
        os.mkdir(filePath)

    return filePath + fileName


def getLoopCache():
    f = None
    loop_cache = {
        u'last': {
            u'status': u'',
            u'dir': u'',
            u'time_start': u'',
            u'time_complete': u''
        },
        u'new': {
            u'status': u'',
            u'dir': u'',
            u'time_start': u'',
            u'time_complete': u''
        }
    }
    try:
        with open(u'cache/loop_cache.json', u'r') as f:
            loop_cache = json.load(f)
    except Exception, e:
        print str(e)
    finally:
        f and f.close()
    return loop_cache


def parse_before(file_path, hash_code):
    load_f = None
    result = None
    try:
        with open(file_path, 'r') as load_f:
            result = parse(load_f.read(), hash_code)
    finally:
        load_f and load_f.close()
    return result


def l_i(condition, list, yes_index, no):
    if condition:
        return list[yes_index]
    else:
        return no


def save_xls_file(sheet_list, save_dir):
    from collections import OrderedDict
    data = OrderedDict()

    for sheet in sheet_list:
        sheet_name = sheet[u'sheet_name']
        rows = sheet[u'rows']

        # 添加sheet表
        data.update({sheet_name: rows})

    # 保存成xls文件
    save_data(u'result/%s.xls' % save_dir, data)


def parse(html, hash_code):
    response = Selector(text=html)
    info = response.xpath(
        u'//div[@class="websiteHeader-companyDescriptionWrapper"]/p[@itemprop="description"]/text()').extract_first(u'')

    over_view_time = response.xpath(
        u'//div[@class="websiteHeader-date"]/span[@class="websiteHeader-dateFull"]/text()').extract_first(u'')

    # 第一部分
    rank_list = u''.join(
        response.xpath(u'//div[@class="websiteRanks-valueContainer js-websiteRanksValue"]/text()').extract()).split()

    global_rank = l_i(len(rank_list), rank_list, 0, u'')
    country_rank = l_i(len(rank_list) > 1, rank_list, 1, u'')
    category_rank = l_i(len(rank_list) > 2, rank_list, 2, u'')

    # 第二部分 https://www.similarweb.com/website/bitcoin.co.id
    second_part = response.xpath(u'//span[@class="engagementInfo-valueNumber js-countValue"]/text()').extract()

    trf_total_visits = l_i(len(second_part), second_part, 0, u'')
    trf_avg_visit_duration = l_i(len(second_part) > 1, second_part, 1, u'')
    trf_pages_per_visit = l_i(len(second_part) > 2, second_part, 2, u'')
    trf_bounce_rate = l_i(len(second_part) > 3, second_part, 3, u'')

    trf_total_visits_change = response.xpath(
        u'//span[@class="engagementInfo-value engagementInfo-value--large u-text-ellipsis"]'
        u'//span[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')

    # 第三部分
    trf_country_1 = u''
    trf_country_1_value = u''
    trf_country_1_change = u''

    trf_country_2 = u''
    trf_country_2_value = u''
    trf_country_2_change = u''

    trf_country_3 = u''
    trf_country_3_value = u''
    trf_country_3_change = u''

    trf_country_4 = u''
    trf_country_4_value = u''
    trf_country_4_change = u''

    trf_country_5 = u''
    trf_country_5_value = u''
    trf_country_5_change = u''

    trf_country_part = response.xpath(u'//div[contains(@class, "accordion-group")]')
    trf_country_index = 0
    for trf_country in trf_country_part:
        trf_country_index += 1
        trf_country_name = trf_country.xpath(u'.//*[contains(@class, "country-name")]/text()').extract_first(u'')
        trf_country_value = trf_country.xpath(
            u'.//*[@class="traffic-share-valueNumber js-countValue"]/text()').extract_first(u'')
        trf_country_change = trf_country.xpath(u'.//*[@class="websitePage-relativeChangeNumber"]/text()').extract_first(
            u'')
        if trf_country_index == 1:
            trf_country_1 = trf_country_name
            trf_country_1_value = trf_country_value
            trf_country_1_change = trf_country_change
        elif trf_country_index == 2:
            trf_country_2 = trf_country_name
            trf_country_2_value = trf_country_value
            trf_country_2_change = trf_country_change
        elif trf_country_index == 3:
            trf_country_3 = trf_country_name
            trf_country_3_value = trf_country_value
            trf_country_3_change = trf_country_change
        elif trf_country_index == 4:
            trf_country_4 = trf_country_name
            trf_country_4_value = trf_country_value
            trf_country_4_change = trf_country_change
        elif trf_country_index == 5:
            trf_country_5 = trf_country_name
            trf_country_5_value = trf_country_value
            trf_country_5_change = trf_country_change
    print hash_code
    print global_rank, country_rank, category_rank, trf_total_visits, trf_total_visits_change, trf_avg_visit_duration, trf_pages_per_visit, trf_bounce_rate

    print trf_country_1, trf_country_2, trf_country_3, trf_country_4, trf_country_5
    print trf_country_1_value, trf_country_2_value, trf_country_3_value, trf_country_4_value, trf_country_5_value
    print trf_country_1_change, trf_country_2_change, trf_country_3_change, trf_country_4_change, trf_country_5_change

    # 第四部分 Traffic Sources
    trf_source_direct = u''
    trf_source_referrals = u''
    trf_source_search = u''
    trf_source_social = u''
    trf_source_mail = u''
    trf_source_display = u''

    trf_source_part = response.xpath(u'//*[contains(@class, "trafficSourcesChart-item")]')
    trf_source_index = 0
    for trf_source in trf_source_part:
        trf_source_index += 1
        trf_source_value = trf_source.xpath(u'.//*[@class="trafficSourcesChart-value"]/text()').extract_first(u'')
        if trf_source_index == 1:
            trf_source_direct = trf_source_value
        elif trf_source_index == 2:
            trf_source_referrals = trf_source_value
        elif trf_source_index == 3:
            trf_source_search = trf_source_value
        elif trf_source_index == 4:
            trf_source_social = trf_source_value
        elif trf_source_index == 5:
            trf_source_mail = trf_source_value
        elif trf_source_index == 6:
            trf_source_display = trf_source_value

    print trf_source_direct, trf_source_referrals, trf_source_search, trf_source_social, trf_source_mail, trf_source_display

    # 第五部分 Referrals
    ref_of_trf_percent = response.xpath(u'//span[@class="subheading-value referrals"]/text()').extract_first(u'')

    ref_top_site_1 = u''
    ref_top_site_1_value = u''
    ref_top_site_1_change = u''

    ref_top_site_2 = u''
    ref_top_site_2_value = u''
    ref_top_site_2_change = u''

    ref_top_site_3 = u''
    ref_top_site_3_value = u''
    ref_top_site_3_change = u''

    ref_top_site_4 = u''
    ref_top_site_4_value = u''
    ref_top_site_4_change = u''

    ref_top_site_5 = u''
    ref_top_site_5_value = u''
    ref_top_site_5_change = u''

    ref_top_site_part = response.xpath(u'//div[@class="referralsSites referring"]//ul[@class="websitePage-list"]/li')
    ref_top_site_index = 0
    for ref_top_site in ref_top_site_part:
        ref_top_site_index += 1
        ref_top_site_name = ref_top_site.xpath(u'.//*[@class="websitePage-listItemTitle"]/a/text()').extract_first(u'')
        ref_top_site_value = ref_top_site.xpath(u'.//*[@class="websitePage-trafficShare"]/text()').extract_first(u'')
        ref_top_site_change = ref_top_site.xpath(
            u'.//*[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')
        if ref_top_site_index == 1:
            ref_top_site_1 = ref_top_site_name
            ref_top_site_1_value = ref_top_site_value
            ref_top_site_1_change = ref_top_site_change
        elif ref_top_site_index == 2:
            ref_top_site_2 = ref_top_site_name
            ref_top_site_2_value = ref_top_site_value
            ref_top_site_2_change = ref_top_site_change
        elif ref_top_site_index == 3:
            ref_top_site_3 = ref_top_site_name
            ref_top_site_3_value = ref_top_site_value
            ref_top_site_3_change = ref_top_site_change
        elif ref_top_site_index == 4:
            ref_top_site_4 = ref_top_site_name
            ref_top_site_4_value = ref_top_site_value
            ref_top_site_4_change = ref_top_site_change
        elif ref_top_site_index == 5:
            ref_top_site_5 = ref_top_site_name
            ref_top_site_5_value = ref_top_site_value
            ref_top_site_5_change = ref_top_site_change
    print u'第五部分 Referrals'
    print ref_of_trf_percent
    print ref_top_site_1, ref_top_site_2, ref_top_site_3, ref_top_site_4, ref_top_site_5
    print ref_top_site_1_value, ref_top_site_2_value, ref_top_site_3_value, ref_top_site_4_value, ref_top_site_5_value
    print ref_top_site_1_change, ref_top_site_2_change, ref_top_site_3_change, ref_top_site_4_change, ref_top_site_5_change

    ref_des_site_1 = u''
    ref_des_site_1_value = u''
    ref_des_site_1_change = u''

    ref_des_site_2 = u''
    ref_des_site_2_value = u''
    ref_des_site_2_change = u''

    ref_des_site_3 = u''
    ref_des_site_3_value = u''
    ref_des_site_3_change = u''

    ref_des_site_4 = u''
    ref_des_site_4_value = u''
    ref_des_site_4_change = u''

    ref_des_site_5 = u''
    ref_des_site_5_value = u''
    ref_des_site_5_change = u''

    ref_des_site_part = response.xpath(u'//div[@class="referralsSites destination"]//ul[@class="websitePage-list"]/li')
    ref_des_site_index = 0
    for ref_des_site in ref_des_site_part:
        ref_des_site_index += 1
        ref_des_site_name = ref_des_site.xpath(u'.//*[@class="websitePage-listItemTitle"]/a/text()').extract_first(u'')
        ref_des_site_value = ref_des_site.xpath(u'.//*[@class="websitePage-trafficShare"]/text()').extract_first(u'')
        ref_des_site_change = ref_des_site.xpath(
            u'.//*[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')
        if ref_des_site_index == 1:
            ref_des_site_1 = ref_des_site_name
            ref_des_site_1_value = ref_des_site_value
            ref_des_site_1_change = ref_des_site_change
        elif ref_des_site_index == 2:
            ref_des_site_2 = ref_des_site_name
            ref_des_site_2_value = ref_des_site_value
            ref_des_site_2_change = ref_des_site_change
        elif ref_des_site_index == 3:
            ref_des_site_3 = ref_des_site_name
            ref_des_site_3_value = ref_des_site_value
            ref_des_site_3_change = ref_des_site_change
        elif ref_des_site_index == 4:
            ref_des_site_4 = ref_des_site_name
            ref_des_site_4_value = ref_des_site_value
            ref_des_site_4_change = ref_des_site_change
        elif ref_des_site_index == 5:
            ref_des_site_5 = ref_des_site_name
            ref_des_site_5_value = ref_des_site_value
            ref_des_site_5_change = ref_des_site_change
    print u'第五部分 Referrals des'
    print ref_des_site_1, ref_des_site_2, ref_des_site_3, ref_des_site_4, ref_des_site_5
    print ref_des_site_1_value, ref_des_site_2_value, ref_des_site_3_value, ref_des_site_4_value, ref_des_site_5_value
    print ref_des_site_1_change, ref_des_site_2_change, ref_des_site_3_change, ref_des_site_4_change, ref_des_site_5_change

    # 第六部分 Search
    sch_of_trf_percent = response.xpath(u'//span[@class="subheading-value searchText"]/text()').extract_first(u'')

    sch_percent = response.xpath(u'//span[@class="searchPie-number"]/text()').extract()
    sch_organic_percent = l_i(len(sch_percent), sch_percent, 0, u'')
    sch_paid_percent = l_i(len(sch_percent) > 1, sch_percent, 1, u'')

    sch_organic_keyword_1 = u''
    sch_organic_keyword_1_value = u''
    sch_organic_keyword_1_change = u''

    sch_organic_keyword_2 = u''
    sch_organic_keyword_2_value = u''
    sch_organic_keyword_2_change = u''

    sch_organic_keyword_3 = u''
    sch_organic_keyword_3_value = u''
    sch_organic_keyword_3_change = u''

    sch_organic_keyword_4 = u''
    sch_organic_keyword_4_value = u''
    sch_organic_keyword_4_change = u''

    sch_organic_keyword_5 = u''
    sch_organic_keyword_5_value = u''
    sch_organic_keyword_5_change = u''

    sch_organic_keyword_part = response.xpath(u'//div[@class="searchKeywords-text searchKeywords-text--left '
                                              u'websitePage-mobileFramed"]//ul[@class="searchKeywords-list"]/li')
    sch_organic_keyword_index = 0
    for sch_organic_keyword in sch_organic_keyword_part:
        sch_organic_keyword_index += 1
        sch_organic_keyword_name = sch_organic_keyword.xpath(
            u'.//*[@class="searchKeywords-words"]/text()').extract_first(u'')
        sch_organic_keyword_value = sch_organic_keyword.xpath(
            u'.//*[@class="searchKeywords-trafficShare"]/text()').extract_first(u'')
        sch_organic_keyword_change = sch_organic_keyword.xpath(
            u'.//*[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')
        if sch_organic_keyword_index == 1:
            sch_organic_keyword_1 = sch_organic_keyword_name
            sch_organic_keyword_1_value = sch_organic_keyword_value
            sch_organic_keyword_1_change = sch_organic_keyword_change
        elif sch_organic_keyword_index == 2:
            sch_organic_keyword_2 = sch_organic_keyword_name
            sch_organic_keyword_2_value = sch_organic_keyword_value
            sch_organic_keyword_2_change = sch_organic_keyword_change
        elif sch_organic_keyword_index == 3:
            sch_organic_keyword_3 = sch_organic_keyword_name
            sch_organic_keyword_3_value = sch_organic_keyword_value
            sch_organic_keyword_3_change = sch_organic_keyword_change
        elif sch_organic_keyword_index == 4:
            sch_organic_keyword_4 = sch_organic_keyword_name
            sch_organic_keyword_4_value = sch_organic_keyword_value
            sch_organic_keyword_4_change = sch_organic_keyword_change
        elif sch_organic_keyword_index == 5:
            sch_organic_keyword_5 = sch_organic_keyword_name
            sch_organic_keyword_5_value = sch_organic_keyword_value
            sch_organic_keyword_5_change = sch_organic_keyword_change
    print u'第六部分 Search organic'
    print sch_of_trf_percent, sch_organic_percent, sch_paid_percent
    print sch_organic_keyword_1, sch_organic_keyword_2, sch_organic_keyword_3, sch_organic_keyword_4, sch_organic_keyword_5
    print sch_organic_keyword_1_value, sch_organic_keyword_2_value, sch_organic_keyword_3_value, sch_organic_keyword_4_value, sch_organic_keyword_5_value
    print sch_organic_keyword_1_change, sch_organic_keyword_2_change, sch_organic_keyword_3_change, sch_organic_keyword_4_change, sch_organic_keyword_5_change

    sch_paid_keyword_1 = u''
    sch_paid_keyword_1_value = u''
    sch_paid_keyword_1_change = u''

    sch_paid_keyword_2 = u''
    sch_paid_keyword_2_value = u''
    sch_paid_keyword_2_change = u''

    sch_paid_keyword_3 = u''
    sch_paid_keyword_3_value = u''
    sch_paid_keyword_3_change = u''

    sch_paid_keyword_4 = u''
    sch_paid_keyword_4_value = u''
    sch_paid_keyword_4_change = u''

    sch_paid_keyword_5 = u''
    sch_paid_keyword_5_value = u''
    sch_paid_keyword_5_change = u''

    sch_paid_keyword_part = response.xpath(
        u'//div[@class="searchKeywords-text searchKeywords-text--right websitePage-mobileFramed"]//ul[@class="searchKeywords-list"]/li')
    sch_paid_keyword_index = 0
    for sch_paid_keyword in sch_paid_keyword_part:
        sch_paid_keyword_index += 1
        sch_paid_keyword_name = sch_paid_keyword.xpath(
            u'.//*[@class="searchKeywords-words"]/text()').extract_first(u'')
        sch_paid_keyword_value = sch_paid_keyword.xpath(
            u'.//*[@class="searchKeywords-trafficShare"]/text()').extract_first(u'')
        sch_paid_keyword_change = sch_paid_keyword.xpath(
            u'.//*[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')
        if sch_paid_keyword_index == 1:
            sch_paid_keyword_1 = sch_paid_keyword_name
            sch_paid_keyword_1_value = sch_paid_keyword_value
            sch_paid_keyword_1_change = sch_paid_keyword_change
        elif sch_paid_keyword_index == 2:
            sch_paid_keyword_2 = sch_paid_keyword_name
            sch_paid_keyword_2_value = sch_paid_keyword_value
            sch_paid_keyword_2_change = sch_paid_keyword_change
        elif sch_paid_keyword_index == 3:
            sch_paid_keyword_3 = sch_paid_keyword_name
            sch_paid_keyword_3_value = sch_paid_keyword_value
            sch_paid_keyword_3_change = sch_paid_keyword_change
        elif sch_paid_keyword_index == 4:
            sch_paid_keyword_4 = sch_paid_keyword_name
            sch_paid_keyword_4_value = sch_paid_keyword_value
            sch_paid_keyword_4_change = sch_paid_keyword_change
        elif sch_paid_keyword_index == 5:
            sch_paid_keyword_5 = sch_paid_keyword_name
            sch_paid_keyword_5_value = sch_paid_keyword_value
            sch_paid_keyword_5_change = sch_paid_keyword_change
    print u'第六部分 Search paid'
    print sch_paid_keyword_1, sch_paid_keyword_2, sch_paid_keyword_3, sch_paid_keyword_4, sch_paid_keyword_5
    print sch_paid_keyword_1_value, sch_paid_keyword_2_value, sch_paid_keyword_3_value, sch_paid_keyword_4_value, sch_paid_keyword_5_value
    print sch_paid_keyword_1_change, sch_paid_keyword_2_change, sch_paid_keyword_3_change, sch_paid_keyword_4_change, sch_paid_keyword_5_change

    # 第七部分 Social
    soc_of_trf_percent = response.xpath(u'//span[@class="subheading-value social"]/text()').extract_first(u'')

    soc_trf_1 = u''
    soc_trf_1_value = u''

    soc_trf_2 = u''
    soc_trf_2_value = u''

    soc_trf_3 = u''
    soc_trf_3_value = u''

    soc_trf_4 = u''
    soc_trf_4_value = u''

    soc_trf_5 = u''
    soc_trf_5_value = u''

    soc_trf_part = response.xpath(u'//ul[@class="socialList"]/li')
    soc_trf_index = 0
    for soc_trf in soc_trf_part:
        soc_trf_index += 1
        soc_trf_name = soc_trf.xpath(u'.//a/text()').extract_first(u'')
        soc_trf_value = soc_trf.xpath(u'.//*[@class="socialItem-value"]/text()').extract_first(u'')
        if soc_trf_index == 1:
            soc_trf_1 = soc_trf_name
            soc_trf_1_value = soc_trf_value
        elif soc_trf_index == 2:
            soc_trf_2 = soc_trf_name
            soc_trf_2_value = soc_trf_value
        elif soc_trf_index == 3:
            soc_trf_3 = soc_trf_name
            soc_trf_3_value = soc_trf_value
        elif soc_trf_index == 4:
            soc_trf_4 = soc_trf_name
            soc_trf_4_value = soc_trf_value
        elif soc_trf_index == 5:
            soc_trf_5 = soc_trf_name
            soc_trf_5_value = soc_trf_value
    print u'第七部分 Social'
    print soc_of_trf_percent
    print soc_trf_1, soc_trf_2, soc_trf_3, soc_trf_4, soc_trf_5
    print soc_trf_1_value, soc_trf_2_value, soc_trf_3_value, soc_trf_4_value, soc_trf_5_value

    # 第八部分 Display Advertising
    ad_of_trf_percent = response.xpath(u'//span[@class="subheading-value display"]/text()').extract_first(u'')

    ad_top_publisher_1 = u''
    ad_top_publisher_2 = u''
    ad_top_publisher_3 = u''
    ad_top_publisher_4 = u''
    ad_top_publisher_5 = u''

    ad_top_publisher_part = response.xpath(u'//*[@data-waypoint="display"]//*[@class="websitePage-listItemContainer"]')
    ad_top_publisher_index = 0
    for ad_top_publisher in ad_top_publisher_part:
        ad_top_publisher_index += 1
        ad_top_publisher_value = ad_top_publisher.xpath(u'./a/text()').extract_first(u'')
        if ad_top_publisher_index == 1:
            ad_top_publisher_1 = ad_top_publisher_value
        elif ad_top_publisher_index == 2:
            ad_top_publisher_2 = ad_top_publisher_value
        elif ad_top_publisher_index == 3:
            ad_top_publisher_3 = ad_top_publisher_value
        elif ad_top_publisher_index == 4:
            ad_top_publisher_4 = ad_top_publisher_value
        elif ad_top_publisher_index == 5:
            ad_top_publisher_5 = ad_top_publisher_value
    print u'第八部分 Display Advertising'
    print ad_of_trf_percent
    print ad_top_publisher_1, ad_top_publisher_2, ad_top_publisher_3, ad_top_publisher_4, ad_top_publisher_5

    # 第九部分 Website Content
    web_sub_domain_1 = u''
    web_sub_domain_1_value = u''

    web_sub_domain_2 = u''
    web_sub_domain_2_value = u''

    web_sub_domain_3 = u''
    web_sub_domain_3_value = u''

    web_sub_domain_4 = u''
    web_sub_domain_4_value = u''

    web_sub_domain_5 = u''
    web_sub_domain_5_value = u''

    web_sub_domain_part = response.xpath(u'//div[@data-tab="subdomains"]//div[@class="websiteContent-tableLine"]')
    web_sub_domain_index = 0
    for web_sub_domain in web_sub_domain_part:
        web_sub_domain_index += 1
        web_sub_domain_name = web_sub_domain.xpath(u'.//span[@class="websiteContent-itemText"]/text()').extract_first(
            u'')
        web_sub_domain_value = web_sub_domain.xpath(
            u'.//span[@class="websiteContent-itemPercentage js-value"]/text()').extract_first(u'')
        if web_sub_domain_index == 1:
            web_sub_domain_1 = web_sub_domain_name
            web_sub_domain_1_value = web_sub_domain_value
        elif web_sub_domain_index == 2:
            web_sub_domain_2 = web_sub_domain_name
            web_sub_domain_2_value = web_sub_domain_value
        elif web_sub_domain_index == 3:
            web_sub_domain_3 = web_sub_domain_name
            web_sub_domain_3_value = web_sub_domain_value
        elif web_sub_domain_index == 4:
            web_sub_domain_4 = web_sub_domain_name
            web_sub_domain_4_value = web_sub_domain_value
        elif web_sub_domain_index == 5:
            web_sub_domain_5 = web_sub_domain_name
            web_sub_domain_5_value = web_sub_domain_value
    print u'第九部分 Website Content'
    print web_sub_domain_1, web_sub_domain_2, web_sub_domain_3, web_sub_domain_4, web_sub_domain_5
    print web_sub_domain_1_value, web_sub_domain_2_value, web_sub_domain_3_value, web_sub_domain_4_value, web_sub_domain_5_value

    # 第十部分 Audience Interests
    also_visit_web_1 = u''
    also_visit_web_2 = u''
    also_visit_web_3 = u''
    also_visit_web_4 = u''
    also_visit_web_5 = u''
    also_visit_web_part = response.xpath(
        u'//*[@data-waypoint="alsoVisited"]//*[@class="websitePage-listItemContainer"]')
    also_visit_web_index = 0
    for also_visit_web in also_visit_web_part:
        also_visit_web_index += 1
        also_visit_web_value = also_visit_web.xpath(u'./a/text()').extract_first(u'')
        if also_visit_web_index == 1:
            also_visit_web_1 = also_visit_web_value
        elif also_visit_web_index == 2:
            also_visit_web_2 = also_visit_web_value
        elif also_visit_web_index == 3:
            also_visit_web_3 = also_visit_web_value
        elif also_visit_web_index == 4:
            also_visit_web_4 = also_visit_web_value
        elif also_visit_web_index == 5:
            also_visit_web_5 = also_visit_web_value
    print u'第十部分 Audience Interests'
    print also_visit_web_1, also_visit_web_2, also_visit_web_3, also_visit_web_4, also_visit_web_5

    # 读取sql
    src_list = SimilarSrc.select().where(SimilarSrc.hash_code == hash_code)
    src = l_i(src_list, src_list, 0, None)
    plat_name = src.plat_name
    search_word = src.search_word
    plat_url = src.plat_url
    area = src.area

    all = [plat_name, plat_url, search_word] \
          + [over_view_time, global_rank, country_rank, category_rank, trf_total_visits, trf_total_visits_change,
             trf_avg_visit_duration, trf_pages_per_visit, trf_bounce_rate] \
          + [trf_country_1, trf_country_1_value, trf_country_1_change] \
          + [trf_country_2, trf_country_2_value, trf_country_2_change] \
          + [trf_country_3, trf_country_3_value, trf_country_3_change] \
          + [trf_country_4, trf_country_4_value, trf_country_4_change] \
          + [trf_country_5, trf_country_5_value, trf_country_5_change] \
          + [trf_source_direct, trf_source_referrals, trf_source_search, trf_source_social, trf_source_mail,
             trf_source_display] \
          + [ref_of_trf_percent, ref_top_site_1, ref_top_site_1_value, ref_top_site_1_change] \
          + [ref_top_site_2, ref_top_site_2_value, ref_top_site_2_change] \
          + [ref_top_site_3, ref_top_site_3_value, ref_top_site_3_change] \
          + [ref_top_site_4, ref_top_site_4_value, ref_top_site_4_change] \
          + [ref_top_site_5, ref_top_site_5_value, ref_top_site_5_change] \
          + [ref_des_site_1, ref_des_site_1_value, ref_des_site_1_change] \
          + [ref_des_site_2, ref_des_site_2_value, ref_des_site_2_change] \
          + [ref_des_site_3, ref_des_site_3_value, ref_des_site_3_change] \
          + [ref_des_site_4, ref_des_site_4_value, ref_des_site_4_change] \
          + [ref_des_site_5, ref_des_site_5_value, ref_des_site_5_change] \
          + [sch_of_trf_percent, sch_organic_percent, sch_paid_percent] \
          + [sch_organic_keyword_1, sch_organic_keyword_1_value, sch_organic_keyword_1_change] \
          + [sch_organic_keyword_2, sch_organic_keyword_2_value, sch_organic_keyword_2_change] \
          + [sch_organic_keyword_3, sch_organic_keyword_3_value, sch_organic_keyword_3_change] \
          + [sch_organic_keyword_4, sch_organic_keyword_4_value, sch_organic_keyword_4_change] \
          + [sch_organic_keyword_5, sch_organic_keyword_5_value, sch_organic_keyword_5_change] \
          + [sch_paid_keyword_1, sch_paid_keyword_1_value, sch_paid_keyword_1_change] \
          + [sch_paid_keyword_2, sch_paid_keyword_2_value, sch_paid_keyword_2_change] \
          + [sch_paid_keyword_3, sch_paid_keyword_3_value, sch_paid_keyword_3_change] \
          + [sch_paid_keyword_4, sch_paid_keyword_4_value, sch_paid_keyword_4_change] \
          + [sch_paid_keyword_5, sch_paid_keyword_5_value, sch_paid_keyword_5_change] \
          + [soc_of_trf_percent] \
          + [soc_trf_1, soc_trf_1_value] \
          + [soc_trf_2, soc_trf_2_value] \
          + [soc_trf_3, soc_trf_3_value] \
          + [soc_trf_4, soc_trf_4_value] \
          + [soc_trf_5, soc_trf_5_value] \
          + [ad_of_trf_percent] \
          + [ad_top_publisher_1, ad_top_publisher_2, ad_top_publisher_3, ad_top_publisher_4, ad_top_publisher_5] \
          + [web_sub_domain_1, web_sub_domain_1_value] \
          + [web_sub_domain_2, web_sub_domain_2_value] \
          + [web_sub_domain_3, web_sub_domain_3_value] \
          + [web_sub_domain_4, web_sub_domain_4_value] \
          + [web_sub_domain_5, web_sub_domain_5_value] \
          + [also_visit_web_1, also_visit_web_2, also_visit_web_3, also_visit_web_4, also_visit_web_5]
    return area, hash_code, all


def start_before():
    # 得到状态，存储地址
    loop_cache = getLoopCache()

    last = loop_cache.get(u'last', {})
    new = loop_cache.get(u'new', {})
    status_last = last.get(u'status', u'')
    status_new = new.get(u'status', u'')

    if status_new == u'complete':
        # 说明需要解析
        dir = new.get(u'dir', u'')
    else:
        if status_last == u'complete':
            dir = last.get(u'dir', u'')
        else:
            return
    # 获取dir下面的所有html
    start(u'C:\\gsma\\pythonWorkSpace\\componey\\similar_web_catch\\trivest_spider\\html\\' + dir, dir)


def start(html_path, save_dir):
    title_names = [u'plat_name', u'plat_url', u'search_word'] \
                  + [u'over_view_time', u'global_rank', u'country_rank', u'category_rank', u'trf_total_visits',
                     u'trf_total_visits_change', u'trf_avg_visit_duration', u'trf_pages_per_visit', u'trf_bounce_rate'] \
                  + [u'trf_country_1', u'trf_country_1_value', u'trf_country_1_change'] \
                  + [u'trf_country_2', u'trf_country_2_value', u'trf_country_2_change'] \
                  + [u'trf_country_3', u'trf_country_3_value', u'trf_country_3_change'] \
                  + [u'trf_country_4', u'trf_country_4_value', u'trf_country_4_change'] \
                  + [u'trf_country_5', u'trf_country_5_value', u'trf_country_5_change'] \
                  + [u'trf_source_direct', u'trf_source_referrals', u'trf_source_search', u'trf_source_social',
                     u'trf_source_mail', u'trf_source_display'] \
                  + [u'ref_of_trf_percent', u'ref_top_site_1', u'ref_top_site_1_value', u'ref_top_site_1_change'] \
                  + [u'ref_top_site_2', u'ref_top_site_2_value', u'ref_top_site_2_change'] \
                  + [u'ref_top_site_3', u'ref_top_site_3_value', u'ref_top_site_3_change'] \
                  + [u'ref_top_site_4', u'ref_top_site_4_value', u'ref_top_site_4_change'] \
                  + [u'ref_top_site_5', u'ref_top_site_5_value', u'ref_top_site_5_change'] \
                  + [u'ref_des_site_1', u'ref_des_site_1_value', u'ref_des_site_1_change'] \
                  + [u'ref_des_site_2', u'ref_des_site_2_value', u'ref_des_site_2_change'] \
                  + [u'ref_des_site_3', u'ref_des_site_3_value', u'ref_des_site_3_change'] \
                  + [u'ref_des_site_4', u'ref_des_site_4_value', u'ref_des_site_4_change'] \
                  + [u'ref_des_site_5', u'ref_des_site_5_value', u'ref_des_site_5_change'] \
                  + [u'sch_of_trf_percent', u'sch_organic_percent', u'sch_paid_percent'] \
                  + [u'sch_organic_keyword_1', u'sch_organic_keyword_1_value', u'sch_organic_keyword_1_change'] \
                  + [u'sch_organic_keyword_2', u'sch_organic_keyword_2_value', u'sch_organic_keyword_2_change'] \
                  + [u'sch_organic_keyword_3', u'sch_organic_keyword_3_value', u'sch_organic_keyword_3_change'] \
                  + [u'sch_organic_keyword_4', u'sch_organic_keyword_4_value', u'sch_organic_keyword_4_change'] \
                  + [u'sch_organic_keyword_5', u'sch_organic_keyword_5_value', u'sch_organic_keyword_5_change'] \
                  + [u'sch_paid_keyword_1', u'sch_paid_keyword_1_value', u'sch_paid_keyword_1_change'] \
                  + [u'sch_paid_keyword_2', u'sch_paid_keyword_2_value', u'sch_paid_keyword_2_change'] \
                  + [u'sch_paid_keyword_3', u'sch_paid_keyword_3_value', u'sch_paid_keyword_3_change'] \
                  + [u'sch_paid_keyword_4', u'sch_paid_keyword_4_value', u'sch_paid_keyword_4_change'] \
                  + [u'sch_paid_keyword_5', u'sch_paid_keyword_5_value', u'sch_paid_keyword_5_change'] \
                  + [u'soc_of_trf_percent'] \
                  + [u'soc_trf_1', u'soc_trf_1_value'] \
                  + [u'soc_trf_2', u'soc_trf_2_value'] \
                  + [u'soc_trf_3', u'soc_trf_3_value'] \
                  + [u'soc_trf_4', u'soc_trf_4_value'] \
                  + [u'soc_trf_5', u'soc_trf_5_value'] \
                  + [u'ad_of_trf_percent'] \
                  + [u'ad_top_publisher_1', u'ad_top_publisher_2', u'ad_top_publisher_3', u'ad_top_publisher_4',
                     u'ad_top_publisher_5'] \
                  + [u'web_sub_domain_1', u'web_sub_domain_1_value'] \
                  + [u'web_sub_domain_2', u'web_sub_domain_2_value'] \
                  + [u'web_sub_domain_3', u'web_sub_domain_3_value'] \
                  + [u'web_sub_domain_4', u'web_sub_domain_4_value'] \
                  + [u'web_sub_domain_5', u'web_sub_domain_5_value'] \
                  + [u'also_visit_web_1', u'also_visit_web_2', u'also_visit_web_3', u'also_visit_web_4',
                     u'also_visit_web_5']

    data_obj = {}

    path_list = get_all_file_path(html_path)
    for path in path_list:
        file_path = path[0]
        file_name = path[1]
        file_name_all = path[2]
        area, hash_code, data_detail = parse_before(file_path, file_name)

        data_item = data_obj.get(area, {
            u'sheet_name': area,
            u'rows': [
                title_names,
            ]
        })
        rows = data_item.get(u'rows', [
            title_names
        ])
        rows.append(data_detail)
        data_item[u'rows'] = rows
        data_obj[area] = data_item
    # 之后批量插入
    data_list = []
    for key in data_obj:
        data_list.append(data_obj[key])
        print data_obj[key]

        save_xls_file(data_list, save_dir)


if __name__ == '__main__':
    start_before()
