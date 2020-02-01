# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import django 
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fsociety.settings'
django.setup()
from movie.models import Movie,Seed
class PianyuanPipeline(object):

    def process_item(self, item, spider):
        if spider.name == 'seed':
            s = Seed.objects.filter(filename=item['filename'])
            if not s:
                seed = Seed()
                seed.imdb = item['imdb']
                seed.filename = item['filename']
                seed.size = item['size']
                seed.quality = item['quality']
                seed.magnet = item['magnet']
                seed.save()

        else:
            m = Movie.objects.filter(imdb=item['imdb'])
            if not m:
                mv = Movie()
                mv.name = item['name']
                mv.name_en = item['name_en']
                mv.year = item['year']
                try:
                    mv.fullname = item['fullname']
                except:
                    mv.fullname = ''
                try:
                    mv.category = item['category']
                except:
                    mv.category = ''
                try:
                    mv.director = ','.join(item['director'])
                except:
                    mv.director = ''
                try:
                    mv.writer = ','.join(item['writer'])
                except:
                    mv.writer = ''
                mv.imdb = item['imdb']
                douban = item['douban'].replace('//movie.douban.com/subject/','')\
                    .replace('/','')
                mv.douban = douban
                mv.rating = item['rating']
                try:
                    mv.actor = ','.join(item['actor'])
                except:
                    mv.actor = ''
                mv.cover = item['images'][0]['path']
                if item['is_movie'] == 1:
                    mv.is_movie = True
                mv.url = item['url']
                mv.save()

        return item

