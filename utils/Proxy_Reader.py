# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
from . import net_fn
import json
import urllib3
import time
import datetime
from tqdm import tqdm
from threading import Thread
from queue import Queue


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.TimeoutError)
urllib3.disable_warnings(urllib3.exceptions.MaxRetryError)

time_stamp = datetime.datetime.now().strftime("%Y-%m-%d")


class Proxy_Reader:
    def __init__(self, Source_List, search_word):
        self.Net = net_fn.Net()
        self.Thread_Check_Max = 500
        self.All_Check_List = dict()
        self.Source_List = Source_List
        self.Proxy_Queue = Queue()
        self.Init_Proxy_Test_Thread()
        self.OK_List = []
        self.search_word = search_word

    def Init_Proxy_Test_Thread(self):

        for x in tqdm(range(self.Thread_Check_Max), desc="正在初始化 - 檢測線程"):
            t = Thread(target=self.Proxy_Test_fn)
            t.start()

        print("初始化檢測線程建立完畢")

    def Proxy_Test_fn(self):
        # while 1:
            # if self.Proxy_Queue.qsize() > 0:
        while self.Proxy_Queue.qsize() > 0:
            proxy_data = self.Proxy_Queue.get()
            stat = self.Proxy_Test_Unit(proxy_ip=proxy_data)
            if stat == True:
                self.OK_List.append(proxy_data)
            time.sleep(0.2)

    def Proxy_Test_Unit(self, proxy_ip):
        test_url = "https://www.google.com/"
        try:
            rs = self.Net.Get(url=test_url, proxy_ip=proxy_ip, timeout=7)

            return True
        except Exception as e:
            print(e)
            return False

    def Get_Page_Proxy(self, url):
        rs = self.Net.Get(url)
        data = rs.content.decode()
        proxy_list = self.Net.preg_get_word(
            "(\d+\.\d+\.\d+\.\d+:\d+)", 'all', data)
        return proxy_list

    def Check_Dump_Page(self, url, dumpdir, dump=True):
        rs_stat = None
        try:
            rs = self.Net.Get(url, timeout=10)
            data = rs.content.decode(errors='ignore')
        except Exception:
            rs_stat = False

        if rs_stat == None:
            proxy_list = self.Net.preg_get_word(
                "(\d+\.\d+\.\d+\.\d+:\d+)", 'all', data)
            if len(proxy_list) == 0 or proxy_list == "empty_data":
                rs_stat = False
            else:
                rs_stat = True
        if dump and rs_stat:
            # with open('./math_term_spider/proxy_pool/data/' + self.search_word + '.json', 'a') as pool_data:
            with open(dumpdir + '/' + self.search_word + '_' + time_stamp + '.json', 'w') as pool_data:
                write_data = '\n'.join(proxy_list) + '\n'
                pool_data.write(write_data)

        if url in self.All_Check_List:
            self.All_Check_List[url] = rs_stat

        return rs_stat

    def Check_Dump_List(self, dump=True, dumpdir='Proxy_Pool_Builder/proxy_data'):

        Thread_list = []
        for source_link in self.Source_List:
            self.All_Check_List[source_link] = False

            t = Thread(target=self.Check_Dump_Page,
                       args=[source_link, dumpdir])
            Thread_list.append(t)
            t.start()
        for tc in tqdm(Thread_list, desc="checking proxy list sources"):
            tc.join()
        Right_List = []
        for url in self.All_Check_List:
            stat = self.All_Check_List[url]
            if stat == True:
                Right_List.append(url)
        return Right_List, dumpdir


if __name__ == "__main__":
    print

    # proxy_source_list =  ['https://webanetlabs.net/freeproxylist/proxylist_at_03.01.2017.txt', 'https://webanetlabs.net/freeproxylist/proxylist_at_09.01.2017.txt', 'http://01717.ir/wp-content/uploads/2017/06/Proxy.txt', 'https://www.paighambot.com/wp-content/uploads/2016/11/proxies-15.txt', 'http://rebbis.ysmz.org/awstats/data/awstats112016.rebbis.ysmz.org.txt', 'https://github.com/yrjyrj123/MobikeAgent/blob/master/proxies.txt', 'https://sblam.com/blacklist.txt', 'http://www.simpleproxy.ru/core/1b0bf30d851b94bcd94738acdda8578e.txt', 'https://a.pomf.cat/yqbwjb.txt', 'http://stlblackmba.org/awstats/data/awstats072017.stlblackmba.org.txt', 'http://blog.chopperguy.net/awstats/data/awstats062017.blog.chopperguy.net.txt', 'http://umweltnetz.ch/awstats/data/awstats072017.umweltnetz.ch.txt', 'http://www.nptccd.health.gov.lk/uploaded/documents/tumdizin/omniapps/nptccdhealthgov/uploaded/sly.txt', 'https://www.freepublicproxylist.com/lists/6252018.txt', 'https://www.freepublicproxylist.com/lists/6242018.txt', 'https://www.freepublicproxylist.com/lists/6152018.txt', 'https://www.freepublicproxylist.com/lists/6182018.txt', 'http://h4.tgkanal.com/2018/06/28/465/5017175362606465075.txt', 'http://kishabajuku.si/awstats/data/awstats052017.kishabajuku.si.txt', 'http://kishabajuku.si/awstats/data/awstats102017.kishabajuku.si.txt', 'http://dev.bayareacasting.com/awstats/data/awstats122016.dev.bayareacasting.com.txt', 'http://williams.ie/awstats/data//awstats042018.williams.ie.txt', 'http://lafalaise-villeneuve.ch/awstats/data/awstats112016.lafalaise-villeneuve.ch.txt', 'http://www.mapwaves.org/awstats/data/awstats072017.mapwaveanalysis.com.txt', 'http://www.robinsdesk.com/awstats/data/awstats112016.shortsaleslist.com.txt', 'http://parkplaceboulder.com/awstats/data/awstats042018.parkplaceboulder.com.txt', 'http://www.amerossimplants.com/awstats/data/awstats042018.amerossimplants.com.txt', 'http://mpcreativedev.com/awstats/data/awstats042018.mpcreativedev.com.txt', 'http://technomine.ru/adept.txt', 'http://nice-hack.gid.pw/Forums/proxy.txt', 'http://www.austin-seafood.com/awstats/data/awstats112016.austin-seafood.com.txt', 'http://www.itzixue.com/%25E6%2596%25B0%25E5%25BB%25BA%25E6%2596%2587%25E6%259C%25AC%25E6%2596%2587%25E6%25A1%25A3.txt', 'http://ilaborator.ro/awstats/data/awstats052017.ilaborator.ro.txt', 'http://www.titanfighter.com/awstats/data/awstats042018.titanfighter.com.txt', 'http://www.n-souken.co.jp/cgis/awstats/stats/awstats022017.txt', 'http://montgomerymag.com/awstats/data/awstats042017.montgomerymag.com.txt', 'https://bridhaven.ie/awstats/data/awstats022017.bridhaven.ie.txt', 'http://www.auladecroly.com/awstats/data/awstats122016.auladecroly.com.txt', 'https://cdn-06.anonfile.com/laPcgff2b5/3d8ba46e-1532417546/92_899x_Elite_HQ_Mixed_Proxies_03-07-2018_._Nadal.txt', 'http://www.jagpartners.com.au/awstats/data/awstats022017.jagpartners.com.au.txt', 'http://burchellconsultinglimited.co.uk/awstats/data/awstats122016.burchellconsultinglimited.co.uk.txt', 'http://blog.casinofew.com/awstats/data/awstats012017.icelay.com.txt', 'http://hnpackages.com/awstats/data/awstats112016.hnpackages.com.txt', 'https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt', 'https://alaska-travel.net/awstats/data/awstats022017.alaska-travel.net.txt', 'http://www.picom.com.au/awstats/awstats042018.dtc.txt', 'http://www.albihome-apparthotel.fr/stats/awstats122016.www.albihome-apparthotel.fr.txt', 'http://blog.redmagiccasino.com/awstats/data/awstats112016.cashcasino.biz.txt', 'http://www.engagemedia.com.mx/awstats/data/awstats072017.engagemedia.com.mx.txt', 'http://patagonia-road.com/awstats/data//awstats042018.patagonia-road.com.txt', 'http://dobrist.ch/awstats/data/awstats062018.dobrist.ch.txt', 'http://hospitalexport.com/userfiles/mahan.txt', 'http://inspekt-rgh.com.ba/awstats/data/awstats102017.inspekt-rgh.com.ba.txt', 'https://www.che.upd.edu.ph/film/awstats/awstats062018.www.filminstitute.upd.edu.ph.txt', 'http://betcasino.biz/awstats/data/awstats042017.betcasino.biz.txt', 'https://proxyscra.pe/proxies/HTTPProxies.txt', 'http://www.nightsquad.eu/proxy.txt', 'http://www.zimmob.ch/awstats/data/awstats042018.zimmob.ch.txt', 'https://www.modaizle.com/wp-content/uploads/2017-proxy-listesi.txt', 'https://malwareworld.com/textlists/suspiciousIPs.txt', 'http://chevyworldparts.com/awstats/data/awstats122016.chevyworldparts.com.txt', 'http://redbingo.org/awstats/data/awstats112016.redbingo.org.txt', 'http://teste.teclavirtual.pt/awstats/data/awstats072017.teste.teclavirtual.pt.txt', 'http://www.medinachemist.com/stats/awstats/mklettingsnottingham.com/awstats062018.txt', 'http://elektroline.ch/awstats/data/awstats012017.elektroline.ch.txt', 'http://www.ecatalogues.net/ecatalog/tmp/awstats/awstats062018.ecatalogues.net.txt', 'http://pestybest.info/z.txt', 'http://ox.users.superford.org/awstats/data/awstats112016.ox.users.superford.org.txt', 'http://www.cokme.com.ua/awstats/data/awstats012017.cokme.com.ua.txt', 'http://www.nhhillclimbchallenge.com/awstats/data/awstats062018.nhhillclimbchallenge.com.txt', 'http://www.youtubebot.org/updaterNfo/socks.txt', 'http://dhcook.net/awstats/data/awstats112016.dhcook.net.txt', 'http://www.barretts-oesophagus.co.uk/awstats/data/awstats042017.barretts-oesophagus.co.uk.txt', 'empty_data', 'http://mostreka383.website/StolenCombos/New%2520Text%2520Document.txt', 'http://forum.layposters.com/awstats/data/awstats072017.casinofit.com.txt', 'https://prodigyy.host/u/9sfk.txt', 'https://softwarenova.net/proxy.txt', 'http://www.o2ss.fr/Mauritania.txt/home/web/h0lg4.org/logs/awstats122016.h0lg4.org.txt', 'http://www.o2ss.fr/Mauritania.txt/home/web/h0lg4.org/logs/awstats042017.h0lg4.org.txt', 'http://new.acmm.ie/awstats/data/awstats012017.new.acmm.ie.txt']
    proxy_source_list = ['https://pan.cccyun.cc/down.php/45811555cfdb2c11750bfc72c275413b.txt', 'https://webanetlabs.net/freeproxyweb/proxylist_at_17.06.2019.txt', 'https://webanetlabs.net/freeproxyweb/proxylist_at_23.01.2019.txt', 'https://mainware.tk/o/p.txt', 'https://cyber-hub.net/proxy/http.txt', 'http://www.bjhwxq.com/http.txt', 'https://cdn-23.anonfile.com/q0Q7b1T8m1/43529e1d-1567187596/8954x%2BProxies.txt', 'https://cdn-23.anonfile.com/J31c5cX6m1/5967900c-1567339105/proxies.txt', 'http://rungthaoduoc.com/file/17k%2520hq%2520Fast%2520http%2520proxy%2520by%2520HS.txt', 'https://admcomp.ru/downloads/proxyold.txt', 'http://www.shadowpvp.eu/api/proxychecker/scan.txt', 'https://onehack.us/uploads/short-url/pOijZyw3LafbNUPTpMosDJXCktx.txt', 'https://chteam.ir/Proxy-List-New-400K.txt', 'https://resolv3.me/proxies/https.txt', 'http://instagrambypass.com/bot/ip/proxy/prxt5656398.txt',
                         'http://instagrambypass.com/bot/ip/proxy/prxt5649801.txt', 'http://075000.xyz/proxy/tmd.txt', 'http://111.67.201.164/2.txt']
    search_word = "188.166.204.196"
    obj = Proxy_Reader(proxy_source_list, search_word)
    print(obj.Check_Dump_List)
    # Right_List = obj.Check_List_Proxy_Stat(proxy_source_list)
    # print(Right_List)
