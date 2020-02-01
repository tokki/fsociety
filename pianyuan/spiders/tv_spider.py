import scrapy
from pianyuan.items import MovieItem, SeedItem
import re


class TvSpider(scrapy.Spider):
    name = 'tv'
    domain = 'http://pianyuan.la'

    #start_urls = ['http://pianyuan.la/tv?p=1',]

    def start_requests(self):
        pages = list(range(1, 85))
        pages.reverse()
        urls = ['http://pianyuan.la/tv?p=' + str(p) for p in pages]
        for url in urls:
            yield scrapy.Request(url, self.parse)

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

        mv['rating'] = response.css('div.minfo div.score i.sum b::text').get() \
            + response.css('div.minfo div.score i.sum::text').get()

        is_movie = response.css('div.rtitle h1 small.label-info')  
        if len(is_movie) == 0:
            mv['is_movie'] = 1
        else:
            mv['is_movie'] = 0


        yield mv
