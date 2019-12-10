# short intro

It's a proxy pool builder (using google currently)\
inspired by and modified from: [peterinhouse123's Proxy_Pool](https://github.com/peterinhouse123/Proxy_Pool.git)

# prerequisite

You need a random free proxy which you can find anywhere
the crawler will search txt files on google base on your given proxy

warning: the actual useful proxy in the proxy pool may be very rare

# how to use:

'''
from Proxy_Pool_Builder.Google_proxy_crawler import Google_proxy_crawler

proxy_crawler = Google_proxy_crawler()
proxy_crawler.build_proxy_pool(new_pool=True)
'''
