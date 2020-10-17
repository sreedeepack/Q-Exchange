import json
from datetime import datetime

import scrapy
from scrapy import Request

from stack.items import RedditItem


# noinspection SpellCheckingInspection
class RedditSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['reddit.com']
    # TODO add more subreddits
    subreddits = ["programming", "webdev", "softwaredevelopment"]
    # Using top.json(returns post as json) since reddit has anti-crawling measures in place
    start_urls = [f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=all" for subreddit in subreddits]

    # TODO get from settings/config file
    max_pages = 50
    curr_page = 0

    custom_settings = {
        'FEED_URI': f'temp/{name}_' + str(datetime.today()) + '.jl',
        'FEED_FORMAT': 'jsonlines',
        'FEED_EXPORTERS': {
            'jsonlines': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response, **kwargs):
        jsonresponse = json.loads(response.text)

        next_link = jsonresponse['data']['after']
        self.curr_page += 1
        if self.curr_page < self.max_pages:
            # visit next page
            next_link = response.urljoin(f"top.json?sort=top&t=all&after={next_link}")
            yield Request(next_link, callback=self.parse)

        # extract data from each post
        for post in jsonresponse['data']['children']:
            item = RedditItem()
            item["title"] = post["data"]['title']
            item["votes"] = post['data']['ups']
            item['comments'] = post['data']['num_comments']

            try:
                item['url'] = post['data']['permalink']
            except KeyError:
                item['url'] = post['data']['url']

            item['src'] = "reddit.com/r/" + post['data']['subreddit']

            item['date'] = datetime.fromtimestamp(post['data']['created']).isoformat()
            yield item
