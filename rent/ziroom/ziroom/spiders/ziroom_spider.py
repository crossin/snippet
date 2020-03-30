# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ziroom.items import ZiroomItem
import re

class ZiroomSpiderSpider(CrawlSpider):
    name = 'ziroom_spider'
    # allowed_domains = ['wh.ziroom.com']
    # 由于能力问题，还没找到办法全自动爬取，所以抓取各城市信息的时候，将注释取消，且修改setting.py中DEFAULT_REQUEST_HEADERS中的host
    # 例如抓取bj,则 host：bj.ziroom.com, tj，则 tj.ziroom.com
    
    # city = "bj"
    # start_urls = ['http://www.ziroom.com/z/z0-d23008614/?isOpen=0','http://www.ziroom.com/z/z0-d23008626/?isOpen=0'
    #               'http://www.ziroom.com/z/z0-d23008613/?isOpen=0','http://www.ziroom.com/z/z0-d23008618/?isOpen=0',
    #               'http://www.ziroom.com/z/z0-d23008617/?isOpen=0', 'http://www.ziroom.com/z/z0-d23008623/?isOpen=0',
    #               'http://www.ziroom.com/z/z0-d23008625/?isOpen=0','http://www.ziroom.com/z/z0-d23008611/?isOpen=0',
    #               'http://www.ziroom.com/z/z0-d23008615/?isOpen=0', 'http://www.ziroom.com/z/z0-d23008629/?isOpen=0',
    #               'http://www.ziroom.com/z/z0-d23008624/?isOpen=0', 'http://www.ziroom.com/z/z0-d23008616/?isOpen=0',
    #               'http://www.ziroom.com/z/z0-d23008620/?isOpen=0']

    city = "hz"
    start_urls = ['http://hz.ziroom.com/z/d330106/?isOpen=0',
                  'http://hz.ziroom.com/z/d330103/?isOpen=0',
                  'http://hz.ziroom.com/z/d330104/?isOpen=0',
                  'http://hz.ziroom.com/z/d330105/?isOpen=0',
                  'http://hz.ziroom.com/z/d330102/?isOpen=0',
                  'http://hz.ziroom.com/z/d330108/?isOpen=0',
                  'http://hz.ziroom.com/z/d330110/?isOpen=0',
                  'http://hz.ziroom.com/z/d330109/?isOpen=0',
                  'http://hz.ziroom.com/z/d23009161/?isOpen=0',
                  'http://hz.ziroom.com/z/d23011864/?isOpen=0'
                   ]
    
    # city = "sz"
    # start_urls = ['http://sz.ziroom.com/z/d23008674/?isOpen=0',
    #               'http://sz.ziroom.com/z/d23008679/?isOpen=0',
    #               'http://sz.ziroom.com/z/d23008672/?isOpen=0',
    #               'http://sz.ziroom.com/z/d23008676/?isOpen=0',
    #               'http://sz.ziroom.com/z/d23008678/?isOpen=0',
    #               'http://sz.ziroom.com/z/d23008677/?isOpen=0']

    # city = "sh"
    # start_urls = [
    #     'http://sh.ziroom.com/z/d310106/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310104/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310101/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310105/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310107/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310115/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310113/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310108/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310109/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310110/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310112/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310114/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310117/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310118/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310120/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310116/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310230/?isOpen=0',
    #     'http://sh.ziroom.com/z/d310333/?isOpen=0',
    #     ]

    # city = "gz"
    # start_urls = ['http://gz.ziroom.com/z/d23008633/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008634/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008635/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008636/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008637/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008638/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008639/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008640/?isOpen=0',
    # 'http://gz.ziroom.com/z/d23008643/?isOpen=0']
    
    # city = "nj"
    # start_urls =  ['http://nj.ziroom.com/z/d320106/?isOpen=0','http://nj.ziroom.com/z/d320105/?isOpen=0',
    #                 'http://nj.ziroom.com/z/d320102/?isOpen=0','http://nj.ziroom.com/z/d320104/?isOpen=0',
    #             'http://nj.ziroom.com/z/d320114/?isOpen=0','http://nj.ziroom.com/z/d320113/?isOpen=0',
    #             'http://nj.ziroom.com/z/d320115/?isOpen=0','http://nj.ziroom.com/z/d320111/?isOpen=0']

    # city = "cd"
    # start_urls = ['http://cd.ziroom.com/z/d510104/?isOpen=0','http://cd.ziroom.com/z/d510105/?isOpen=0',
    #               'http://cd.ziroom.com/z/d510106/?isOpen=0','http://cd.ziroom.com/z/d990002/?isOpen=0',
    #               'http://cd.ziroom.com/z/d510107/?isOpen=0','http://cd.ziroom.com/z/d510108/?isOpen=0',
    #               'http://cd.ziroom.com/z/d510108/?isOpen=0','http://cd.ziroom.com/z/d510122/?isOpen=0',
    #               'http://cd.ziroom.com/z/d23008850/?isOpen=0'
    #               ]

    # city = "wh"
    # start_urls = ['http://wh.ziroom.com/z/d23008782/?isOpen=0','http://wh.ziroom.com/z/d23008785/?isOpen=0',
    #               'http://wh.ziroom.com/z/d23008779/?isOpen=0','http://wh.ziroom.com/z/d420115/?isOpen=0',
    #               'http://wh.ziroom.com/z/d23008780/?isOpen=0','http://wh.ziroom.com/z/d23008781/?isOpen=0',
    #               'http://wh.ziroom.com/z/d23008783/?isOpen=0','http://wh.ziroom.com/z/d23008784/?isOpen=0',
    #               'http://wh.ziroom.com/z/d23009129/?isOpen=0'
    #               ]

    # city = "tj"
    # start_urls = ['http://tj.ziroom.com/z/d120101/?isOpen=0','http://tj.ziroom.com/z/d120104/?isOpen=0',
    #               'http://tj.ziroom.com/z/d120103/?isOpen=0','http://tj.ziroom.com/z/d120102/?isOpen=0',
    #               'http://tj.ziroom.com/z/d120105/?isOpen=0','http://tj.ziroom.com/z/d120106/?isOpen=0',
    #               'http://tj.ziroom.com/z/d120111/?isOpen=0','http://tj.ziroom.com/z/d120113/?isOpen=0',
    #               'http://tj.ziroom.com/z/d120110/?isOpen=0','http://tj.ziroom.com/z/d120112/?isOpen=0',
    #              ]
    rules = (
        # 设置爬取需要爬取url的正则表达式
        Rule(LinkExtractor(allow=r'http://.*\.ziroom.com/z\/.*/\?isOpen=0'), follow=True),
        # follow =True
        Rule(LinkExtractor(allow=r'http://.*\.ziroom.com/z\/.*d\d+-p\d+\/'),callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
        Z_list_box = response.xpath("/html/body/section/div[3]/div[2]/div")

        # 因为网页中穿插有广告，所以使用try语句，如果提取不到信息则代表为广告。
        for ziroom in Z_list_box:
            try:
                title = ziroom.xpath(".//h5/a/text()").get()
            except:
                title = ""
            try:
                desc = ziroom.xpath("./div[2]/div[1]/div[1]/text()").get()
            except:
                desc = ""
            try:
                location = ziroom.xpath("./div[2]/div[1]/div[2]/text()").get().replace("\n","").replace("\t","").strip(" ")
            except:
                location = ""
            try:
                region = response.xpath("/html/body/section/div[2]/div[2]/div[2]/a/text()").get()
            except:
                region = ""

            picture = ""
            try:
                prices_url = ziroom.xpath(".//div[@class='price']/span[2]/@style").get()
                pattern1 = re.compile(r'//static8.*png')
                prices_url = "http:" + pattern1.search(prices_url).group(0) 
            except:
                prices_url = ""
                picture = ""
                
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/c4b718a0002eb143ea3484b373071495.png":
                picture = '9310867542'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/48d4fa3aa7adf78a1feee05d78f33700.png":
                picture = '6291078453'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/f4c1f82540f8d287aa53492a44f5819b.png":
                picture = '4978123605'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/a8a37e8b760bc3538c37b93d60043cfc.png":
                picture = '4983571602'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/2e120609b7f35a9ebec0c72c4b7502b2.png":
                picture = '7465139280'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/0f2d52da9106e522530305f1a1fa0788.png":
                picture = '6948527301'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/dff9d441e1fc59f793d5c3b68461b3ea.png":
                picture = '5471380629'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/377327c0373f87395ab1908cd1607c1b.png":
                picture = '6547098213'
            if prices_url == "http://static8.ziroom.com/phoenix/pc/images/price/new-list/a9da4f199beb8d74bffa9500762fd7b7.png":
                picture = '8670415923'
            if prices_url ==  "http://static8.ziroom.com/phoenix/pc/images/price/new-list/9aef59e0b28bf1225780d84f37520891.png":
                picture = '9635804271'
            try:
                room_url = ziroom.xpath(".//h5/a/@href").get()
            except:
                room_url = ""

            pattern = re.compile(r'-\d+.*px')
            img_px_list = ['-0px', '-21.4px', '-42.8px', '-64.2px', '-85.6px', '-107px', '-128.4px', '-149.8px', '-171.2px', '-192.6px']
            try:
                num_1 = ziroom.xpath(".//div[@class='price']/span[2]/@style").get()
                num_1 = pattern.search(num_1).group(0)
                num_1 = img_px_list.index(num_1)
            except:
                # 如果是广告则为 0
                num_1 = 0
            try:
                num_2 = ziroom.xpath(".//div[@class='price']/span[3]/@style").get()
                num_2 = pattern.search(num_2).group(0)
                num_2 = img_px_list.index(num_2)
            except:
                num_2 = 0
            # 因为存在日租的价格所以，日租价格可能不会上百，所以需要判断是否日租，因为有10个位置，所以num取值只要不是0-9就可以
            try:
                num_3 = ziroom.xpath(".//div[@class='price']/span[4]/@style").get()
                num_3 = pattern.search(num_3).group(0)
                num_3 = img_px_list.index(num_3)
            except:
                num_3 = 10
            try:
                num_4 = ziroom.xpath(".//div[@class='price']/span[5]/@style").get()
                num_4 = pattern.search(num_4).group(0)
                num_4 = img_px_list.index(num_4)
            except:
                num_4 = 10             
            try:
                if num_3 ==10 and num_4 ==10:
                    price = picture[num_1] + picture[num_2]
                elif num_3 !=10 and num_4 == 10:
                    price = picture[num_1] + picture[num_2] +picture[num_3]     
                else:
                    price = picture[num_1] + picture[num_2] +picture[num_3] + picture[num_4]
            except:
                price = 0
            print(self.city)
            item = ZiroomItem(
                title = title,
                desc = desc,
                location = location,
                region = region,
                prices_url = prices_url,
                price = price,
                room_url = room_url,
                city = self.city,
            )
            yield item

            


