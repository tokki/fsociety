import scrapy
from pianyuan.items import MovieItem, SeedItem
import re
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fsociety.settings'
django.setup()
from movie.models import Movie,Seed


class MovieSpider(scrapy.Spider):
    name = 'movie'
    domain = 'http://pianyuan.la'

    #start_urls = [ 'http://pianyuan.la/mv?p=1', ]

    def d_start_requests(self):
        pages = list(range(1, 10))
        pages.reverse()
        urls = ['http://pianyuan.la/mv?p=' + str(p) for p in pages]
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def start_requests(self):
        movies = Movie.objects.all()
        name = []
        fname = []
        for mv in movies:
            if float(mv.rating) > 8.0:
                if not re.search('[a-zA-Z(),]',mv.director):
                    name.append(mv.director)
        for n in name:
            if n not in fname:
                fname.append(n)

        urls = ['http://pianyuan.la/search?q='+n for n in fname]
        for url in urls:
            yield scrapy.Request(url,self.parse_search)


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
        tt = response.css('div.masthead h1::text').get()
        tt = tt.replace('\n', '')
        tt = tt.strip()
        tt = tt.split('  ')
        mv['name'] = tt[0]
        mv['name_en'] = tt[1]
        year = tt[2]
        mv['year'] = year[1:-1]
        dt = response.css('div.minfo ul.detail')
        for li in dt.css('li'):
            text = li.css('strong::text').get().replace(':', '')
            if text == '又名':
                mv['fullname'] = li.css('div::text').get().strip()
            if text == '地区':
                mv['country'] = li.css('div::text').get().strip()
            if text == '类型':
                mv['category'] = li.css('div::text').get().strip()
            if text == '导演':
                mv['director'] = li.css('div a::text').getall()
            if text == '编剧':
                mv['writer'] = li.css('div a::text').getall()
            if text == '主演':
                mv['actor'] = li.css('div a::text').getall()
            if text == 'imdb':
                mv['imdb'] = li.css('div a::text').get()
            if text == '豆瓣':
                mv['douban'] = li.css('div a::attr(href)').get()

        src = response.css('div.minfo div.litpic img::attr(src)').get()
        mv['image_urls'] = [self.domain + src]
        url = response.css('div.minfo div.litpic a::attr(href)').get()
        mv['url'] = url

        is_movie = response.css('div.rtitle h1 small.label-info')  
        if len(is_movie) == 0:
            mv['is_movie'] = 1
        else:
            mv['is_movie'] = 0

        mv['rating'] = response.css('div.minfo div.score i.sum b::text').get() \
            + response.css('div.minfo div.score i.sum::text').get()
        yield mv
