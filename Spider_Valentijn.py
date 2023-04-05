import scrapy

class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    start_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page=0']

    def parse(self, response):
        self.log('Visited: ' + response.url)
        for table in response.css('table.clamp-list'):
            for game in table.css('td.clamp-summary-wrap'):
                item = {
                'title':game.css('a.title::attr(href)').extract_first(),
                'metascore':game.css('div.metascore_w::text').extract_first(),
                'userscore':game.css('div.metascore_w::text')[2].extract()
                }
                yield item
        next_page = response.css('a[rel="next"]::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,callback=self.parse)