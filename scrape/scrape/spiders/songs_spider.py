import scrapy
import json
import re
import os
from googletrans import Translator

class SongsSpider(scrapy.Spider):
    name = 'songs'
    song_data = []

    def start_requests(self):
        url = 'https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page='

        for i in range(1,23):
            yield scrapy.Request(url=url+str(i), callback=self.parse)        

    def parse(self, response):
        for song in response.css('div.pt-cv-ifield'):
            yield scrapy.Request(url=song.css('h4.pt-cv-title a::attr(href)').get(), callback=self.retrieve)


    def retrieve(self, response):
        for song_details in response.css('body'):
            song_body = (song_details.xpath('//div[@class="entry-content"]//pre/text()').extract())
            song_body_split = []
            for parts in song_body:
                lines = parts.split('\n')
                for line in lines:
                    song_body_split.append(line)
            
            song = ''
            chords = ''

            for line in song_body_split:
                if(re.search('[a-zA-Z]', line)):
                    chords = chords + line + '\n'
                elif(len(line)!=0):
                    line = line.replace('+', '')
                    line = line.replace('|', '')
                    line.strip()
                    song = song + line + os.linesep


            translator = Translator()
            genre_list_en = list(set(song_details.css('span.entry-tags a::text').getall()))
            genre_list_si = []
            for g in genre_list_en:
                genre_list_si.append(translator.translate(g, src='en', dest='si').text)

            self.song_data.append({
                'title': song_details.css('div.entry-content span.sinTitle::text').get().strip(),
                'artist': translator.translate(song_details.css('span.entry-categories a::text').get(), src='en', dest='si').text,
                'genre': genre_list_si,
                'lyrics_by': translator.translate(song_details.css('span.lyrics a::text').get(), src='en', dest='si').text,
                'music': translator.translate(song_details.css('span.music a::text').get(), src='en', dest='si').text,
                'visits': song_details.css('div.tptn_counter::text').re(r'\d*[,]*\d+')[0],
                'lyrics': song.strip()
            })
            
            with open('songs.json', 'w', encoding='utf8') as out:
                json.dump(self.song_data, out, indent=4, ensure_ascii=False)


