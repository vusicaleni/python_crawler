import threading
from tkinter import END
from urllib.request import urlopen
from urllib.parse import urlparse
from get_links import GetLinks
from general import *


class Crawler:
    #class variables 
    END = '\n \n'
    folder_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()
    #initilize class functionality 
    def __init__(self, folder_name, base_url, domain_name):
        Crawler.folder_name = folder_name
        Crawler.base_url = base_url
        Crawler.domain_name = domain_name
        Crawler.queue_file = Crawler.folder_name + '/queue.txt'
        Crawler.crawled_file = Crawler.folder_name + '/crawled.txt'
        self.boot()
        self.crawl_page(Crawler.base_url)

    @staticmethod
    # Creates directory and files for project on first run and starts the spider
    def boot():
        create_project_dir(Crawler.folder_name)
        create_data_files(Crawler.folder_name, Crawler.base_url)
        Crawler.queue = file_to_set(Crawler.queue_file)
        Crawler.crawled = file_to_set(Crawler.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(base_url):
        if base_url not in Crawler.crawled:
            print( 'Crawling: ' + base_url + '\nOn thread: ' + threading.current_thread().name + '\n')
            print('Items in Queue ' + str(len(Crawler.queue)) + ' Vs Items Crawled  ' + str(len(Crawler.crawled)) + '\n')
            Crawler.add_links_to_queue(Crawler.gather_links(base_url))
            Crawler.queue.remove(base_url)
            Crawler.crawled.add(base_url)
            Crawler.update_files()
            print( ' -------------------------------------------------------------------------')

    # Get domain name (example.com)
    def get_domain_name(url):
        try:
            results = Crawler.get_sub_domain_name(url).split('.')
            return results[-2] + '.' + results[-1]
        except:
            return ''

    
    # Get sub domain name (name.example.com)
    def get_sub_domain_name(url):
        try:
            return urlparse(url).netloc
        except:
            return ''


    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(base_url):
        html_string = ''
        try:
            response = urlopen(base_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = GetLinks(Crawler.base_url, base_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Crawler.queue) or (url in Crawler.crawled):
                continue
            if Crawler.domain_name != Crawler.get_domain_name(url):
                continue
            Crawler.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Crawler.queue, Crawler.queue_file)
        set_to_file(Crawler.crawled, Crawler.crawled_file)
