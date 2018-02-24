# -*- coding: utf-8 -*-
# similarWeb 详情解析
from scrapy import Selector

from trivest_spider.parse import value


def detailBaseParse(spider, response):
    spider_name = spider.name
    spider.logInfo(spider_name)
    if False:
        spider.logWarn(u'访问过多被禁止')
        return None

    src_id = response.meta[u'src_id']
    search_word = response.meta[u'search_word']
    plat_name = response.meta[u'plat_name']
    hash_code = response.meta[u'hash_code']

    spider.saveFile(hash_code, response.body)

    source_url = response.url
    spider.logInfo(u'开始解析：%s' % plat_name + source_url)

    info = response.xpath(u'//div[@class="websiteHeader-companyDescriptionWrapper"]/p[@itemprop="description"]/text()').extract_first(u'')

    over_view_time = response.xpath(u'//div[@class="websiteHeader-date"]/span[@class="websiteHeader-dateFull"]/text()').extract_first(u'')

    # 第一部分
    global_rank = response.xpath(u'//li[@class="websiteRanks-item js-globalRank"]'
                                 u'//div[@class="websiteRanks-valueContainer js-websiteRanksValue"]/text()').extract_first(u'')
    country_rank = response.xpath(u'//li[@class="websiteRanks-item js-countryRank"]'
                                 u'//div[@class="websiteRanks-valueContainer js-websiteRanksValue"]/text()').extract_first(u'')
    category_rank = response.xpath(u'//li[@class="websiteRanks-item js-categoryRank"]'
                                 u'//div[@class="websiteRanks-valueContainer js-websiteRanksValue"]/text()').extract_first(u'')

    # 第二部分
    trf_total_visits = response.xpath(u'//span[@class="engagementInfo-valueNumber js-countValue"][1]/text()').extract_first(u'')
    trf_total_visits_change = response.xpath(u'//span[@class="engagementInfo-value engagementInfo-value--large u-text-ellipsis"]'
                                      u'//span[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')
    trf_avg_visit_duration = response.xpath(u'//span[@class="engagementInfo-valueNumber js-countValue"][2]/text()').extract_first(u'')
    trf_pages_per_visit = response.xpath(u'//span[@class="engagementInfo-valueNumber js-countValue"][3]/text()').extract_first(u'')
    trf_bounce_rate = response.xpath(u'//span[@class="engagementInfo-valueNumber js-countValue"][4]/text()').extract_first(u'')


    # content_item = {
    #     u'hash_code': hash_code,
    #     u'search_word': search_word,
    #     u'src_id': src_id,
    #     u'url': source_url,
    #     u'info': info,
    #     u'content': content
    # }
    #
    # return content_item

def i_e(condition, yes, no):
    if condition:
        return yes
    else:
        return no


if __name__ == '__main__':
    pass
    response = Selector(text=value.html)
    info = response.xpath(
        u'//div[@class="websiteHeader-companyDescriptionWrapper"]/p[@itemprop="description"]/text()').extract_first(u'')

    over_view_time = response.xpath(
        u'//div[@class="websiteHeader-date"]/span[@class="websiteHeader-dateFull"]/text()').extract_first(u'')

    # 第一部分
    rank_list = u''.join(response.xpath(u'//div[@class="websiteRanks-valueContainer js-websiteRanksValue"]/text()').extract()).split()

    global_rank = i_e(len(rank_list), rank_list[0], u'')
    country_rank = i_e(len(rank_list)>1, rank_list[1], u'')
    category_rank = i_e(len(rank_list)>2, rank_list[2], u'')

    # 第二部分 https://www.similarweb.com/website/bitcoin.co.id
    second_part = response.xpath(u'//span[@class="engagementInfo-valueNumber js-countValue"]/text()').extract()

    trf_total_visits = i_e(len(second_part), second_part[0], u'')
    trf_avg_visit_duration = i_e(len(second_part) > 1, second_part[1], u'')
    trf_pages_per_visit = i_e(len(second_part) > 2, second_part[2], u'')
    trf_bounce_rate = i_e(len(second_part) > 3, second_part[3], u'')

    trf_total_visits_change = response.xpath(
        u'//span[@class="engagementInfo-value engagementInfo-value--large u-text-ellipsis"]'
        u'//span[@class="websitePage-relativeChangeNumber"]/text()').extract_first(u'')

    print global_rank, country_rank, category_rank, trf_total_visits, trf_avg_visit_duration, trf_pages_per_visit, trf_bounce_rate