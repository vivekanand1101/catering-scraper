import scrapy.item
import scrapy.selector
import scrapy.linkextractors
import scrapy.spiders
import scrapy.conf
import scrapy.crawler

import catering
import catering.items
import catering.settings

class CateringAppliances(scrapy.spiders.CrawlSpider):
    """Web Crawler for catering-appliance.com"""

    name = 'cateringapp'
    allowed_domains = ['www.catering-appliance.com']

    start_urls = ['http://www.catering-appliance.com']

    extraction_regex_list = ['/.*']

    extractor = scrapy.linkextractors.LinkExtractor(
            allow = extraction_regex_list,
            restrict_xpaths = (
                '//*[@id="products_wrapper"]'
            )
    )

    pagination_regex_list = ['/.*']

    paginate = scrapy.linkextractors.LinkExtractor(
            allow = pagination_regex_list,
            restrict_xpaths = (
                '//*[@id="categoriesnav"]/ul',
                '//div[contains(@class, "padesc flexbox")]',
            )
    )

    rules = [
        scrapy.spiders.Rule(
            extractor, callback='parse_items', follow=True
        ),
        scrapy.spiders.Rule(
            paginate
        )
    ]

    def parse_items(self, response):
        hxs = scrapy.Selector(response)

        item = catering.items.CateringItem()
        item['url'] = self.get_url(response)
        item['url_key'] = self.get_url_key(response)
        item['accessories'] = self.get_accessories(hxs)
        item['sku'] = self.get_sku(hxs)
        item['meta_desc'] = self.get_meta_desc(hxs)
        item['meta_key'] = self.get_meta_key(hxs)
        item['meta_title'] = self.get_meta_title(hxs)
        item['brand_logo'] = self.get_brand_logo(hxs)
        item['thumb_src'] = self.get_thumb_src(hxs)
        item['thumb_alt'] = self.get_thumb_alt(hxs)
        item['has_option'] = self.get_has_option(hxs)
        item['dropdown'] = self.get_has_dropdown(hxs)
        item['options'] = self.get_options(hxs)
        yield item

    def get_url(self, response):
        return response.url

    def get_url_key(self, response):
        url = self.get_url(response)
        url_key = url.replace('http://www.catering-appliance.com/', '')
        return url_key

    def get_sku(self, hxs):
        sku_path = hxs.xpath('//span[contains(@class, "dkbluetext")][contains(., "MPN")]/../following-sibling::node()/text()')
        try:
            sku = sku_path.extract()[0].strip()
            return sku
        except:
            return ''

    def get_accessories(self, hxs):
        accessories_path = hxs.xpath('//ul[contains(@class, "multibuys")]//a/text()')
        accessories = accessories_path.extract()
        return accessories

    def get_meta_desc(self, hxs):
        meta_desc = hxs.xpath('//meta[contains(@name, "description")]/@content')
        try:
            meta_desc = meta_desc.extract()[0].strip()
            return meta_desc
        except IndexError:
            return ''


    def get_meta_key(self, hxs):
        meta_desc = hxs.xpath('//meta[contains(@name, "keyword")]/@content')
        try:
            meta_desc = meta_desc.extract()[0].strip()
            return meta_desc
        except IndexError:
            return ''

    def get_meta_title(self, hxs):
        meta_title = hxs.xpath('//title/text()')
        try:
            meta_title = meta_title.extract()[0].strip()
            return meta_title
        except IndexError:
            return ''

    def get_brand_logo(self, hxs):
        brand_logo_path = hxs.xpath('//*[@id="basketform"]/p/img/@src')
        try:
            brand_logo = brand_logo_path.extract()[0].replace('/images/', '')
            return brand_logo
        except IndexError:
            return ''

    def get_thumb_src(self, hxs):
        thumb_src_path = hxs.xpath('//div[contains(@class, "thumbnails")]//img/@src')
        thumb_src = thumb_src_path.extract()
        x = []
        for i in thumb_src:
            x.append(i.split('/')[-1])
        return x

    def get_thumb_alt(self, hxs):
        thumb_alt_path = hxs.xpath('//div[contains(@class, "thumbnails")]//img/@alt')
        try:
            thumb_alt = thumb_alt_path.extract()[0]
            return thumb_alt
        except IndexError:
            return ''

    def get_has_option(self, hxs):
        has_option_path = hxs.xpath('//*[@id="optionsaccessories"]/h2[contains(., "Product Options")]/text()')
        try:
            has_option = has_option_path.extract()[0]
            return '1'
        except IndexError:
            return '0'

    def get_has_dropdown(self, hxs):
        has_option = self.get_has_option(hxs)
        if has_option == '1':
            return 'dropdown'
        else:
            return ''

    def get_options(self, hxs):
        options_path = hxs.xpath('//*[@id="optionsaccessories"]//div[contains(@class, "colour")]/text()')
        options = options_path.extract()
        options = [i.strip() for i in options]
        return options
