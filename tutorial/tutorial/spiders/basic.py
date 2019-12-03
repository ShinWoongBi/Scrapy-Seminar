import scrapy
import json


class BasicSpider(scrapy.Spider):
    name = 'basic'  # spider 이름

    # crawling 할 url
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    # json data 저장 array
    jsonData = []

    # parse() 함수가 제일 먼저 호출된다
    def parse(self, response):
        text = ""
        author = ""
        tags = ""

        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.xpath('span/small/text()').get()
            tags = quote.xpath('div/a/text()').getall()

            # jsonData 에 수집한 데이터 append
            self.jsonData.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        # 결과 출력
        print(json.dumps(self.jsonData))