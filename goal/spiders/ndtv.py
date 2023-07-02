import scrapy



class QuoteSpiderDetail(scrapy.Spider):
    name = 'ndtv'
    start_urls = ['https://sports.ndtv.com/football/news']


    def parse(self, response):
        top_section = response.css("div.lst-pg_hd li.lst-pg-a-li div.lst-pg_txt-wrp a::attr('href')").extract()
        remove_list = ["javascript:void(0)"]
        url_lists = [i for i in top_section if i not in remove_list]
        for i in url_lists:
            absolute_url = response.urljoin(i)
            yield response.follow(url=absolute_url, callback=self.detail_news)

      
    def detail_news(self, response):
        news_title = response.css("div.sp-cn h1.sp-ttl::text").get()
        news_teaser = response.css("div.sp-cn h2.sp-descp::text").get()
        news_body = response.css("div.story__content")

        full_news_body = None
        for p in news_body:
            full_news_body = p.css("p::text").extract()
        
        l = None
        if full_news_body is not None:
            l = ' '.join(full_news_body)
        
        # breakpoint()

        if news_title is not None and news_teaser is not None and l is not None:
            myfile = open('ndtv.txt', 'a')
            myfile.write(f"{news_title}\n\n")
            myfile.write(f"{news_teaser}\n\n")
            myfile.write(f"{l}\n\n\n")
            myfile.close()