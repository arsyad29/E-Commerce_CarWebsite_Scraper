# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class MobilPipeline:
    def process_item(self, item, spider):
        
        # adapter = ItemAdapter(item)


        # Strip all whitespace from strings
        # field_names = adapter.field_names()
        # for field_name in field_names:
        #     if field_name != 'url':
        #         value = adapter.get(field_name)
                
                # print untuk mencari tahu bagian mana yang terbaca tuple oleh python
                # print("*******************")
                # print(value)

                # adapter[field_name] = value.strip()
                # jadi karna value = ()'2000c',) ada koma di belakang, maka hal itu di anggap tuple oleh python
                # dan cara mengatasinya ialah menambahkan [0] (untuk mengambil data di dalam string '2000c') pada value
                # adapter[field_name] = value[0].strip().replace('\\n', '').replace('\n', '').replace('  ','')


        return item
