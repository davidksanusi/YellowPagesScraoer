import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import re
import time
import random
import concurrent.futures
import gspread
from datetime import date
from datetime import datetime
from email.message import EmailMessage
import smtplib
import ssl
from urllib.parse import urlparse



headers = requests.utils.default_headers()
headers.update({
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
})

proxies = ['169.57.1.85:8123', '198.206.133.34:8118', '139.59.228.95:8118', '103.161.123.1:30003']
proxies = ['3.226.168.144:80', '128.199.97.42:80', '104.225.220.233:80', '169.57.1.85:8123', '100.19.135.109:80', '165.227.71.60:80', '47.245.33.104:12345', '143.244.132.11:80', '162.243.174.235:80', '201.217.49.2:80', '167.172.158.85:81', '213.222.34.200:53281', '190.196.176.5:60080', '160.16.209.7:3128', '143.198.242.86:8048', '105.28.176.41:9812', '134.122.58.174:80', '193.31.27.123:80', '198.59.191.234:8080', '121.1.41.162:111', '190.214.52.226:53281', '104.45.128.122:80', '71.19.249.118:8001', '103.161.123.1:30003', '167.172.173.210:37823', '104.244.75.218:8080', '80.48.119.28:8080', '130.41.47.235:8080', '20.222.136.61:8000', '74.208.177.198:80', '58.27.59.249:80', '8.214.4.72:33080', '85.70.210.30:80', '68.183.185.62:80', '74.205.128.200:80', '5.58.110.249:8080', '154.236.189.27:8080', '218.39.136.163:8000', '198.206.133.34:8118', '117.102.202.215:8080', '103.151.177.197:9812', '109.194.101.128:3128', '37.143.126.113:80', '103.81.114.182:53281', '216.176.187.99:8886', '196.1.97.209:80', '138.91.159.185:80', '34.87.84.105:80', '204.16.1.169:82', '144.91.123.26:80', '208.109.191.184:80', '43.255.113.232:8082', '167.172.150.160:80', '3.144.107.123:80', '167.99.236.14:80', '52.200.191.158:80', '213.97.45.73:8083', '152.44.40.139:5566', '129.41.171.244:8000', '34.75.202.63:80', '1.214.62.61:8000', '52.168.34.113:80', '216.137.184.253:80', '194.67.91.153:80', '176.223.143.230:80', '177.73.186.12:8080', '223.171.84.181:8000', '138.197.102.119:80', '95.216.12.141:22209', '14.177.236.212:55443', '187.95.112.36:6666', '144.217.7.157:9300', '43.228.125.189:8080', '118.172.187.127:8080', '85.173.165.36:46330', '67.212.186.99:80', '160.16.139.152:3128', '114.4.104.254:3128']


gc = gspread.service_account(filename="/Users/David/PycharmProjects/yp-scraper/creds.json")
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m3S0MgCRZxXp1aG-em2Fzovnf1hABfJ4BGrY3p95p0s/edit#gid=105903045').get_worksheet(4)
sh2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m3S0MgCRZxXp1aG-em2Fzovnf1hABfJ4BGrY3p95p0s/edit#gid=105903045').get_worksheet(6)
sh3 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m3S0MgCRZxXp1aG-em2Fzovnf1hABfJ4BGrY3p95p0s/edit#gid=105903045').get_worksheet(7)
sh4 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m3S0MgCRZxXp1aG-em2Fzovnf1hABfJ4BGrY3p95p0s/edit#gid=105903045').get_worksheet(8)

print(sh3)

def url_getter(url):

    response = requests.get(url, headers=headers,  timeout=5).content
    soup = BeautifulSoup(response, "html.parser")

    return soup


def industry_crawler(url):
    worked = False
    tries = 1

    print("INDUSTRY CRAWLER - FUNCTION #2")
    print(f"TRYING TO CONNECT TO: {url}")
    while not worked:
        try:
            # prox = random.choice(proxies)
            cur = url_getter(url)
            time.sleep(random.randint(0,10))
            print("MADE CONNECTION")
            cur_results = cur.find("section", {"class": "popular-cats"})
            industries = cur_results.find_all("a")
            print("INDUSTRIES CAPTURED")

            print("INDUSTRY EXTRACTOR - FUNCTION #3")
            for i in industries[:19] + industries[40:]:
                industry_extractor(i)

            worked = True

        except Exception as e:
            print(f'FUNCTION 2 FAILED WITH {tries} failed tries')
            print(e)
            # print(f"{prox} failed")
            tries += 1
            time.sleep(1)


def crawl_companies(url):
    worked = False
    tries = 1

    while not worked:
        try:
            # prox = random.choice(proxies)
            cur = url_getter(url)
            time.sleep(random.randint(0,10))
            cur_results = cur.find("div", {"class": "search-results organic"})
            companies = cur_results.find_all("div", {"class": "result"})

            for i in companies:
                try:
                    web = i.find("a", {"class": "track-visit-website"})['href']
                    website = urlparse(web).netloc
                    db = sh3.col_values(1)

                    if website not in db:
                        end_link = i.find("a", {"class": "business-name"})['href']
                        link = f"https://yellowpages.com{end_link}"
                        print(f"{link} available for scraping")
                        sh3.insert_row([website], 1)
                        company_extractor(link, website)
                    else:
                        print("We already scraped this company")
                except:
                    print("Company does not have a website.")

                time.sleep(1)

            worked = True
            sh.insert_row([url], 3)


        except Exception as e:
            print(f'{tries} failed tries')
            print(e)
            # print(f"{prox} failed")
            tries += 1
            time.sleep(1)


def company_extractor(url, company_web):
    worked = False
    tries = 1

    while not worked:
        try:
            # prox = random.choice(proxies)
            cur = url_getter(url)
            time.sleep(random.randint(0, 10))
            if cur.find("a", {"class": "email-business"}):
                email = cur.find("a", {"class": "email-business"})
                phone = "n/a"
                address = "n/a"
                mail = email['href'][7:]
                company = "n/a"

                try:
                    data = cur.find("h1", {"class": "dockable business-name"})
                    company = data.text

                except:
                    print(f"Company name not available")

                try:
                    data = cur.find("a", {"class": "phone dockable"})
                    phone = data['href'][4:]

                except:
                    print(f"{company} phone not available")

                try:
                    addr = cur.find("span", {"class": "address"})
                    address = addr.text
                except:
                    print(f"{company} address not available")

                today = date.today()

                date_scraped = f"{today.strftime('%b-%d-%Y')}"

                # Current time
                curtime = datetime.now().strftime('%b-%d-%Y %H:%M:%S')

                business_years = ""
                company_data = [company, mail, phone, company_web, address, url, date_scraped, curtime]
                print(f"Extracted {company_data}")
                # print(f"It took {tries} tries to work! Thank you {prox}")

                db_check(mail, company_data, date_scraped)

            else:
                print(f"{url} does not have an email.")
            worked = True

        except Exception as e:
            print(f'{tries} failed tries')
            print(e)
            # print(f"{prox} failed")
            tries += 1
            time.sleep(1)


def db_check(uid, info, scraped_day):
    db = sh4.col_values(2)

    if uid in db:
        print("This email is a duplicate")

    else:
        sh4.insert_row(info, 2)
        print("company data inserted")

        send_email(uid, scraped_day)
        print("Email sent")



def send_email(email_receiver, date_checker):
    worked = False

    subject1 = 'Improving Your Business'
    subject2 = 'Automating Your Business'
    subject3 = 'Business Automation Opportunity'

    body1 = '''Hello - I saw your services on Yellow Pages and wanted to see if you had any problems running your business.\n\nI help decrease operating expenses and alleviate heavy workloads by automating existing workflows without having to change the way you do business.\n\n\nHere are some example use cases that can be implemented in your business:\n\n - [Problem 1] You collect orders through google forms, manually input the information into an invoice document, and then email it.\n - [Solution 1] I would create a Google AppScript function that automatically converts the form response into an invoice templated document and emails it to the customer after they submit the form.\n\n - [Problem 2] You run a plumbing business where you manually have to give different quotes to customers depending on their needs.\n - [Solution 2] I would build out a dynamic contact form that takes in a variety of answers from the customer and once they submit the form, they'll be given an accurate quotation (or a rough estimate) of what their project will cost.\n\n - [Problem 3] You want to sell something to real estate agents so you go to a site like realtor . com and manually type the data you find into a spreadsheet.\n - [Solution 3] I would create a script that automatically goes to this website and extract the information you need at a faster and more scalable pace.\n\n - [Problem 4] You run an eBay store where you spend 2 hours a day posting/deleting products and making sure everything matches your company website.\n - [Solution 4] I would create a central database that compiles the product information and would make a bot that posts and deletes products as needed.\n\n - [Problem 5] You have a pizza truck that uses a POS containing various customer data and you need help identifying the locations that made you the most money and on which days.\n - [Solution 5] I would build a script that takes the exported data from your POS and input it into a simple database like Google Sheets and use that to create a dashboard that presents an analytical visualization of trends among your customers and their buying patterns.\n\n\nHopefully, this gives you an idea of the type of tasks that can be accomplished while minimizing your operational costs and time spent doing these manually.\n\nIf you're interested in this or have an idea of how I can help, I'd like to hop on a quick call to better understand your business needs and see what solutions we could implement.\n\nI look forward to your response.\n\nBest,\nDavid Sanusi'''
    body2 = '''Hello - I saw your services on Yellow Pages and wanted to see if you needed help automating reptetitve, costly, and time consuming tasks.\n\nI help decrease operating expenses and alleviate heavy workloads by automating existing workflows without having to change the way you do business. \n\nIf you're interested in this or have an idea of how I can help, I'd like to hop on a quick call to better understand your business needs and see what solutions we could implement.\n\nI look forward to your response.\n\nBest,\nDavid Sanusi'''

    subjects = [subject1, subject2, subject3]
    bodies = [body1, body2]

    subject = random.choice(subjects)
    body = random.choice(bodies)

    email_sender = "kayusidigital@gmail.com"
    email_password = "rwmkhokhhkgdtrby"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    while not worked:
        try:
            dates = sh4.col_values(7)
            emails_sent = dates.count(date_checker)
            if emails_sent < 500:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())
                    print(f"Success! You've sent {emails_sent} emails today.")

                worked = True
        except Exception as e:
            print(e)
            time.sleep(43200)
            print("Email limit reached. Sleeping for 12 hours")


def industry_extractor(industry):
    worked = False
    tries = 1

    while not worked:
        try:
            # prox = random.choice(proxies)
            end_link = industry['href']
            link = f"https://yellowpages.com{end_link}"

            print("GETTING INDUSTRY")
            new_cur = url_getter(link)
            time.sleep(random.randint(0, 10))
            new_cur_results = new_cur.find("div", {"class": "search-results organic"})
            companies = new_cur_results.find_all("div", {"class": "result"})

            pages = new_cur.find("div", {"class": "pagination"})
            num_pages = pages.span.text.split(" ")
            total_pages = int(num_pages[-1])
            final_page = (total_pages // 30) - 1
            current_page = 1

            while current_page < final_page:
                new_url = f"{link}?page={current_page}"
                print(f"SCRAPING {new_url}")
                crawl_companies(new_url)
                current_page += 1

            worked = True

        except Exception as e:
            print(f'Function 3 failed with {tries} failed tries')
            print(e)
            # print(f"{prox} failed")
            tries += 1
            time.sleep(1)

industry_crawler('https://www.yellowpages.com/los-angeles-ca')

