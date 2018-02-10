from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import SimpleQueue


import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

def load_url(url, timeout):
    return urllib.request.urlopen(url, timeout=timeout).read()

with ThreadPoolExecutor(max_workers=5) as executor:
    future_to_url = dict((executor.submit(load_url, url, 60), url)
                         for url in URLS)

    for future in executor.as_completed(future_to_url):
        url = future_to_url[future]
        if future.exception() is not None:
            print('%r generated an exception: %s' % (url,
                                                     future.exception()))
        else:
            print('%r page is %d bytes' % (url, len(future.result())))