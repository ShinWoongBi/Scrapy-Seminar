import scrapy
from tutorial.items import NewsItem

'''
    class:
        NewsCrawlBasic: 
            기사 목록을 보여주는 페이지에서 보이는 모든 기사들의 정보를 수집하는 크롤러.
    function:
        parse:
            기사 목록을 보여주는 페이지에서 보이는 모든 기사들의 URL 을 찾아서 sub_parse 에 request 를 보낸다.
        sub_parse:
            기사 내용, 기사 작사, 기사 업로드 날짜 등 모든 정보를 수집해 저장한다.
'''


class NewsCrawlBasic(scrapy.Spider):
    name = "news_basic"
    start_urls = [
        "https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm&date=20191114&page=1"
    ]

    def parse(self, response):
        # 현재 url 에 존재하는 기사들의 url 수집
        for li in response.xpath("//ul[@class='type06_headline']/li"):
            url = li.xpath("dl/dt[1]/a/@href").get()  # 기사 URL
            imageUrl = li.xpath("dl/dt[@class='photo']/a/img/@src").get()  # 썸네일 주소
            author = li.xpath("dl/dd/span[@class='writing']/text()").get()  # 기사 작가

            # meta = {'imageUrl': imageUrl, 'url': url, 'author': author}  # 썸네일 주소, 작가, url 을 dict 로 저장
            yield scrapy.Request(url=url, callback=self.sub_parse)  # 기사 url 에 meta data 와 함 Request

    def sub_parse(self, response):
        # 기사 본문
        content = response.xpath("//div[@id='articleBodyContents']")
        content = content.xpath("text()").getall()
        content = ' '.join(content)
        content = content.replace('\t', '').replace('\n', '')

        title = response.xpath("//*[@id='articleTitle']/text()").get()  # 기사 제목
        date = response.xpath("//div[@class='sponsor']/span[@class='t11']/text()").get()  # 기사 업로드 날짜
        imaegUrl = response.meta.get('imaegUrl')  # 썸네일 주소
        author = response.meta.get('author')  # 기사 작가
        url = response.meta.get('url')  # 기사 URL

        # items 객체에 수집한 데이터 저장
        items = NewsItem()
        items['title'] = title
        items['author'] = author
        items['url'] = url
        items['imageUrl'] = imaegUrl
        items['content'] = content
        items['date'] = date

        # 결과 반환(items)
        yield items
