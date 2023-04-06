import scrapy


class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    start_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/pc/filtered']

    def parse(self, response):
        self.log('Visited: ' + response.url)
        for table in response.css('table.clamp-list'):
            for game in table.css('td.clamp-summary-wrap'):
                detail_url = game.css('a.title::attr(href)').extract_first()
                if detail_url:
                    detail_url = response.urljoin(detail_url)
                    yield scrapy.Request(url=detail_url,callback=self.parseDetail)
                    yield scrapy.Request(url=(detail_url+'/critic-reviews'),callback=self.parse_critic_reviews)
                    yield scrapy.Request(url=(detail_url+'/user-reviews'),callback=self.parse_user_reviews)
                
        next_page = response.css('a[rel="next"]::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,callback=self.parse)

    def parseDetail(self, response):
        self.log('Visited: ' + response.url)
        details = response.css('div.summary_wrap')
        if response.xpath('//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div/span/text()').extract_first() != None:
            metascorepath = '//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div/span/text()'
        else:
            metascorepath = '//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[1]/div/div/a/div/span/text()'
        
        if response.xpath('normalize-space(//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/p/span[2]/a/span/text())').extract_first() != "":
            critic_amount_path = 'normalize-space(//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div[2]/p/span[2]/a/span/text())'
        else:
            critic_amount_path = 'normalize-space(//*[@id="main"]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/div[1]/div/div/div[2]/p/span[2]/a/span/text())'

        item = {
            'title':response.css('div.product_title h1::text').extract_first(),
            'metascore':response.xpath(metascorepath).extract_first(),
            'critic_amount':response.xpath(critic_amount_path).extract_first(),
            'userscore':details.css('div.metascore_w::text').extract_first(),
            'userrating_amount':response.css('div.details.side_details div.score_summary div.summary span.count a::text').extract_first()
            }
        
        yield item

    def parse_critic_reviews(self, response):
        for review in response.css('li.review.critic_review'):
            name_path = 'div.source a::text'
            if review.css(name_path).extract_first() == None:
                name_path = 'div.source::text'
            
            critic_reviews = {
                'game':response.css('div.product_title h1::text').extract_first(),
                'platform':response.css('div.product_title span a::text').extract_first().strip(),
                'critic_name':review.css(name_path).extract_first(),
                'grade':review.css('div.metascore_w::text').extract_first(),
                'review':review.css('div.review_body::text').extract_first().strip(),
                'date':review.css('div.date::text').extract_first()
            }
            yield critic_reviews

    def parse_user_reviews(self, response):
        for review in response.css('li.review.user_review'):
            name_path = 'div.name a::text'
            if review.css(name_path).extract_first().strip() == None or "":
                name_path = 'div.name::text'
            
            user_reviews = {
                'game':response.css('div.product_title h1::text').extract_first(),
                'platform':response.css('div.product_title span a::text').extract_first().strip(),
                'username':review.css(name_path).extract_first(),
                'grade':review.css('div.metascore_w::text').extract_first(),
                'review':review.css('div.review_body span::text').extract_first().strip(),
                'date':review.css('div.date::text').extract_first(),
                'thumbs_helpful':review.css('div.review_helpful span.total_ups::text').extract_first(),
                'thumbs_total':review.css('div.review_helpful span.total_thumbs::text').extract_first()
            }
            yield user_reviews
        
        next_user_review_page = response.css('a[rel="next"]::attr(href)').extract_first()
        if next_user_review_page:
            next_user_review_page = response.urljoin(next_user_review_page)
            yield scrapy.Request(url=next_user_review_page,callback=self.parse_user_reviews)