# from pyquery import PyQuery as pq
from .utils import net_fn, Proxy_Reader
import json
import time
from bs4 import BeautifulSoup


class Google_proxy_crawler:
    # you'll need a random free proxy as your search_word e.g. 47.90.63.202 188.166.204.196
    def __init__(self, search_word="76.250.137.241", engine='Google'):
        self.Net = net_fn.Net()
        self.search_word = search_word
        self.engine = engine

    def Search_Page(self, keyword, page_num):
        if self.engine == 'Google':
            url = "https://www.google.com/search?q={}&start={}".format(
                keyword, page_num*10)
        if self.engine == 'Bing':
            url = "https://www.bing.com/search?q={}&first={}".format(
                keyword, page_num*10)
        rs = self.Net.Get(url)
        end = []
        try:
            soup = BeautifulSoup(rs.text, "html.parser")
        except:
            return []
        # wtf ? can't get the same html as inspect
        for searchWrapper in soup.find_all('div', {'class': 'BNeawe UPmit AP7Wnd'}):
            url = searchWrapper.parent["href"]
            url = self.Net.preg_get_word("\?q=(.+)&sa=", 1, url)
            if url == "empty_data":
                continue
            end.append(url)
        return end

    def Search(self, keyword, max_page_num):
        end = []

        for n in range(max_page_num):
            page_rs = self.Search_Page(keyword=keyword, page_num=n)
            for link in page_rs:
                end.append(link)
        return end

    def build_proxy_pool(self, new_pool=True, max_page_num=10):
        if new_pool:
            print('searching on ' + self.engine + '...')
            proxy_source_list = self.Search(keyword=self.search_word + " filetype:txt",
                                            max_page_num=max_page_num)
        else:
            proxy_source_list = ['http://proxy.tgmember.com/1~6_2019/02-Apr-2019/04%253A35.txt', 'http://proxy.tgmember.com/24-Jun-2019/22%253A45.txt', 'http://iegalizer.info/1564729063_proxies.txt', 'https://pan.cccyun.cc/down.php/45811555cfdb2c11750bfc72c275413b.txt', 'https://webanetlabs.net/freeproxyweb/proxylist_at_17.06.2019.txt', 'https://webanetlabs.net/freeproxyweb/proxylist_at_23.01.2019.txt', 'http://www.marketplace-dl.space/proxies.txt', 'https://mainware.tk/o/p.txt', 'https://cyber-hub.net/proxy/http.txt', 'http://www.bjhwxq.com/http.txt', 'https://cdn-23.anonfile.com/q0Q7b1T8m1/43529e1d-1567187596/8954x%2BProxies.txt', 'https://cdn-23.anonfile.com/J31c5cX6m1/5967900c-1567339105/proxies.txt', 'http://rungthaoduoc.com/file/17k%2520hq%2520Fast%2520http%2520proxy%2520by%2520HS.txt', 'https://admcomp.ru/downloads/proxyold.txt', 'http://www.shadowpvp.eu/api/proxychecker/scan.txt', 'https://onehack.us/uploads/short-url/pOijZyw3LafbNUPTpMosDJXCktx.txt', 'https://chteam.ir/Proxy-List-New-400K.txt', 'https://resolv3.me/proxies/https.txt', 'http://instagrambypass.com/bot/ip/proxy/prxt5656398.txt',
                                 'http://instagrambypass.com/bot/ip/proxy/prxt5649801.txt', 'http://075000.xyz/proxy/tmd.txt', 'http://111.67.201.164/2.txt']
        proxy_Reader = Proxy_Reader.Proxy_Reader(
            proxy_source_list, self.search_word)
        Right_List, dumpdir = proxy_Reader.Check_Dump_List(proxy_source_list)
        print('a proxy pool has been built from the following sites\n', Right_List)
        print('='*30)
        print('please check out ' + dumpdir)


if __name__ == "__main__":
    # new_txt = 0
    # search_word = "188.166.204.196"
    # if new_txt:
    #     Google_spider = Google()
    #     #test
    #     proxy_source_list = Google_spider.Search(keyword = search_word + " filetype:txt",
    #                                             max_page_num=10) # 这里是从free ip pool 这个中随便找一个，在google上搜索txt
    # else:
    #     proxy_source_list = ['http://proxy.tgmember.com/1~6_2019/02-Apr-2019/04%253A35.txt', 'http://proxy.tgmember.com/24-Jun-2019/22%253A45.txt', 'http://iegalizer.info/1564729063_proxies.txt', 'https://pan.cccyun.cc/down.php/45811555cfdb2c11750bfc72c275413b.txt', 'https://webanetlabs.net/freeproxyweb/proxylist_at_17.06.2019.txt', 'https://webanetlabs.net/freeproxyweb/proxylist_at_23.01.2019.txt', 'http://www.marketplace-dl.space/proxies.txt', 'https://mainware.tk/o/p.txt', 'https://cyber-hub.net/proxy/http.txt', 'http://www.bjhwxq.com/http.txt', 'https://cdn-23.anonfile.com/q0Q7b1T8m1/43529e1d-1567187596/8954x%2BProxies.txt', 'https://cdn-23.anonfile.com/J31c5cX6m1/5967900c-1567339105/proxies.txt', 'http://rungthaoduoc.com/file/17k%2520hq%2520Fast%2520http%2520proxy%2520by%2520HS.txt', 'https://admcomp.ru/downloads/proxyold.txt', 'http://www.shadowpvp.eu/api/proxychecker/scan.txt', 'https://onehack.us/uploads/short-url/pOijZyw3LafbNUPTpMosDJXCktx.txt', 'https://chteam.ir/Proxy-List-New-400K.txt', 'https://resolv3.me/proxies/https.txt', 'http://instagrambypass.com/bot/ip/proxy/prxt5656398.txt',
    #                          'http://instagrambypass.com/bot/ip/proxy/prxt5649801.txt', 'http://075000.xyz/proxy/tmd.txt', 'http://111.67.201.164/2.txt']

    # txt_Reader = Proxy_Read.Proxy_Read(proxy_source_list, search_word)
    # Right_List = txt_Reader.Check_List_Proxy_Stat(proxy_source_list)
    # print(Right_List)
    pass
