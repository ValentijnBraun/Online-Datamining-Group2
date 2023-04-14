# Some parts of this code are retrieved from ChatGPT(2023).
#import all libraries 
import scrapy
import re
# Define the spider: 'VGChartzspider' and create as a subclass of Scrapy.spider
class VgchartzspiderSpider(scrapy.Spider):
    name = 'VGChartzspider'
    allowed_domains = ['www.vgchartz.com']
    results_per_page = 400
    start_urls = [f'https://www.vgchartz.com/games/games.php?&results={results_per_page}']

    def parse(self, response):#Define a function for the parse method, which also processes the response from the website
        #Use XPath expression for returning a list of selectors. Where the first part selects all table cell elements, The second part limits the results to those that have the preceding attribute 'photo3'
        #the last part ensures that 'read the review' is not seen as a game title.
        for row in response.xpath('//td[preceding::*[@id="photo3"]]/a[not(contains(text(), "Read the review"))]'):
            game_url = row.xpath('@href').get()
            if game_url:
                yield scrapy.Request(url=response.urljoin(game_url), callback=self.parse_game_details,#download detail page where genre variables can be found and calls the function related to extracting the genre.  
                                     meta={'game_data': {#Create dictionary to save the scraped data afterwards.
                                         'game_title': row.xpath('normalize-space(.//text())').get(), #.encode('latin-1').decode('utf-8'),#clean game title
                                         'console': row.xpath('.//preceding::td[1]/div/a/div/img/@src').get(), #Using Xpath, the elements are selected from the HMTL tags and scraped. Thereby, the 'normalize-space' removes all extra spaces.
                                         'publisher': row.xpath('normalize-space(.//following::td[2]/text())').get(),#""
                                         'vgchartz_score': row.xpath('normalize-space(.//following::td[3]/text())').get(),#""
                                         'critic_score': row.xpath('normalize-space(.//following::td[4]/text())').get(),#""
                                         'user_score': row.xpath('normalize-space(.//following::td[5]/text())').get(),#""
                                         'total_shipped': row.xpath('normalize-space(.//following::td[6]/text())').get(),#""
                                         'release_date': row.xpath('normalize-space(.//following::td[7]/text())').get(),#""
                                         'last_update': row.xpath('normalize-space(.//following::td[8]/text())').get(),#""
                                     }})

        # The following code is applied so that scrapy scraped all pages from the website. The spider automatically closes if no next page is found.    
        current_page_number_match = re.search(r'page=(\d+)', response.url) #The page number is extracted by using the regular expression. 
        if current_page_number_match:
            current_page_number = int(current_page_number_match.group(1))
        else:
            current_page_number = 1

        next_page_number = current_page_number + 1

        if current_page_number_match:
            next_page_url = re.sub(r'page=\d+', f'page={next_page_number}', response.url)
        else:
            next_page_url = response.url + f'&page={next_page_number}'

        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)
 
#Scrape 'genre'from detail page
    def parse_game_details(self, response):
        game_data = response.meta['game_data']
        game_data['genre'] = response.xpath('//div[@id="gameGenInfoBox"]/h2[contains(text(), "Genre")]/following-sibling::p/text()').get()
        yield game_data



 
