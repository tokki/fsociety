import scrapy
from pianyuan.items import MovieItem, SeedItem
import re
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fsociety.settings'
django.setup()
from movie.models import Movie,Seed


class MovieSpider(scrapy.Spider):
    name = 'seed'
    domain = 'http://pianyuan.la'

    def d_start_requests(self):
        pages = list(range(1, 10))
        pages.reverse()
        urls = ['http://pianyuan.la/mv?p=' + str(p) for p in pages]
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def start_requests(self):
        movies = Movie.objects.exclude(url='')

        urls = ['http://pianyuan.la'+m.url for m in movies]

        for url in urls:
            yield scrapy.Request(url,self.parse_movie)


    def parse_search(self,response):
        urls = response.css('div.minfo div.litpic a::attr(href)').getall()
        for url in urls:
            yield scrapy.Request('http://pianyuan.la'+url,self.parse_movie)



    def parse(self, response):
        for mv in response.css('div.mone.prel'):
            movie_url = self.domain + mv.css('a::attr(href)').get()
            yield scrapy.Request(url=movie_url, callback=self.parse_movie)

    def parse_movie(self, response):
        mv = MovieItem()
        dt = response.css('div.minfo ul.detail')
        for li in dt.css('li'):
            text = li.css('strong::text').get().replace(':', '')
            if text == 'imdb':
                mv['imdb'] = li.css('div a::text').get()

        for seed in response.css(
                'div.related.allres table td a::attr(href)').getall():
            seed_url = self.domain + seed
            yield scrapy.Request(url=seed_url,
                                 callback=self.parse_seed,
                                 meta={'imdb': mv['imdb']})

    def parse_seed(self, response):
        imdb = response.meta['imdb']
        seed = SeedItem()
        seed['imdb'] = imdb
        filename = response.css('div.masthead h1::text').get()
        seed['filename'] = filename
        moreinfo = response.css('div.rinfo ul li::text').getall()
        seed['size'] = moreinfo[1]
        seed['quality'] = moreinfo[0]
        seed['magnet'] = response.css(
            'div.tdown a.btn-primary::attr(href)').get()
        yield seed
