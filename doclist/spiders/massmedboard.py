from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from doclist.items import DoclistItem, ExtraInfoItem
from scrapy.shell import inspect_response
class MassSpider(CrawlSpider):
    name = "massmedboard.org"
    #allowed_domains = ["massmedboard.org"]
    #start_urls = ['http://profiles.massmedboard.org/MA-Physician-Profile-Choose-Doctor.asp?lname=&showActiveCB=showActiveCBVal&showMDCB=showMDCBVal&fname=&showDOCB=showDOCBVal&town=&specialty=&hospital=&submit1=Find+Physician']

    rules = (
        #http://profiles.massmedboard.org/MA-Physician-Profile-View-Doctor.asp?ID=94307
        Rule(SgmlLinkExtractor(allow=('/MA-Physician-Profile-View-Doctor.asp\?ID=\d+',)), callback='parse_extra'),
    )

    '''
    def start_requests(self):
        f = open('/home/ubuntu/toriago/doclist/basic.csv')
        f.readline()
        template = 'http://profiles.massmedboard.org/MA-Physician-Profile-View-Doctor.asp?ID='
        #pages = []
        lines = f.readlines()
        for line in lines:
            yield template+line.split(',')[4]
        #return pages
    '''

    def start_requests(self):
        pages = []
        template = 'http://profiles.massmedboard.org/MA-Physician-Profile-Choose-Doctor.asp?lname=&showActiveCB=showActiveCBVal&showMDCB=showMDCBVal&fname=&showDOCB=showDOCBVal&town=&specialty=&hospital=&submit1=Find+Physician&PageNo=%d'
        
        last_page = 1658
        for i in xrange(1,last_page+1):
            url = template % (i,)
            pages.append(Request(url))
        return pages

    '''
    def parse_start_url(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[1]/font/a/@href').extract()
        last_names = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[1]/font/a/text()').extract()
        first_names = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[2]/font/text()').extract()
        initials = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[3]/font/text()').extract()
        specialties = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[4]/font/text()').extract()
        cities = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[5]/font/text()').extract()
        states = hxs.select('//tr[@onmouseover="this.bgColor=\'#ffee88\'"]/td[6]/font/text()').extract()
        
        items = []
        count = len(last_names)
        for i in range(count):
            di = DoclistItem()
            di['doctor_id'] = links[i].strip().split('=')[-1]
            di['last_name'] = last_names[i].strip()
            di['first_name'] = first_names[i].strip()
            di['initial'] = initials[i].strip()
            di['specialty'] = specialties[i].strip()
            di['city'] = cities[i].strip()
            di['state'] = states[i].strip()
            items.append(di)

        #inspect_response(response)
        return items
    '''

    def parse_extra(self, response):
        #inspect_response(response)
        doctor_id = response.url.split('=')[-1]
        hxs = HtmlXPathSelector(response)
        new_patients = hxs.select('//a[@href="javascript:openWin(\'MA-Physician-Profile-FAQ.asp#new_patients\')"]/../../../../td[3]/font/text()').extract()
        if len(new_patients) > 0:
            new_patients = str(new_patients[0].strip())
        else:
            new_patients = 'Unknown'

        medicaid = hxs.select('//a[@href="javascript:openWin(\'MA-Physician-Profile-FAQ.asp#medicaid\')"]/../../../../td[3]/font/text()').extract()
        if len(medicaid) > 0:
            medicaid = str(medicaid[0].strip())
        else:
            medicaid = 'Unknown'

        work_setting = hxs.select('//a[@href="javascript:openWin(\'MA-Physician-Profile-FAQ.asp#work_setting\')"]/../../../../td[3]/font/text()').extract()
        if len(work_setting) > 0:
            work_setting = str(work_setting[0].strip())
        else:
            work_setting = 'Unknown'

        address = hxs.select('//a[@href="javascript:openWin(\'MA-Physician-Profile-FAQ.asp#office_location\')"]')
        if len(address) > 0:
            address = address[0].select('../../../../td[3]/font/text()').extract()
            address = map((lambda x: str(' '.join(x.split()))), address)
            address += ['']*(4-len(address))
        else:
            address = ['Unknown', '', '', '']

        affiliation = hxs.select('//a[@href="javascript:openWin(\'MA-Physician-Profile-FAQ.asp#hosp_affil\')"]/../../../../td[3]/font/text()').extract()
        affiliation = map((lambda x: str(' '.join(x.split()))), affiliation)
        affiliation += ['']*(4-len(affiliation))

        grad_year = hxs.select('//a[@href=\'javascript:openWin("MA-Physician-Profile-FAQ.asp#grad_date")\']/../../../../td[3]/font/text()').extract()
        if len(grad_year) > 0:
            grad_year = str(grad_year[0].strip())
        else:
            grad_year = 'Unknown'

        ei = ExtraInfoItem()
        ei['doctor_id'] = doctor_id
        ei['new_patients'] = new_patients
        ei['medicaid'] = medicaid
        ei['work_setting'] = work_setting
        ei['address1'] = address[0]
        ei['address2'] = address[1]
        ei['address3'] = address[2]
        ei['address4'] = address[3]
        ei['affiliation1'] = affiliation[0]
        ei['affiliation2'] = affiliation[1]
        ei['affiliation3'] = affiliation[2]
        ei['affiliation4'] = affiliation[3]
        ei['graduation_year'] = grad_year

        return ei
