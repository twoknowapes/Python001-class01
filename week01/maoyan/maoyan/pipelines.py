# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MaoyanPipeline:
    def process_item(self, item, spider):
        movie_title = item['movie_title']
        movie_type = item['movie_type']
        movie_date = item['movie_date']
        with open('./movies.csv', 'a+', encoding='utf-8') as f:
            output = f'{movie_title}\t{movie_type}\t{movie_date}\n\n'
            f.write(output)
        return item
