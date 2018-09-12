# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
import time
from Xinwen.items.news import NewsItem
from readability.readability import Document
from Xinwen.spiders.base_.Base_ import Base_Spiders
from scrapy.loader import ItemLoader

class Uav81Spider(Base_Spiders):
    name = 'xinwen'
    allowed_domains = []
    start_urls = [
        'http://www.ciiip.com/newslisting.aspx?page=1&tid=648'
    ]
    site_name = "中国智能化产业与产品网"
    rules = (
        Rule(LinkExtractor(allow=r"http://www.ciiip.com/newslisting.aspx\?page=\d&tid=648", restrict_css="div.qzPagination"), follow=True),
        Rule(LinkExtractor(allow=r'http://www.ciiip.com/news-\d{4}-648.html', restrict_css='li a'),follow=False, callback="parse_item"),
    )
    MG_COLLECTION = "xinwen"
    def parse_item(self, response):
        sel = Selector(response)
        try:
            print(response.url)
            #region title
            if sel.css("h1#title::text").extract_first().strip():
                title = sel.css("h1#title::text").extract_first().strip()
            elif sel.xpath("//title/text()").extract_first().strip():
                title = sel.xpath("//title/text()").extract_first().strip()
            else:
                title = ""
            #endregion
            #region publish_data
            if sel.css("span#pubtime::text").re_first(r"\d{4}年\d{2}月\d{2}日"):
                publish_data = sel.css("span#pubtime::text").re_first("\d{4}年\d{2}月\d{2}日")
            else:
                publish_data = ""
            # endregion
            #region reference
            if sel.css("span#pubtime::text").re_first(r"来源:(.*)"):
                reference = sel.css("span#pubtime::text").re_first(r"来源:(.*)")
            else:
                reference = ""
            #endregion
            #region keywords
            if sel.xpath("//div[@class='zuoyou0']/div[5]/font/text()").extract():
                keywords = ",".join(sel.xpath("//div[@class='zuoyou0']/div[5]/font/text()").extract())
            elif sel.xpath("//div[@class='zuoyou0']/div[4]/font/text()").extract():
                keywords = ",".join(sel.xpath("//div[@class='zuoyou0']/div[4]/font/text()").extract())
            elif sel.xpath('//meta[@name="keywords"]/@content').extract_first():
                keywords = ",".join(sel.xpath('//meta[@name="keywords"]/@content').extract_first())
            else:
                keywords = ''
            #endregion
            #region html_content
            if sel.xpath("//div[@class='duiqi']/p/font/text()").extract():
                html_content = "".join(sel.xpath("//div[@class='duiqi'][2]/p").extract())
            else:
                html_content = Document(response.text).summary()
                html_content = html_content.replace('<html><body>','').replace('<html><body>','')
            content = "".join(Selector(text=html_content).css("::text").extract())

            #endregion
            #region img_url
            if Selector(text=html_content).css("img::attr(src)").extract():
                img = Selector(text=html_content).css("img::attr(src)").extract_first
            else:
                img = ''

            #endregion


            # region item
            i = ItemLoader(item=NewsItem(), response=response)
            if (title):
                i.add_value(field_name='title', value=title)
                i.add_value(field_name='publish_date', value=publish_data)
                i.add_value(field_name="reference", value=reference)
                # i.add_value(field_name="author", value=authon)
                i.add_value(field_name="keywords", value=keywords)
                i.add_value(field_name="html_content", value=html_content)
                i.add_value(field_name="image_url", value=img)
                # 补全代码
                # 基类

                yield i.load_item()
            # endregion
        except Exception as e:
            print(e.args)
