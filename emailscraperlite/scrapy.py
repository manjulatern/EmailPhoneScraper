import logging, csv, re, traceback, sys
import phonenumbers
from extract_emails import ExtractEmails
import requests

class PhoneEmailScraperLite():

	def scrape(self,urls,depth):
		if depth == "all":
			depth = None
		logging.warning("EmailPhoneSpider; Extraction Process Started")
		
		file = open('output.csv', 'w')
		writer = csv.writer(file)
		writer.writerow(["URL", "Phone", "Email"])
		file.close()
		for url in urls:
			logging.warning("EmailPhoneSpider; Extraction started for URL: %s",url)
			phone_numbers = ""
			emails = ""
			try:
				html_text = requests.get(url).text
				phone_numbers = self.extract_phone(html_text,url)
				emails = self.extract_emails(url,depth)
				file = open('output.csv', 'a')
				writer = csv.writer(file)
				writer.writerow([url, phone_numbers, emails])
				logging.warning("EmailPhoneSpider; Adding data in CSV for URL: %s",url)
			except Exception as e:
				logging.error("EmailPhoneSpider;Error on Extraction for URL=%s; Error: %s ",url,traceback.format_exc())	
				logging.error("Not a valid URL")
			finally:
				file.close()

	def extract_phone(self,html_text,url):
		number = ""
		try:
			phone_numbers = set()
			for match in phonenumbers.PhoneNumberMatcher(html_text, "US"):
				phone = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
				phone_numbers.add(str(phone))	
			for num in phone_numbers:
				if num:
					number = number + num + ","
		except Exception as e:
			logging.debug("EmailPhoneSpider;Error on Phone Number Extraction for URL=%s; Error: %s ",url,traceback.format_exc())	

		logging.warning("EmailPhoneSpider;Phone Number Extraction completed for URL: %s",url)
		return number.strip(",")

	def extract_emails(self,url,depth):
		all_emails = ""
		try:
			em = ExtractEmails(url, depth, print_log=False, ssl_verify=True, user_agent=None, request_delay=0.0)
			emails = em.emails
			for email in emails:
				all_emails = all_emails + email + ","

		except Exception as e:
			logging.debug("EmailPhoneSpider;Error on Phone Number Extraction for URL=%s; Error: %s ",url,traceback.format_exc())	
		
		logging.warning("EmailPhoneSpider;Email Extraction completed for URL: %s",url)
		return all_emails.strip(",")

	def load_csv(self,name):
		urls = []
		with open(name, 'r') as file:
			reader = csv.reader(file)
			for row in reader:

				urls.append(row[0])
		return urls

scraper = PhoneEmailScraperLite()
if len(sys.argv) < 3:
	print("General Usage > python scrapy.py <csv_file> <pages> \n Pages: 'single': Single Page  && 'all': All internal pages")
else:
	urls = scraper.load_csv(sys.argv[1])
	depth = sys.argv[2]
	scraper.scrape(urls,depth)
