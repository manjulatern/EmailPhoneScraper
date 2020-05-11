import os
import subprocess
import sys

class PhoneEmailScraperLite():

	def runSpider(self,csv_file,depth):
		try:
			proc = subprocess.Popen(['scrapy crawl emailPhoneSpider -a csv_file='+ csv_file +' -a depth='+ depth+''],shell=True)
			print("Process ID is: "+str(proc.pid))
		except subprocess.CalledProcessError as cperr:
			print("Subprocess Error while scraping" + str(cperr))

scraper = PhoneEmailScraperLite()
if len(sys.argv) < 3:
	print("\nGeneral Usage > python scrapy.py <csv_file> <depth> \n Depth: 0 : Single Page; [integer]:  Number of Links in the page  && None: All internal pages\n")
else:
	csv_file = sys.argv[1]
	depth = sys.argv[2]
	scraper.runSpider(csv_file,depth)