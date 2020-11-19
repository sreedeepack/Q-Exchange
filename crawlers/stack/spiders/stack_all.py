from datetime import datetime

from stack.settings import OTHER_STACK_PAGES, STACKOVERFLOW_PAGES
from .stack_base import StackSpider

base_url = ("http://", ".com/questions?pagesize=50&sort=frequent")


class SOSpider(StackSpider):
    name = "stackoverflow"
    custom_settings = {
        'FEED_URI': f'temp/{name}_' + str(datetime.today()) + '.jsonl',
    }
    start_urls = [
        f"{base_url[0]}stackoverflow{base_url[1]}",
    ]
    # //TODO put pages in a config file and use that instead
    pages = STACKOVERFLOW_PAGES

    def __init__(self):
        super(SOSpider, self).__init__(start_urls=self.start_urls, pages=self.pages)


class UnixSpider(StackSpider):
    name = "unix"
    custom_settings = {
        'FEED_URI': f'temp/{name}_' + str(datetime.today()) + '.jsonl',
    }
    start_urls = [
        f"{base_url[0]}askubuntu{base_url[1]}",
        f"{base_url[0]}unix.stackexchange{base_url[1]}",
    ]
    pages = OTHER_STACK_PAGES

    def __init__(self):
        super(UnixSpider, self).__init__(start_urls=self.start_urls, pages=self.pages)


class OtherSESpider(StackSpider):
    name = "stack-other"
    custom_settings = {
        'FEED_URI': f'temp/{name}_' + str(datetime.today()) + '.jsonl',
    }
    start_urls = [
        f"{base_url[0]}math.stackexchange{base_url[1]}",
        f"{base_url[0]}chemistry.stackexchange{base_url[1]}",
        f"{base_url[0]}english.stackexchange{base_url[1]}",
    ]
    pages = OTHER_STACK_PAGES

    def __init__(self):
        super(OtherSESpider, self).__init__(start_urls=self.start_urls, pages=self.pages)
