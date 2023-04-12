# import Scrapy module

import scrapy 

# define the spider class
class imdbgamescraper(scrapy.Spider):

    # define the spider name, allowed domains, and starting URLs

    name = "imdbgamescraper"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?title_type=video_game"]

    # define the parse function to extract data from the pages
    def parse(self, response):
        # log the URL of the page being visited
        self.log("I Have Visited : " + response.url)
        games = response.css("div.lister-item-content")
        
        for game in games:
            # extract the details of each game using CSS selectors
            detailed_url = game.css("h3.lister-item-header>a::attr(href)").get()

            # if the detailed URL exists, join the URL and make a request to parse the details
            if detailed_url:
                detailed_url = response.urljoin(detailed_url)
                detailed_url = detailed_url 
                yield scrapy.Request(url= detailed_url,callback=self.parsedetails)

        # extract the next page URL and make a request to parse the details
        next_page = response.css("div.desc > a::attr(href)").getall()[-1]
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page,callback=self.parse)

    # define the parsedetails function to extract details from each game's page
    def parsedetails(self, response):

        # extract data from each game's page using CSS and xpath selectors
        
        # Get the game title.
        Title = response.css("span.sc-afe43def-1.fDTGTb::text").get(),
        # Get the game Released Date using css and xpath.
        Released_Date = response.css("div.sc-385ac629-3.kRUqXl > div.sc-52d569c6-0.kNzJA-D > ul > li:nth-child(2) > a::text").get(),
        Released_Date_Xpath = response.xpath("//div[1]/ul/li[2]/a/text()").get(),        # Get the game title.
        # Get the game score.
        Score=response.css(" div.sc-bde20123-2.gYgHoj > span.sc-bde20123-1.iZlgcd::text").get(),
        # Get the game Rating using xpath.
        Rating = response.xpath('//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]/a/text()').get(),
        # Get the game Director.
        Director = response.css("div.ipc-metadata-list-item__content-container > ul > li > a::text").get(),
        # Get the game cast.
        Star_1 = response.css("li.ipc-metadata-list__item.ipc-metadata-list-item--link > div > ul > li:nth-child(1) > a::text").getall()[0],
        Star_2 = response.css("li.ipc-metadata-list__item.ipc-metadata-list-item--link > div > ul > li:nth-child(1) > a::text").getall()[1],
        # Get the game's developer studio.
        studio = response.css("li.ipc-metadata-list__item.ipc-metadata-list-item--link > div > ul > li:nth-child(1) > a::text").getall()[-1],
        # Get the game studios's Location.
        Locaton = response.css("li.ipc-metadata-list__item.ipc-metadata-list-item--link > div > ul > li:nth-child(1) > a::text").getall()[-2],

        # Putting the data into a dictionary
        items = {
            "Title"  :Title,
            "Released_Date" :Released_Date,
            "Released_Date_Xpath":Released_Date_Xpath,
            "Score":Score,
            "Rating":Rating,
            "Director":Director,
            "Star_1" :Star_1,
            "Star_2":Star_2,
            "studio":studio,
            "Locaton" :Locaton,
            }
        
        # 
        yield items