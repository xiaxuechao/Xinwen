# --*-- coding:utf-8 --*--
from scrapy.item import Item
from scrapy.item import Field
class NewsItem(Item):
    # 域名
    domain = Field()
    # 新闻原文链接
    url = Field()
    # 标题
    title = Field()
    # 来源
    reference = Field()
    # 作者
    author = Field()
    # 发布时间
    publish_date = Field()
    # 关键词
    keywords = Field()
    # 摘要
    abstract = Field()
    # 【abstract非中文时，中文摘要】
    custom_abstract = Field()
    # 新闻正文
    content = Field()
    # 新闻中的图片链接
    image_url = Field()
    # 文章语言
    language = Field()
    # 新闻在模块
    module = Field()
    # 正文部分的html
    html_content = Field()
    # 所爬网站名
    site_name = Field()
    # 扩展字段
    meta_data = Field()
    ##唯一id
    hash_code = Field()

