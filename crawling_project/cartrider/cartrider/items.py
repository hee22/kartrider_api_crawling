import scrapy

class CartriderItem(scrapy.Item):
    matches = scrapy.Field()
    trackId = scrapy.Field()
    kart = scrapy.Field()
    matchRank = scrapy.Field()
    rankinggrade2 = scrapy.Field()
