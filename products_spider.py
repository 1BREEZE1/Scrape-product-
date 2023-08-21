import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    ]

    def parse(self, response):
        product_cards = response.css("div.s-result-item")

        for product_card in product_cards:
            product_info = {
                "url": response.urljoin(product_card.css("h2 a::attr(href)").get()),
                "name": product_card.css("h2 a span.a-text-normal::text").get(),
                "price": product_card.css("span.a-price span.a-offscreen::text").get(),
                "rating": product_card.css("span.a-icon-alt::text").get(),
                "reviews_count": product_card.css("span.a-size-base::text").get()
            }
            yield product_info

        # Follow pagination links for more pages
        next_page = response.css("li.a-last a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
