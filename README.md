# Install the libraries (Recommended to run inside a virtual environment)
	>> pip install -r requirements.txt

## There are two ways you can run the application. 
1. EmailScraper
	- Uses Scrapy library
	- Folder: emailscraper

2. EmailScraperLite
	- Uses python requests library only
	- Folder: emailscraperlite

# Run the python script with parameters
	
```shell
python scrap.py <csv-file> <pages>
```
#### Parameters:
	1. csv-file : The csv files with all the urls to look for
	2. pages: How many depths you want to go into. 0 for single page. Put other integer for more links.

#### Example 1: python scrapy.py lawyers.csv 0
	* This will run the scraper for all the urls from the file and looks for the content in only the url specified.
#### Example 2: python scrapy.py lawyers.csv all
	* This will run the scraper for all of the urls and goes into every depth of the page.
	* This is time consuming but gets all the details from each and every page of the website.
	* This will look at each and every links of the website, so it will take much longer.
	* This is recommended to use only for some specific URLs where you don't know where the content is.
