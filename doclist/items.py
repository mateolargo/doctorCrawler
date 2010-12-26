# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class DoclistItem(Item):
    doctor_id = Field()
    first_name = Field()
    last_name = Field()
    initial = Field()
    specialty = Field()
    city = Field()
    state = Field()

class ExtraInfoItem(Item):
    doctor_id = Field()
    new_patients = Field()
    medicaid = Field()
    work_setting = Field()
    address1 = Field()
    address2 = Field()
    address3 = Field()
    address4 = Field()
    affiliation1 = Field()
    affiliation2 = Field()
    affiliation3 = Field()
    affiliation4 = Field()
    graduation_year = Field()
    
