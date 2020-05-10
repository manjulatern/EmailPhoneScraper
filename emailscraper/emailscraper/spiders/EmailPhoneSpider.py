# -*- coding: utf-8 -*-
import scrapy
from emailscraper.items import EmailscraperItem
import logging, csv, re, traceback

import phonenumbers
from extract_emails import ExtractEmails


class EmailPhoneSpider(scrapy.Spider):
	name = 'emailPhoneSpider'	

	def __init__(self, csv_file='', pages = 'single', *args, **kwargs):
		if pages == "all":
			self.depth = None
		else:
			self.depth = 0
		self.start_urls = []
		if not csv_file:
			logging.error("EmailPhoneSpider;Please upload a CSV File")
			return
		else:
			super(EmailPhoneSpider, self).__init__(*args, **kwargs)
			self.start_urls = self.load_csv(csv_file)

	def parse(self, response):
		logging.info("EmailPhoneSpider;Spider started for URL: %s",response.url)
		item = EmailscraperItem()
		item["url"] = response.url
		item["phone"] = self.extract_phone(response.text,response.url)
		item["email"] = self.extract_email(response.url)
		yield item

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

		logging.info("EmailPhoneSpider;Phone Number Extraction completed for URL: %s",url)
		return number.strip(",")

	def extract_email(self,url):
		all_emails = ""
		try:
			em = ExtractEmails(url, self.depth, print_log=False, ssl_verify=True, user_agent=None, request_delay=0.0)
			emails = em.emails
			for email in emails:
				all_emails = all_emails + email + ","

		except Exception as e:
			logging.debug("EmailPhoneSpider;Error on Phone Number Extraction for URL=%s; Error: %s ",url,traceback.format_exc())	
		
		logging.info("EmailPhoneSpider;Email Extraction completed for URL: %s",url)
		return all_emails.strip(",")
	
	"""
	def extract_phone(self,html_text):
		res = re.findall(r'((\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})',html_text)
		phone_numbers = set()

		for i in range(len(res)):
			try:
				if phonenumbers.is_valid_number(res[i][0]):
					phone_numbers.add(res[i][0])
			except Exception as e:
				print("Not a valid Phone number %s ",res[i][0])

		return phone_numbers

		for num in phone_numbers:
			if num:
				number = number + num + ","
		return number.strip(",")
	"""
	def load_csv(self,name):
		urls = []
		with open(name, 'r') as file:
			reader = csv.reader(file)
			for row in reader:

				urls.append(row[0])
		return urls

