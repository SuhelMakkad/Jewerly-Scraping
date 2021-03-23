import scrapy
import json

class JewerlySpider(scrapy.Spider):
    name = 'jewerly_urls'
    count = 2
    start_urls = ['https://www.houseofindya.com/zyra/cat?depth=1&label=Jewelry']
    list_urls = []

    def parse(self, responce):
        JewerlySpider.list_urls = []
        for jewerly in responce.xpath("//ul[@id='JsonProductList']"):
            JewerlySpider.list_urls.append(jewerly.xpath("./li/@data-url").extract())
            # print(list_urls)

        next_page = f"https://www.houseofindya.com/zyra/cat?depth=1&label=Jewelry&page={JewerlySpider.count}"
        if JewerlySpider.count <= 5:
            yield responce.follow(next_page, callback=self.parse)

        JewerlySpider.count += 1
        yield {
            'jewerly_list_urls': JewerlySpider.list_urls
        }

class DetailsSpider(scrapy.Spider): 
    name = "jewerly_details"
    count = 0

    try:
        f = open('urls.json')

        data = json.load(f)
        urls = []
        for url in data:
            urls += url["jewerly_list_urls"][0]

        start_urls = [urls[count]]

        def parse(self, responce):
            for jewerly in responce.xpath("//div[@class='prodCntr']"):
                yield {
                    "price": jewerly.xpath("./div[@class='prodRight']/h4/span[@style='font-size:20px;color:#ed1c24']/text()").extract_first().strip(),
                    "discription": jewerly.xpath("./div[@class='prodRight']/div[@class='prodecCntr']/div[@id='tab-1']/p/text()").extract_first().rstrip().lstrip(),
                    "image_urls": jewerly.xpath("./div[@class='prodLeft']/div/ul/li/a/@data-image").extract()
                }

            DetailsSpider.count += 1
            next_page = DetailsSpider.urls[DetailsSpider.count]

            if DetailsSpider.count < len(DetailsSpider.urls):
                yield responce.follow(next_page, callback=self.parse)

    except:
        pass





