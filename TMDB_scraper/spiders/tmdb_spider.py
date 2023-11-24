# to run 
# scrapy crawl tmdb_spider -o movies.csv

#import necessary packages
import scrapy
import requests
import random

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider' #defines the name of the spider that can be called in the terminal
    start_urls = ['https://www.themoviedb.org/movie/346698-barbie/'] #Beginning url for the Barbie Movie
    user_agent = "something something" #Helps avoid a 403 error
    
    def parse(self,response):
        """
        starts at the main page of the Barbie movie, 
        navigates to the Full Cast & Crew Page,
        and then calls parse_full_credits(self, response) on the credits page
        does not return any data
        """
        cast_page_url = response.url + "/cast"
        yield scrapy.Request(cast_page_url, callback = self.parse_full_credits)
        
    def parse_full_credits(self, response):
        '''
        parses the Full Cast & Credits Page
        this parsing method extracts links to individual actors' pages,
        navigates to each link that contains 'person/',
        and then calls parse_actor_page(self, response) on each actor's page
        does not return any data
        '''
        for cast in response.css("div.content_wrapper.false > section.panel:first-of-type a::attr(href)").getall():
            if "/person/" in cast:
                yield response.follow(cast, callback=self.parse_actor_page)

    
    def parse_actor_page(self,response):
        '''
        parses individual actor's pages to extract movie and tv show credits
        extracts actor's name,
        iterates through listed credits on the actors page
        yields a dictionary containing the actor's name and the movie/tv show title
        '''
        actor_name = response.css("h2.title a::text").get()
        for movie_name in response.css("div.credits_list > table.card.credits:first-of-type a.tooltip bdi::text").getall():
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_name}