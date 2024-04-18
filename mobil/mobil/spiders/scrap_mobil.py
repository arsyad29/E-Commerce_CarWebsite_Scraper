import scrapy
# from playwright.sync_api import sync_playwright
import time
import pandas as pd
from mobil.items import MobilItem

class ScrapMobilSpider(scrapy.Spider):
    name = "scrap_mobil"    
    allowed_domains = ["mobilbaru.mobil123.com"]
    start_urls = ["https://mobilbaru.mobil123.com/price-list"]

    def parse(self, response):

        # Filter asc dan desc
        filter_input = int(input('1. Harga jual rendah\n2. Harga jual tinggi\n3. Terpopuler\nInput number filter: '))
        if filter_input == 1:
            filter_num = 'asc'
        elif filter_input == 2:
            filter_num = 'desc'
        elif filter_input == 3:
            filter_num = 'popularity'
        else:
            print('Masukkan filter salah, coba lagi')

        # Filter brand
        list_brand = response.css('div.right').css('div.brand-filter').css('div.sort_by_block').css('select').css('option::text').getall()
        print('===========================')
        for index, i in enumerate(list_brand):
            print(index, i)
        brand_input = int(input('\nMasukkan nomor brand: '))
        if brand_input == 0:
            brand_output ='price-list'
            for i in range(0, 10):
                try: url = "https://mobilbaru.mobil123.com/{}?_token=yAMf6nUnORAdq5oBumwfCfxvvGMWgXASimW8yqQt&page={}&order={}".format(str(brand_output).lower(), str(i), str(filter_num))
                except: url = ''
                yield scrapy.Request(url, callback=self.find_links)
        else:
            brand_output = list_brand[brand_input]
            for i in range(0, 10):
                try: url = "https://mobilbaru.mobil123.com/price-list/{}?_token=yAMf6nUnORAdq5oBumwfCfxvvGMWgXASimW8yqQt&page={}&order={}".format(str(brand_output).lower(), str(i), str(filter_num))
                except: url = ''
                yield scrapy.Request(url, callback=self.find_links)

        # # Link header
        # for i in range(0, 10):
        #     # try: url = "https://mobilbaru.mobil123.com/price-list?_token=yAMf6nUnORAdq5oBumwfCfxvvGMWgXASimW8yqQt&page={}&order={}".format(str(i), filter_input)
        #     # try: url = "https://mobilbaru.mobil123.com/{}?_token=yAMf6nUnORAdq5oBumwfCfxvvGMWgXASimW8yqQt&page={}&order={}".format(brand_output.lower(), str(i), filter_num)
        #     try: url = "https://mobilbaru.mobil123.com/{}?_token=yAMf6nUnORAdq5oBumwfCfxvvGMWgXASimW8yqQt&page={}&order={}".format(str(brand_output).lower(), str(i), str(filter_num))
        #     https://mobilbaru.mobil123.com/price-list/bmw?_token=nQcW99xW1N2zkoNgAG1j5y2o7iFjtABA1veksZFH&page=0&order=popularity
        #     except: url = ''
        #     yield scrapy.Request(url, callback=self.find_links)

    def find_links(self, response):
        # Untuk mengambil masing-masing link yang dibuat
        # Link sub
        links = response.css('div[class*=result]').css('div[class*=rows]').css('a ::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.find_details)

    
    def find_details(self, response):
        '''
            Sedikit logic, jika setelah tahun ada 2 slash maka itu adalah website yang lengkap
            Contoh1 = 2024/xe/hse (ini lengkap)
            Contoh2 = 2024/xe (ini tidak lengkap)
            diantar kedua contoh itu memiliki 2 web yang berbeda

            Link contoh1 = links: https://mobilbaru.mobil123.com/jaguar/2024/xf/portfolio 
            Link contoh2 = links: https://mobilbaru.mobil123.com/jaguar/2024/f-type

            name1 = untuk link contoh1
            name2 = untuk link contoh2

            link contoh price1 = https://mobilbaru.mobil123.com/wuling/2024/formo/max-standard
            Link contoh price2 = https://mobilbaru.mobil123.com/mini/2024/countryman
        '''
        name1 = None
        name2 = None
        
        name = response.css('div.variant-name div.name-header span::text').get()
        if name is not None:
            name1 = name.strip()
            try: transmission1 = response.css('div.col-row-wrap').css('#transmission').css('div.row-flex').css('div[class|=col-flex]::text').get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: transmission1 = ''
            try: capacity1 = response.css('div.col-row-wrap').css('#enginespecification').css('div.row-flex').css('div[class|=col-flex]::text')[1].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: capacity1 = ''
            try: fueltype1 = response.css('div.col-row-wrap').css('#enginespecification').css('div.row-flex').css('div[class|=col-flex]::text')[5].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: fueltype1 = ''
            try: seat1 = response.css('div.col-row-wrap').css('#general').css('div.row-flex').css('div[class|=col-flex]::text')[1].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: seat1 = ''
            try: price1 = response.css('div.variant-name').css('div.name-section').css('div.name-header').css('div.price1-header').css('div.price-full::text').get().strip().replace(',', '').replace('RP ', '')
            except: price1 = ''

        if name is None:
            name2 = response.css('div[class*=cg-m-5]').css('h1[class*=model-name]::text').get()
            try: transmission2 = response.css('section.key-details.clearfix').css('li.transmission::text')[1].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: transmission2 = ''
            try: capacity2 = response.css('section.key-details.clearfix').css('li.capacity::text')[1].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: capacity2 = ''
            try: fueltype2 = response.css('section.key-details.clearfix').css('li.fuel-type::text')[1].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: fueltype2 = ''
            try: seat2 = response.css('section.key-details.clearfix').css('li.seat-capacity::text')[1].get().strip().replace('\\n', '').replace('\n', '').replace('  ','')
            except: seat2 = ''
            try: price2 = response.css('div.cg-m-5.car-info').css('span.second::text').get().strip().replace(',', '').replace('RP ','')
            except: price2 = ''

            
            # Assign name2 to name1 if name1 is None
            name1 = name2.strip()
            transmission1 = transmission2
            capacity1 = capacity2
            fueltype1 = fueltype2
            seat1 = seat2
            price1 = price2

        mobil_item = MobilItem()

        mobil_item['url'] = response.url,
        mobil_item['name'] = name1,
        mobil_item['transmission'] = transmission1,
        mobil_item['capacity'] = capacity1,
        mobil_item['fueltype'] = fueltype1,
        mobil_item['seat'] = seat1
        mobil_item['price'] = price1

        yield mobil_item

        
        # output = {'Url': response.url,
        #           'Name': name1,
        #           'Transmission': transmission1,
        #           'Capacity': capacity1,
        #           'Fuel Type': fueltype1,
        #           'Seat': seat1
        #           }
        # yield output
        ############################################################
        # Otomatis
        # comfort_col = response.css('div.col-row-wrap').css('#comfort').css('div.row-flex').css('div.col-flex.left::text').getall()
        # comfort_row = response.css('div.col-row-wrap').css('#comfort').css('div.row-flex').css('div[class|=col-flex]::text').getall()

        # entertainment_col = response.css('div.col-row-wrap').css('#entertainment').css('div.row-flex').css('div[class|=col-flex]::text').getall()
        # entertainment_row = response.css('div.col-row-wrap').css('#entertainment').css('div.row-flex').css('div[class|=col-flex]::text').getall()

        # # Adding data into dictionary
        # list_mobil1 = {}

        # # Add name
        # list_mobil1['Name'] = name1

        # # Add comfort info
        # for column, value in zip(comfort_col, comfort_row):
        #     # Tambahkan pasangan kunci dan nilai ke dalam dictionary
        #     list_mobil1[column.strip()] = value.strip()

        # # Add entertainment info
        # for column, value in zip(entertainment_col, entertainment_row):
        #     # Tambahkan pasangan kunci dan nilai ke dalam dictionary
        #     list_mobil1[column.strip()] = value.strip()
        ############################################################