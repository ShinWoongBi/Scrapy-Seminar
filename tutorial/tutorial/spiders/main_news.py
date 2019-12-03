import scrapy
from tutorial.items import NewsItem
import json

'''
    class:
        NewsCrawlMain: 
            원하는 뉴스 카테고리의 기사들을 원하는 페이지 수 만큼 수집하는 크롤러.
    function:
        parse:
            self.pages 만큼 Request 를 보낸다.
        parse_page:
            기사 목록을 보여주는 페이지에서 보이는 모든 기사들의 URL 을 찾아서 sub_parse 에 request 를 보낸다.
        sub_parse:
            기사 내용, 기사 작사, 기사 업로드 날짜 등 모든 정보를 수집해 저장한다.
'''


class NewsCrawlMain(scrapy.Spider):
    name = "main_news"
    pages = 1  # 가져올 페이지 수

    url = "https://news.naver.com/main/mainNews.nhn?sid1=101&page="
    start_urls = [
        "https://news.naver.com/"
    ]
    categories = {'정치': '100', '경제': '101', '사회': '102', '생활문화': '103', '세계': '104', 'IT과학': '105', '오피니언': '110',
                       'politics': '100', 'economy': '101', 'society': '102', 'living_culture': '103', 'world': '104',
                       'IT_science': '105', 'opinion': '110'}
    selected_categories = '경제'

    def parse(self, response):
        for i in range(1, self.pages+1):
            yield scrapy.Request(url=self.url + str(i), callback=self.parse_page)

    def parse_page(self, response):
        category = self.categories[self.selected_categories]  # 뉴스 카테고리

        # 뉴스 JsonData
        jsonStr = json.loads(json.loads(response.text)['airsResult'])['result']
        jsonStr = jsonStr[category]

        for content in jsonStr:
            articleId = content['articleId']
            officeId = content['officeId']
            officeName = content['officeName']
            title = content['title']
            summary = content['summary']
            imageUrl = content['imageUrl']

            url = "https://news.naver.com/main/read.nhn?sid1="+category+"&oid="+officeId+"&aid="+articleId
            meta = {'imageUrl': imageUrl, 'url': url, 'author': officeName, 'summary': summary, 'title': title}
            yield scrapy.Request(url=url, callback=self.sub_parse, meta=meta)

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