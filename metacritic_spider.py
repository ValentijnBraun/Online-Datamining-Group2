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
