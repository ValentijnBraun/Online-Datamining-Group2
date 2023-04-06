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
        
        title_css = response.css('div.product_title h1::text').extract_first()
        title_xpath = response.xpath("//div[@class='product_title']//h1/text()").extract_first()
        if title_css != title_xpath:
            raise scrapy.exceptions.CloseSpider('STOPPING: Found different titles, CSS: {0}, Xpath: {1}'.format(title_css,title_xpath))
        
        metascore_css = response.css('a.metascore_anchor div.metascore_w span::text').extract_first()
        metascore_xpath = response.xpath("//div[@class='score_summary metascore_summary']//a[@class='metascore_anchor']//span/text()").extract_first()
        if metascore_css != metascore_xpath:
            raise scrapy.exceptions.CloseSpider('STOPPING: Found different metascores for {0}, CSS: {1}, Xpath: {2}'.format(title_css,metascore_css,metascore_xpath))

        userscore_css = response.css('div.summary_wrap div.metascore_w::text').extract_first()
        userscore_xpath = response.xpath("//a[@class='metascore_anchor']/div/text()").extract_first()
        if  userscore_css != userscore_xpath:
            raise scrapy.exceptions.CloseSpider('STOPPING: Found different user score for {0}, CSS: {1}, Xpath: {2}'.format(title_css,userscore_css,userscore_xpath))
        
        item = {
            'title':title_css,
            'metascore':metascore_css,
            'critic_amount':response.xpath("normalize-space(//div[@class='score_summary metascore_summary']//a/span/text())").extract_first(),
            'userscore':userscore_xpath,
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