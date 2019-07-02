import scrapy
from ScrapyDemo.items import QuoteItem
from ScrapyDemo.items import AuthorItem

class QuotesSpider(scrapy.Spider):
    name='quote'
    allowed_domains = ['http://quotes.toscrape.com/']

    def start_requests(self):
        urls=[
            'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        courses = response.xpath('//div[@class="col-md-8"]/div[@class="quote"]')

        for course in courses:
            item = QuoteItem()
            item['text']=course.xpath('.//span[@class="text"]/text()').extract_first()
            item['author']=course.xpath('.//small[@class="author"]/text()').extract_first()
            item['tags']=course.xpath('.//div[@class="tags"]/a/text()').extract_first()

            author_url=course.xpath('.//a/@href').extract_first()
            if author_url!='':
                request = scrapy.Request(url='http://quotes.toscrape.com'+author_url, dont_filter=True, callback=self.authorParse)
                request.meta['item']=item
                yield request

        next_page_request=self.requestNextPage(response)
        yield next_page_request


    def authorParse(self,response):
        item=response.meta['item']
        sources=response.xpath('//div[@class="author-details"]')
        author_item=AuthorItem()
        for source in sources:
            author_item['name'] = source.xpath('.//h3[@class="author-title"]/text()').extract_first()
            author_item['birthday'] = source.xpath('.//span[@class="author-born-date"]/text()').extract_first()
            author_item['address'] = source.xpath('.//span[@class="author-born-location"]/text()').extract_first()
            author_item['description'] = source.xpath('.//div[@class="author-description"]/text()').extract_first()

        item['author']=author_item

        yield item

    def requestNextPage(self,response):
        next_page=response.xpath('.//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            if next_page!='':
                return scrapy.Request(url='http://quotes.toscrape.com/'+next_page, callback=self.parse)
        return None