# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from shopee.utils.uri_builders.category_index_api_uri_builder import CategoryIndexApiUriBuilder
from shopee.utils.uri_builders.item_api_uri_builder import ItemApiUriBuilder
from shopee.utils.uri_builders.rating_api_uri_builder import RatingApiUriBuilder
from shopee.utils.info_extractors.extract_items_from_category import ExtractItemsFromCategory
from shopee.helpers.pagination_helper import PaginationHelper
from scrapy.shell import inspect_response
import json


class ThoiTrangNamSpider(scrapy.Spider,
                         CategoryIndexApiUriBuilder,
                         ItemApiUriBuilder,
                         ExtractItemsFromCategory,
                         PaginationHelper):
    name = 'thoi_trang_nam'
    allowed_domains = ['shopee.vn']

    start_urls = [
        'https://shopee.vn/api/v2/search_items/',
    ]

    def start_requests(self):
        for i in range(1, 100):
            category_index_page_uri = CategoryIndexApiUriBuilder(
                by='pop',
                limit='50',
                match_id='77',
                newest='{}'.format(i*50),
                order='desc',
                page_type='search',
            ).build_category_index_api_uri()
            yield Request(url=self.start_urls[0] + category_index_page_uri, callback=self.parse_category_index)

    def parse_category_index(self, response):
        category_json_data = json.loads(response.text)
        items_info = [ExtractItemsFromCategory(item).extract() for
                      item in category_json_data.get("items")]
        for item_info in items_info:
            item_uri = ItemApiUriBuilder(**item_info).build_item_api_uri()
            yield scrapy.Request(url="https://shopee.vn/api/v2/item/get" + item_uri,
                                 callback=self.parse_item_info)

    def parse_item_info(self, response):
        product_json_data = json.loads(response.text)
        item_id = product_json_data.get("item").get("itemid")
        shop_id = product_json_data.get("item").get("shopid")
        cmt_count = product_json_data.get("item").get("cmt_count")
        pagination_list = PaginationHelper(cmt_count, 50).create_paginatation_list()
        for page in pagination_list:
          limit = page.get("limit")
          offset = page.get("offset")
          rating_uri = RatingApiUriBuilder(
              itemid=item_id,
              shopid= shop_id,
              filter= 0,
              flag= 1,
              type= 0,
              limit = limit,
              offset = offset,
              ).build_rating_api_uri()
          yield scrapy.Request(url="https://shopee.vn/api/v2/item/get_ratings"+rating_uri, 
            callback=self.parse_rating_info)

        yield {
          'product': product_json_data
        }

    def parse_rating_info(self, response):
        rating_json_data = json.loads(response.text)
        yield {
            "rating": rating_json_data 
        }
