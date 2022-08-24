import requests
import yp_scraper

# For this to work correctly, you need to configure the SMTP function and get your credentials for the Google API functions (sheets)

# Use this function if you'd like to loop through all the companies in all the major industries in a particular city
yp_scraper.industry_crawler('https://www.yellowpages.com/los-angeles-ca')

# Use this function if you want to loop through a particular industry in a specific city
# yp_scraper.crawl_companies("https://yellowpages.com/los-angeles-ca/attorneys")