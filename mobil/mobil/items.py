# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MobilItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    transmission = scrapy.Field()
    capacity = scrapy.Field()
    fueltype = scrapy.Field()
    seat = scrapy.Field()
    price = scrapy.Field()