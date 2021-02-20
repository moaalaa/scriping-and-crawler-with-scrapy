from typing import List

import scrapy


class PostsSpider(scrapy.Spider):
    name = "posts"
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response: scrapy.http.Response):
        # Get Posts Container
        posts: List[scrapy.http.TextResponse] = response.css('div.oxy-post')
        
        for post in posts:
            yield {
                'title': post.css('div.oxy-post-wrap a.oxy-post-title::text').get().strip(),
                'date': post.css('a.oxy-post-image div.oxy-post-image-date-overlay::text').get().strip(),
                'author': post.css('div.oxy-post-wrap div.oxy-post-meta-author::text').get().strip(),
            }
        
        next_page = response.css('div.oxy-easy-posts-pages a.next.page-numbers::attr(href)').get()
    
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
            
        
