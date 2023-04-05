import scrapy


class ImdbgameSpider(scrapy.Spider):
    name = "imdbgame"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?title_type=video_game"]

    def parse(self, response):
        self.log("I Visited: " + response.url)

        games = response.css("div.lister-item-content")
        for game in games:
            item = {
                "Title": game.css("h3.lister-item-header>a::text").extract_first(),
                "Release Date": game.css("span.lister-item-year::text").extract_first()[1:5],
                "Rating": game.css("span.certificate::text").extract_first(),
                "Genres": game.css("div.lister-item-content > p:nth-child(2) > span.genre::text").extract_first(),
                "score": game.css('div.inline-block.ratings-imdb-rating > strong::text').getall(),
                "Summary": game.css("p.text-muted::text").getall(),
            }

            yield item

        next_page_url = response.css("div.desc > a::attr(href)").extract()[-1]
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
