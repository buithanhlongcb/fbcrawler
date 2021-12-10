import scrapy
from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json

class FbPostSpider(Spider):
    
    name = "post"
    allowed_domains = ['facebook.com']
    unique_data = []
    flag = 0
    custom_settings = {
        'DUPEFILTER_CLASS' : 'scrapy.dupefilters.BaseDupeFilter'
    }

    def start_requests(self):
        post_url = self.post_url

        if post_url.find('photos') != -1:
            post_id = post_url.partition("photos/")[2].rstrip('/')
            page_id = post_id.partition("/")[0].lstrip("a.")
            post_id = post_id.partition("/")[2]
        else: 
            post_id = post_url.partition("posts/")[2].rstrip("/")
            page_id = post_url.partition("posts/")[0].partition("facebook.com/")[2]

        url = f"https://mbasic.facebook.com/story.php?story_fbid={post_id}&id={page_id}"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        filename=f"home{self.flag}.html"
        self.flag += 1
        with open(filename, 'wb') as f:
            f.write(response.body)

        if response.xpath('//div[@id="MPhotoContent"]') == []:
            comments = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div/div')
            next_id_comment = response.xpath('//div[@id="root"]/div[2]/div[2]/div/div[2]/div[contains(@id,"see_next")]/a/@href').extract()

        else:
            comments = response.xpath('//div[@id="MPhotoContent"]/div[2]/div/div/div[3]/div/div')
            next_id_comment = response.xpath('//div[@id="MPhotoContent"]/div[2]/div/div/div[3]/div[contains(@id,"see_next")]/a/@href').extract()


        for reply in comments:
    
            #Check if it was a reply or not
            reply_check = reply.xpath('./div[4]/div/div')
            
            if reply_check != []:
                href = reply_check.xpath('./a/@href').extract_first()
                
                reply_url = "https://mbasic.facebook.com/" + href
                
                yield scrapy.Request(reply_url,
                                    callback = self.parse_reply,
                                    meta = {
                                        'url': reply_url
                                    })
            else:
                # Regular comment
                
                user = reply.xpath('./h3/a/text()').extract()
                tags = reply.xpath('./div[1]/a/text()').extract()
                content = reply.xpath('./div[1]/text()').extract()
                
                check = [user, 'None', content, tags]
                if check not in self.unique_data:
                    self.unique_data.append(check)

                    yield {
                        'User': user,
                        'Reply to': 'None',
                        'Comment': content,
                        'Tag': tags,
                    }  
                
        
        next_url =''
        #print('11111111111111111111', next_id_comment)
        if next_id_comment != []:
            next_url = 'http://mbasic.facebook.com' + next_id_comment[0]
            yield response.follow(next_url, self.parse)      

    def parse_reply(self, response):
        #Parse root comment
        root = response.xpath('//div[contains(@id,"root")]/div/div/div[count(@id)!=1 and contains("0123456789", substring(@id,1,1))]')
        root_user = root.xpath('./h3/a/text()').extract()
        content = root.xpath('./div[1]/text()').extract()
        tags = root.xpath('./div[1]/a/text()').extract()

        check = [root_user, 'None', content, tags]
        if check not in self.unique_data:
            self.unique_data.append(check)
            yield {
                'User': root_user,
                'Reply to': 'None',
                'Comment': content,
                'Tag': tags,
            }

        #Parse the rest
        for reply in response.xpath('//div[contains(@id,"root")]/div/div/div[count(@id)=1 and contains("0123456789", substring(@id,1,1))]'):
            user = reply.xpath('./div/h3/a/text()').extract()
            content = reply.xpath('./div/div[1]/text()').extract()
            tags = reply.xpath('./div/div[1]/a/text()').extract()
            
            check = [user, root_user, content, tags]
            if check not in self.unique_data:
                self.unique_data.append(check)
                yield {
                    'User': user,
                    'Reply to': root_user,
                    'Comment': content,
                    'Tag': tags,
                }

        next_id_comment = response.xpath('//div[contains(@id,"comment_replies_more_1")]/a/@href').extract()
        #print('222222222222222222222222', next_id_comment)
        if next_id_comment != []:
            next_url = 'http://mbasic.facebook.com' + next_id_comment[-1]
            yield response.follow(next_url, self.parse_reply) 