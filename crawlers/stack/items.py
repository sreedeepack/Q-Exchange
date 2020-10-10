# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class StackItem(scrapy.Item):
    """For stackoverflow"""
    title = Field()
    url = Field()
    votes = Field()
    views = Field()
    answers = Field()
    tags = Field()
    date = Field()


class UbuntuItem(scrapy.Item):
    """For AskUbuntu"""
    name = scrapy.Field()
    pass
