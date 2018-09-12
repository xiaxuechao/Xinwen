# -*- coding: utf-8 -*-
import scrapy,re
from scrapy.spiders import CrawlSpider,Rule,Request
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from Xinwen.items.news import NewsItem
# from scrapy.loader import ItemLoader
from readability.readability import Document



class BiaodanSpider(CrawlSpider):
    name = 'tu'
    allowed_domains = []
    start_urls = ['http://www.ttbz.org.cn/']

    custom_settings = {
        "urls":"http://www.ttbz.org.cn/Home/Standard?tdsourcetag=s_pcqq_aiomsg&page={}",
        "page_count":"3",
        "MG_COLLECTION":"biange"
    }

    rules = (
        Rule(LinkExtractor(allow=r"http://www.ttbz.org.cn/StandardManage/Detail/\d+/",restrict_css="td a"),follow=False,callback="parse_item"),
    )
    MG_COLLECTION = "biange"
    def start_requests(self):
        url = self.custom_settings.get("urls")
        max_page = int(self.custom_settings.get("page_count"))
        for i in range(max_page):
            yield Request(url=url.format(i+1),dont_filter=True)

    def parse_item(self, response):
        sel = Selector(response)
        try:
            print(response.url)
            #region 标准信息
            list2 = sel.xpath("//table[@class='tctable'][2]//tr/td/text()").extract()[:-2]
            for i in range(len(list2)):
                c = str(list2[i] + ":" + sel.xpath("//table[@class='tctable'][2]//tr["+str(i+2)+"]//text()").extract()[3].strip())
                print(c)
            #endregion
            #region 标准信息1
            t_heads = sel.css("table.tctable th::text").extract()
            param = {}
            for j in range(len(t_heads)):
                if t_heads[j].find('标准详细信息') > -1:
                    trs = sel.xpath('//table[@class="tctable"][%d]' % (j + 1)).css("tr")
                    for tr in trs[1:]:
                        temp_key = "" if not tr.xpath('td[1]/text()').extract_first() else tr.xpath('td[1]/text()').extract_first().strip()
                        temp_val = "" if not tr.xpath('td[2]/span/text()').extract_first() else tr.xpath('td[2]/span/text()').extract_first().strip()
                        param.update({temp_key:temp_val})
            #endregion
            #region 团体信息


            #endregion
            #region item
            status = param.get("标准状态")
            serial_number = param.get("标准编号")
            chines_title = param.get("中文标题")
            engilish_title = param.get("英文标题")
            international_number = param.get("国际标准分类号")
            china_number = param.get("中国标准分类号")
            economics_classify = param.get("国名经济分类")
            issue_date = param.get("发布日期")
            material_date = param.get("实施日期")
            drafter = param.get("起草人")
            unit = param.get("起草单位")
            ranges = param.get("范围")
            technology_body = param.get("主要技术内容")
            patent_information = param.get("是否包含专利信息")
            standard_text = param.get("标准文本")
            i = NewsItem(item=NewsItem(), response=response)
            if (status):
                i.add_value(field_name='status', value=status)
                i.add_value(field_name='serial_number', value=serial_number)
                i.add_value(field_name='chines_title', value=chines_title)
                i.add_value(field_name='engilish_title', value=engilish_title)
                i.add_value(field_name='international_number', value=international_number)
                i.add_value(field_name='china_number', value=china_number)
                i.add_value(field_name='economics_classify', value=economics_classify)
                i.add_value(field_name='issue_date', value=issue_date)
                i.add_value(field_name='material_date', value=material_date)
                i.add_value(field_name='drafter', value=drafter)
                i.add_value(field_name='unit', value=unit)
                i.add_value(field_name='ranges', value=ranges)
                i.add_value(field_name='technology_body', value=technology_body)
                i.add_value(field_name='patent_information', value=patent_information)
                i.add_value(field_name='standard_text', value=standard_text)

                yield i.load_item()
            #endregion

            pass
        except Exception as e:
            print(e.args)

# -*- coding: utf-8 -*-
import scrapy, re
# from scrapy.spiders import CrawlSpider, Rule, Request
# from scrapy.linkextractors import LinkExtractor
# from scrapy import Selector
# from readability.readability import Document
#
#
# class BiaodanSpider(CrawlSpider):
#     name = 'tu'
#     allowed_domains = []
#     start_urls = ['http://www.ttbz.org.cn/']
#     custom_settings = {
#         "urls": "http://www.ttbz.org.cn/Home/Standard?tdsourcetag=s_pcqq_aiomsg&page={}",
#         "page_count": "5",
#     }
#     rules = (
#         Rule(LinkExtractor(allow=r"http://www.ttbz.org.cn/StandardManage/Detail/\d+/", restrict_css="td a"),follow=False, callback="parse_item"),
#     )
#     def start_requests(self):
#         url = self.custom_settings.get("urls")
#         max_page = int(self.custom_settings.get("page_count"))
#         for i in range(max_page):
#             yield Request(url=url.format(i + 1), dont_filter=True)
#     def parse_item(self, response):
#         sel = Selector(response)
#         try:
#             print(response.url)
#             # region 标准信息
#             list2 = sel.xpath("//table[@class='tctable'][2]//tr/td/text()").extract()[:-2]
#             for i in range(len(list2)):
#                 c = str(list2[i] + ":" + sel.xpath("//table[@class='tctable'][2]//tr["+str(i+2)+"]//text()").extract()[3].strip())
#                 print(c)
#             # # endregion
#             # # region 标准信息1
#             t_heads = sel.css("table.tctable th::text").extract()
#             a = {}
#             for j in range(len(t_heads)):
#                 if t_heads[j].find('标准详细信息') > -1:
#                     trs = sel.xpath('//table[@class="tctable"][%d]' % (j + 1)).css("tr")
#                     for tr in trs[1:]:
#                         temp_key = "" if not tr.xpath('td[1]/text()').extract_first() else tr.xpath('td[1]/text()').extract_first().strip()
#                         temp_val = "" if not tr.xpath('td[2]/span/text()').extract_first() else tr.xpath('td[2]/span/text()').extract_first().strip()
#                         a.update({temp_key:temp_val})
#             # endregion
            # region 团体信息
        #     list1 = sel.xpath("//table[@class='tctable'][1]//tr/td/text()").extract()[:-2]
        #     for u in range(len(list1)):
        #         k = str(list1[u] + ":" +sel.xpath("//table[@class='tctable'][1]//tr[" + str(u - 1) + "]//text()").extract()[3].strip())
        #         print(k)
        #     t_head = sel.css("table.tctable th::text").extract()
        #     w = {}
        #     for j in range(len(t_head)):
        #         if t_head[j].find('团体详细信息'):
        #             trd =sel.xpath('//table[@class="tctable"][%d]' % (j +1)).css("tr").extract()
        #             for tr in trd[1:]:
        #                 temp_key = "" if not tr.xpath('td[1]/text()').extract_first() else tr.xpath('td[1]/text()').extract_first().strip()
        #                 temp_val = "" if not tr.xpath('td[2]/span/text()').extract_first() else tr.xpath('td[2]/span/text()').extract_first().strip()
        #                 w.update({temp_key:temp_val})
        #
        #     #
        #     # endregion
        #
        #     pass
        # except Exception as e:
        #     print(e.args)
