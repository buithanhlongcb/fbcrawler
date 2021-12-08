from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json
import unidecode

def remove_accent(text):
    return unidecode.unidecode(text)


class FbBaseSpider(Spider):
    name = "fb"
    allowed_domains = ['facebook.com']
    start_urls = ["https://mbasic.facebook.com/us.vnuhcm/?_rdr"]
    
    def parse(self, response):
        questions = Selector(response).xpath('//div[@data-ft]/@data-ft').extract()
        for question in questions:
            jsonfile = json.loads(question)
            if 'mf_story_key' in jsonfile:
                id_post = jsonfile['mf_story_key']
                href = 'http://mbasic.facebook.com/' + id_post
                yield response.follow(href, self.parse_comment)

    def parse_comment(self, response):
        url = response.url
        users = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div/div/h3/a/text()').extract()
        users = [remove_accent(user) for user in users]
        comments = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div/div/div[1]').extract()
        comments = [re.compile(r'<[^>]+>').sub('', comment) for comment in comments]
        comments = [remove_accent(comment) for comment in comments]
        next_id_comment = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div/a/@href').extract()
        next_url =''
        if next_id_comment != []:
            next_url = 'http://mbasic.facebook.com' + next_id_comment[-1]

        yield {
                'Url': url,
                'User': users,
                'Comment': comments,
                'Next_url': next_url
            }

        if next_id_comment != []:
            yield response.follow(next_url, self.parse_comment)
