from .stack_base import StackSpider

base_url = ("http://", ".com/questions?pagesize=50&sort=frequent")


class SOSpider(StackSpider):
    name = "stackoverflow"
    start_urls = [
        f"{base_url[0]}stackoverflow{base_url[1]}",
    ]
    # //TODO put pages in a config file and use that instead
    pages = 100

    def __init__(self):
        super(SOSpider, self).__init__(start_urls=self.start_urls, pages=self.pages)


class UnixSpider(StackSpider):
    name = "unix"
    start_urls = [
        f"{base_url[0]}askubuntu{base_url[1]}",
        f"{base_url[0]}unix.stackexchange{base_url[1]}",
    ]
    pages = 50

    def __init__(self):
        super(UnixSpider, self).__init__(start_urls=self.start_urls, pages=self.pages)


class OtherSESpider(StackSpider):
    name = "stack-other"
    start_urls = [
        f"{base_url[0]}math.stackexchange{base_url[1]}",
        f"{base_url[0]}chemistry.stackexchange{base_url[1]}",
        f"{base_url[0]}english.stackexchange{base_url[1]}",
    ]
    pages = 50

    def __init__(self):
        super(OtherSESpider, self).__init__(start_urls=self.start_urls, pages=self.pages)
