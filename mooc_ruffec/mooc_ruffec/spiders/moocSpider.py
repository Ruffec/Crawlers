# -*- coding: utf-8 -*-
import scrapy
from mooc_ruffec.items import MoocRuffecItem

class MoocspiderSpider(scrapy.Spider):
    name = 'moocSpider'
    allowed_domains = ['www.imooc.com']
    start_urls = []
    for i in range(5):
        url = 'https://www.imooc.com/course/list?page=' + str(i)
        start_urls.append(url)
    def parse(self, response):
        items = MoocRuffecItem()
        # 先获每个课程的div
        for sel in response.xpath("//div[@class='course-card-container']/a[@target='_blank']"):
            # 获取div中的课程标题
            items["title"] = sel.xpath(".//h3/text()").extract()
            # 获取每个div中的课程路径
            items["url"] = 'http://www.imooc.com' + sel.xpath('.//@href').extract()[0]
            # 获取div中的标题图片地址
            items['image_url'] = sel.xpath('.//@src').extract()
            # 获取div中的学生人数
            items['student'] = sel.xpath('.//span/text()').extract()[1].strip()
            # 获取div中的课程简介
            items['introduction'] = sel.xpath('.//p/text()').extract()
            print("title : %s, url : %s, image_url : %s, student : %s, introduction : %s"
                  %(items["title"], items["url"], items["image_url"], items["student"], items["introduction"]))

            yield items

