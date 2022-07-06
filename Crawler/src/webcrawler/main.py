import threading
from queue import Queue
from crawler import Crawler
from general import *

#INITIALIZATION OF VARIABLES
BASE_URL = 'https://rescale.com'
DOMAIN_NAME = Crawler.get_domain_name(BASE_URL)
FOLDER_NAME = 'rescale'
QUEUE_FILE = FOLDER_NAME + '/queue.txt'
CRAWLED_FILE = FOLDER_NAME + '/crawled.txt'
# my computer has 16 logical processers as such I set my threads to 16, for an older computer this may need to be adjsuted 8
NUMBER_OF_THREADS = 16
queue = Queue()
Crawler(FOLDER_NAME, BASE_URL, DOMAIN_NAME)


def initialize_program():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Crawler.crawl_page(url)
        queue.task_done()


# Each queued link is used as a new task 
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        create_jobs()


initialize_program()
crawl()
