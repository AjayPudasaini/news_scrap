import scrapy



class QuoteSpiderDetail(scrapy.Spider):
    name = 'theguardian'
    start_urls = ['https://www.theguardian.com/football']
    # url = "https://www.goal.com/en/news/{}"

    # def start_requests(self):
    #     for i in range(1, 4038):
    #         yield scrapy.Request(self.url.format(i))

    def parse(self, response):
        top_section = response.css("div.fc-item__container a::attr('href')")
        for i in top_section:
            absolute_url = response.urljoin(i.get())
            yield response.follow(url=absolute_url, callback=self.detail_news)

      
    def detail_news(self, response):
        news_title = response.css("div.dcr-1txtwj h1.dcr-d3raws::text").get()
        news_body = response.css("div.dcr-16guhjf div.article-body-commercial-selector")        
        
        full_news_body = None
       
        for p in news_body:
            n = []
            if p.css("p span.dcr-uj791q"):
                first_letter = p.css("p span.dcr-wio59t::text").get()
                first_complete_p = p.css("p span.dcr-1up63on::text").get()
                c = str(first_letter) + str(first_complete_p)
                n.append(c)
            full_news_body = p.css("p::text").extract()
            n.append(full_news_body)
            full_news_body = n

        l = None
        if full_news_body is not None:
            if len(full_news_body) == 2:
                c = full_news_body[:1] + full_news_body[1]
                l = ' '.join(c)
        
        # # breakpoint()
        
        if news_title is not None and l is not None:
            myfile = open('theguardian.txt', 'a')
            myfile.write(f"{news_title}\n\n")
            myfile.write(f"{l}\n\n\n")
            myfile.close()

        # yield{
        #     'title': news_title,
        #     'news_body': news_body
        # }