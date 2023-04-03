import scrapy



class QuoteSpiderDetail(scrapy.Spider):
    name = 'goal'
    # start_urls = ['https://www.goal.com/en/news/1/']
    url = "https://www.goal.com/en/news/{}"

    def start_requests(self):
        for i in range(1, 4038):
            yield scrapy.Request(self.url.format(i))

    def parse(self, response):
        top_section = response.css("div.component-news-archive a::attr('href')")
        for i in top_section:
            # title_top_news = i.css('.item article.card_card__c3b2f div.content-wrapper div.content-body a h3.title span::text').get()
            # link_top_news = i.css("a::attr('href')").get()
            absolute_url = response.urljoin(i.get())
            
            yield response.follow(url=absolute_url, callback=self.detail_news)
        # next_page = response.css("div.component-paginator a::attr('href')").get()
        # print("l21", next_page)
      
    def detail_news(self, response):
        news_title = response.css("main.wrapper_component-layout-main__34R6u header h1.article_title___h6VL::text").get()
        news_teaser = response.css("main.wrapper_component-layout-main__34R6u div.article_content__XFYIz p.article_teaser__FgIqm::text").get()

        
        news_body = response.css("main.wrapper_component-layout-main__34R6u div.article-body_body__JAkqy")

        full_news_body = None
        for p in news_body:
            full_news_body = p.css("p::text").extract()
        
        l = None
        if full_news_body is not None:
            l = ' '.join(full_news_body)
        
        # breakpoint()

        if news_title is not None and news_teaser is not None and l is not None:
            myfile = open('news.txt', 'a')
            myfile.write(f"{news_title}\n\n")
            myfile.write(f"{news_teaser}\n\n")
            myfile.write(f"{l}\n\n\n")
            myfile.close()

        # yield{
        #     'title': news_title,
        #     'teaser': news_teaser,
        #     'news_body': l
        # }