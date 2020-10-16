from scrapy import Spider, Request
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com", "stackexchange.com", "askubuntu.com"]

    def __init__(self, start_urls=None, pages=50, **kwargs):
        super().__init__(**kwargs)
        self.pages = pages
        self.start_urls = start_urls
        if start_urls is None:
            self.start_urls = [
                "http://stackoverflow.com/questions?pagesize=50&sort=frequent",
                "http://math.stackexchange.com/questions?pagesize=50&sort=frequent",
                "https://chemistry.stackexchange.com/questions?pagesize=50&sort=frequent",
                "http://askubuntu.com/questions?pagesize=50&sort=frequent",
            ]

    def parse(self, response, **kwargs):
        next_urls = [f'{response.url} + &page={i}' for i in range(1, self.pages + 1)]
        for next_url in next_urls:
            yield Request(next_url, callback=self.parse_stack)

    def parse_stack(self, response):
        """

        @rtype: object
        """
        questions = Selector(response).xpath('//div[@class="question-summary"]')

        for question in questions:
            item = StackItem()
            item['src'] = response.urljoin('/')
            item['title'] = question.css('.question-hyperlink').xpath('.//text()').extract()[0]

            # url(src without trailing /) + relative link to question
            item['url'] = item['src'][:-1] + question.css('.question-hyperlink').xpath('.//@href').extract()[0]

            item['votes'] = question.css('.vote-count-post').xpath('.//strong/text()').extract()[0]
            item['tags'] = question.css('.post-tag::text').extract()
            item['answers'] = question.css('.status').xpath('.//strong/text()').extract()[0]
            try:
                item['date'] = question.css('.relativetime').xpath('.//@title').extract()[0]
            except IndexError:
                # Posts can become community owned and hence post date is removed
                item['date'] = 'NA'

            # Fetch question description from link to question
            request = Request(item['url'], callback=self.parse_answer_page)
            request.meta['item'] = item
            request.meta['link'] = item['src']
            request.meta['new_link'] = item['url']
            # generator for requests, the callback function parse_answer_page
            # will return the actual item
            yield request

    def parse_answer_page(self, response):
        """
        @rtype: string
        """
        # get item fields from parse_stack()
        item = response.meta['item']

        # ignores <code/> tag and contents
        sel = Selector(response)
        desc = sel.css('.s-prose').xpath('.//p/text()').extract()
        desc = ' '.join(desc)
        item['desc'] = desc

        yield item
