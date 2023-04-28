import scrapy
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
import csv
import pandas as pd

class Articulo(Item):
    title = Field()
    price = Field()
    desc = Field()

class MercadoLibreSpider(CrawlSpider):
    name = 'mercadolibre'
    allowed_domains = ['mercadolibre.com.ar', 'listado.mercadolibre.com.ar']
    start_urls = ['https://listado.mercadolibre.com.ar/procesadores#D[A:procesadores]']
    delay_download = 1
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20, # Limitamos la cantidad de páginas a recorrer
        'FEED_URI': 'procesadores.csv', # Exportamos los datos a un archivo CSV
        'FEED_FORMAT': 'csv'
    }

    # Definimos las reglas de navegación
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/computacion/componentes-pc/procesadores/_Desde_\d+'
            ), follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'/procesador-'
            ), follow=True, callback='parse_items'
        ),
    )

    def Limpiartext(self, texto):
        nuevotext = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevotext

    # Cargamos los datos
    def parse_items(self, response):
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)
        item.add_xpath('title', '//h1/text()', MapCompose(self.Limpiartext))
        item.add_xpath('price', '//span[@class="andes-money-amount__fraction"]/text()')
        item.add_xpath('desc', '//div[@class="ui-pdp-description pl-45 pr-45 ui-pdp-collapsable--is-collapsed"]/p/text()', MapCompose(self.Limpiartext))
        yield item.load_item()
    
    # Ordenamos la información del archivo y guardamos en uno nuevo
    def closed(self, reason):
        df = pd.read_csv('procesadores.csv')
        df = df.dropna()
        df = df.sort_values(by=['precio'], ascending=True)
        df.to_csv('procesadoresActualizado.csv', index=False, encoding='utf-8')

# Pendiente el eliminar los valores duplicados y cambiar el orden de las columnas  