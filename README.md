# Scrapy-Seminar
<img src="/Users/woongbishin/Woongbi_File/Scrapy-Seminar/scrapy_image.png" alt="scrapy" style="zoom:30%;" />

Scrapy 라이브러리를 이용한 Crawling 배워보기 - https://festa.io/events/717/

Python 라이브러리 'Scrapy'를 이용해 네이버 뉴스 크롤링까지 할 수 있는 세미나 입니다.

tutorial 디렉토리는 scrapy project이며 코드는 [spiders](https://github.com/ShinWoongBi/Scrapy-Seminar/tree/master/tutorial/tutorial/spiders)에서 참고하시기 바랍니다.

***

### 주의사항

**settings.py** 의 ROBOTSTXT_OBEY = False 로 변경해 주세요.

```python
ROBOTSTXT_OBEY = False
```

***

### Scrapy 실행방법

#### 프로젝트에 존재하는 spider를 조회

```bash
$ scrapy list
basic
main_news
news_basic
news_pages
```

#### spider 실행

~~~bash
$ scrapy crawl [spider_name]
~~~

#### spider 실행 후 scv, xml, json 파일로 출력

~~~bash
$ scrapy crawl [spider_name] -o [file_name].csv
$ scrapy crawl [spider_name] -o [file_name].json
~~~