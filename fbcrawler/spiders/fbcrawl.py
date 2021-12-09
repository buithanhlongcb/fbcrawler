from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json

class FbBaseSpider(Spider):
    name = "fb"
    allowed_domains = ['facebook.com']
    start_urls = ["https://mbasic.facebook.com/us.vnuhcm/?_rdr"]
    


    def parse(self, response):
        id_posts = response.xpath('//div[@data-ft]/div[2]/a[2]/@href').extract()
        for id_post in id_posts:
                href = 'http://mbasic.facebook.com/' + id_post
                yield response.follow(href, self.parse_comment)

    def parse_comment(self, response):
        url = response.url
        #users = response.xpath('').extract()
        #users = [remove_accent(user) for user in users]
        if response.xpath('//div[@id="MPhotoContent"]') == []:
            comments = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div/div')
        else:
            comments = response.xpath('//div[@id="MPhotoContent"]/div[2]/div/div/div[3]/div/div')
        for comment in comments:
            user = comment.xpath('./h3/a/text()').extract()
            tags = comment.xpath('./div[1]/a/text()').extract()
            content = comment.xpath('./div[1]/text()').extract()
            yield {
                'Url': url,
                'User': user,
                'Comment': content,
                'Tag': tags,
            }
        #comments = [re.compile(r'<[^>]+>').sub('', comment) for comment in comments]
        #comments = [remove_accent(comment) for comment in comments]
        next_id_comment = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div/a/@href').extract()
        next_url =''
        if next_id_comment != []:
            next_url = 'http://mbasic.facebook.com' + next_id_comment[-1]
            yield response.follow(next_url, self.parse_comment)

        #yield {
        #        'Url': url,
        #        'User': users,
        #        'Comment': comments,
        #        'Tag': tags,
        #        'Next_url': next_url
        #    }
        