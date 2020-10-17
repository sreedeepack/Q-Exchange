from scrapy.crawler import CrawlerProcess

from stack.spiders.reddit import RedditSpider
from stack.spiders.stack_all import SOSpider, UnixSpider, OtherSESpider

# run spider on cmd
# cmdline.execute("scrapy crawl stack".split())
# cmdline.execute("scrapy crawl reddit".split())

# Run all spiders
process = CrawlerProcess()
process.crawl(RedditSpider)
process.crawl(SOSpider)
process.crawl(UnixSpider)
process.crawl(OtherSESpider)
# the script will block here until all crawling jobs are finished
process.start()
