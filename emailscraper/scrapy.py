import os
import subprocess
import sys

class PhoneEmailScraperLite():

	def runSpider(self,csv_file,pages):
		try:
			proc = subprocess.Popen(['scrapy crawl emailPhoneSpider -a csv_file='+ csv_file +' -a pages='+ pages+''],shell=True)
		except subprocess.CalledProcessError as cperr:
			print("Subprocess Error while scraping" + str(cperr))

scraper = PhoneEmailScraperLite()
if len(sys.argv) < 3:
	print("\nGeneral Usage > python scrapy.py <csv_file> <pages> \n Pages: 'single': Single Page  && 'all': All internal pages\n")
else:
	csv_file = sys.argv[1]
	pages = sys.argv[2]
	scraper.runSpider(csv_file,pages)