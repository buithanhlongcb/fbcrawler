from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json
def save_html(htmlbody, name):
    filename = 'body' + name +'.html'
    with open(filename, 'wb') as f:
        f.write(htmlbody)

class FbBaseSpider(Spider):
    name = "fb"
    allowed_domains = ['facebook.com']
    start_urls = ['https://mbasic.facebook.com/login']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        if not self.email or not self.password:
            raise CloseSpider('Please provide email or password')

        self.page_id = kwargs.get('page_id')
        if not self.page_id:
            raise CloseSpider('Please provide page_id')
        if ',' in self.page_id:
            self.page_id = self.page_id.split(',')
        else:
            self.page_id = [self.page_id]

    def parse(self, response):
        return FormRequest.from_response(
                response,
                formxpath='//form[contains(@action, "login")]',
                formdata={'email': self.email,'pass': self.password},
                callback=self.parse_home
                )
    
    def parse_home(self, response):
        urls = ['https://mbasic.facebook.com/' + id_page + "/?_rdr" for id_page in self.page_id]
        for url in urls:
            yield response.follow(url, self.parse_page, dont_filter=True)

    def parse_page(self, response):
        name = 'homepage'
        save_html(response.body, name)
        id_posts = response.xpath("//*[contains(text(), 'Full Story')]/@href").extract()
        for id_post in id_posts:
            href = 'http://mbasic.facebook.com' + id_post
            yield response.follow(href, self.parse_comment, dont_filter=True)

    def parse_comment(self, response):
        url = response.url
        id_page = url[url.find('Acontent_owner_id_new.') + len('Acontent_owner_id_new.'):url.find('%', url.find('Acontent_owner_id_new.'))]
        id_post = url[url.find('mf_story_key')+len('mf_story_key.'):url.find('%')]
        #users = response.xpath('').extract()
        #users = [remove_accent(user) for user in users]
        if response.xpath('//div[@id="MPhotoContent"]') == []:
            comments = response.xpath('//div[@id="root"]/div/div[2]/div/div[5]/div/div') 
        else:
            comments = response.xpath('//div[@id="MPhotoContent"]/div[2]/div/div/div[4]/div/div')
        
        if comments.xpath('./div[4]/div/div/a/@href').extract() != []:
            rep_urls = comments.xpath('./div[4]/div/div/a/@href').extract()
            for rep_url in rep_urls:
                next_url = 'http://mbasic.facebook.com' + rep_url
                yield response.follow(next_url, self.parse_comment_rep)

        for comment in comments:
            user = comment.xpath('./h3/a/text()').extract()
            tags = comment.xpath('./div[1]/a/text()').extract()
            content = comment.xpath('./div[1]/text()').extract()
            yield {
                'Idpage - Idpost':id_page + " - "+id_post, 
                'User': user,
                'Comment': content,
                'Tag': tags,
            }
        
        next_id_comments = response.xpath("//*[contains(text(), 'View more comments…')]/@href").extract()
        for next_id_comment in next_id_comments:
            next_url = 'http://mbasic.facebook.com' + next_id_comment
            yield response.follow(next_url, self.parse_comment, dont_filter=True)
        
    def parse_comment_rep(self, response):
        url = response.url
        id_page = url[url.find('Acontent_owner_id_new.') + len('Acontent_owner_id_new.'):url.find('%', url.find('Acontent_owner_id_new.'))]
        id_post = url[url.find('mf_story_key')+len('mf_story_key.'):url.find('%')]
        comments = response.xpath('//div[@id="root"]/div/div[3]/div/div') 
        if len(comments) >= 10:
            save_html(response.body, id_post)
        for comment in comments:
            user = comment.xpath('./h3/a/text()').extract()
            tags = comment.xpath('./div[1]/a/text()').extract()
            content = comment.xpath('./div[1]/text()').extract()
            yield {
                #'Url': url,
                'Idpage - Idpost':id_page + " - "+id_post, 
                'User': user,
                'Comment': content,
                'Tag': tags,
            }       
        next_id_comments = response.xpath("//*[contains(text(), 'View more comments…')]/@href").extract()
        for next_id_comment in next_id_comments:
            next_url = 'http://mbasic.facebook.com' + next_id_comment
            yield response.follow(next_url, self.parse_comment_rep, dont_filter=True)