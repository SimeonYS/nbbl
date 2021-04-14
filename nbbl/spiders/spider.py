import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import NnbblItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class NnbblSpider(scrapy.Spider):
	name = 'nbbl'
	start_urls = ['https://www.nbbl.bz/news/']

	def parse(self, response):
		post_links = response.xpath('//h5/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="post_meta_item post_date"]/a/text()').get()
		title = response.xpath('//h3/text()').get()
		content = response.xpath('(//div[@class="wpb_wrapper"]/div[@class="wpb_text_column wpb_content_element "])[position()>1]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=NnbblItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
