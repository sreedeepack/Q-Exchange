# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field


class StackItem(scrapy.Item):
    """For stackoverflow and other stack-exchange websites"""
    title = Field()
    desc = Field()
    url = Field()
    votes = Field()
    views = Field()
    answers = Field()
    tags = Field()
    date = Field()
    src = Field()
