# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class ShopeePipeline(object):
  def open_spider(self, spider):
    self.product_file = codecs.open('products.jl', 'w', encoding='utf-8')
    self.rating_file = codecs.open('rating.jl', 'w', encoding='utf-8')

  def close_spider(self, spider):
    self.product_file.close()
    self.rating_file.close()

  def process_item(self, item, spider):
    if 'product' in item.keys():
      line = json.dumps(dict(item), ensure_ascii=False) + "\n"
      self.product_file.write(line)
      return item
    if 'rating' in item.keys():
      line = json.dumps(dict(item), ensure_ascii=False) + "\n"
      self.rating_file.write(line)
      return item
