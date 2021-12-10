from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json



class FbBaseSpider(Spider):
    name = "fb"
    allowed_domains = ['facebook.com']
    start_urls = ['https://mbasic.facebook.com/login']
    
    def __init__(self):
        self.id_pages = ['us.vnuhcm']
        self.email = "longlong.031.2000@gmail.com"
        self.password = "LongLong031"
        self.flags= 0
        self.flags_rep = 0


    def parse(self, response):
        return FormRequest.from_response(
                response,
                formxpath='//form[contains(@action, "login")]',
                formdata={'email': self.email,'pass': self.password},
                callback=self.parse_home
                )
    
    def parse_home(self, response):
        urls = ['https://mbasic.facebook.com/' + id_page + "/?_rdr" for id_page in self.id_pages]
        for url in urls:
            yield response.follow(url, self.parse_page)

    def parse_page(self, response):
        filename = 'home.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        id_posts = response.xpath('//div[@id="timelineBody"]/div[2]/div/div/div/div/div/div[2]/a[3]/@href').extract() 
        for id_post in id_posts:
                href = 'http://mbasic.facebook.com' + id_post
                yield response.follow(href, self.parse_comment)

    def parse_comment(self, response):
        filename = 'home' + str(self.flags) + '.html'
        self.flags +=1
        with open(filename, 'wb') as f:
            f.write(response.body)
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
                #'Url': url,
                'Idpage - Idpost':id_page + " - "+id_post, 
                'User': user,
                'Comment': content,
                'Tag': tags,
                'html': self.flags-1
            }
        #comments = [re.compile(r'<[^>]+>').sub('', comment) for comment in comments]
        #comments = [remove_accent(comment) for comment in comments]
        next_id_comment = response.xpath('//div[@id="root"]/div/div[2]/div/div[5]/div/a/@href').extract()  

        if next_id_comment != []:
            next_url = 'http://mbasic.facebook.com' + next_id_comment[-1]
            if len(next_id_comment) == 1:
                if 'View previous comments' in response.xpath('//div[@id="root"]/div/div[2]/div/div[5]/div/a/text()')[0].extract():
                    next_url =''

            if next_url != '':
                yield response.follow(next_url, self.parse_comment)

        #yield {
        #        'Url': url,
        #        'User': users,
        #        'Comment': comments,
        #        'Tag': tags,
        #        'Next_url': next_url
        #    }
        
    def parse_comment_rep(self, response):
        filename = 'rep_cmt' + str(self.flags_rep) +'.html'
        self.flags_rep +=1
        with open(filename, 'wb') as f:
            f.write(response.body)
        url = response.url

        id_page = url[url.find('Acontent_owner_id_new.') + len('Acontent_owner_id_new.'):url.find('%', url.find('Acontent_owner_id_new.'))]
        id_post = url[url.find('mf_story_key')+len('mf_story_key.'):url.find('%')]

        comments = response.xpath('//div[@id="root"]/div/div[3]/div/div') 

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
                'html': str(self.flags_rep-1) + "rep"
            }       