from urllib import parse
from html.parser import HTMLParser
from pathlib import Path


class GetLinks(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    #use this function when we  encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                #insure correct attribute 
                if attribute == 'href':
                    #used to crawl links without a suffix to avoid a get request 
                    if not Path('a').suffix:
                        url = parse.urljoin(self.base_url, value)
                        self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
