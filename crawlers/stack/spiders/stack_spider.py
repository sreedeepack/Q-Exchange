from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com", "stackexchange.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=100&sort=new",
        "http://math.stackexchange.com/questions?pagesize=100&sort=new",
        "https://chemistry.stackexchange.com/questions?pagesize=10&sort=new"
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="question-summary"]')

        for question in questions:
            item = StackItem()

            item['title'] = question.css('.question-hyperlink').xpath('.//text()').extract()[0]
            item['url'] = question.css('.question-hyperlink').xpath('.//@href').extract()[0]

            item['votes'] = question.css('.vote-count-post').xpath('.//strong/text()').extract()[0]
            item['tags'] = question.css('.post-tag::text').extract()
            item['answers'] = question.css('.status').xpath('.//strong/text()').extract()[0]
            item['date'] = question.css('.relativetime').xpath('.//@title').extract()[0]
            # //TODO fetch text from question
            # item['question']
            yield item
