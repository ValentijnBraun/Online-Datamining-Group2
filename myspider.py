# Some parts of this code are retrieved from ChatGPT(2023)
#import important library
import scrapy
# Define the spider: 'MetacriticSpider' and create as a subclass of Scrapy.spider
class MetacriticSpider(scrapy.Spider):
    name = 'metacritic'
    start_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered'] #Define the web page URL that the spider can start scrapping from.

    def parse(self, response):#Define a function for the parse method, which also processes the response from the website
        for game in response.css('td.clamp-summary-wrap'):#Use CSS expression for returning a list of selectors.
            #Using CSS, the elements are selected from the HMTL tags and scraped. Thereby, the 'strip' method removes all extra white spaces. 
            title = game.css('a.title h3::text').get(),
            metascore = game.css('div.metascore_w::text').get(),
            userscore = game.css('div.metascore_w.user.large.game::text').get(),
            platform = game.css('div.platform span.data::text').get().strip()
            summary = game.css('div.summary::text').get().strip()
            # creates a dictionary          
            yield {
                'title': title,
                'metascore': metascore,
                'userscore': userscore,
                'platform': platform,
                'summary' : summary,
                             
            }
        #code for pagination
        next_page = response.css('span.flipper.next a::attr(href)').get() #Tries to find the link to the next page.
        if next_page is not None:#checks if there is a next page. If not the value will be none.
            yield response.follow(next_page, self.parse)
    
