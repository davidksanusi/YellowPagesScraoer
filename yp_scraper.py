import requests
from bs4 import BeautifulSoup
import time
import random
import gspread
from datetime import date
from datetime import datetime
import gmail
import proxy_rotation
import google_sheets
import site_analysis



def url_getter(url):

    # THERE WILL BE TWO SCRAPING OPTIONS BELOW

    # 1) THE FIRST FUNCTION IS USING THE FREE PROXY SERVICE.
    #    This service will pull the most up-to-date free proxies and will be rotated on each request.
    #    Because the proxies are free, that means they will most likely be blocked on a lot of the requests.
    #    This function automatically retries a random proxy in the list until success.

    # To scrape with the proxy, uncomment this function bellow and comment out function #1

    return proxy_rotation.url_getter_wp(url)

    # 2) THE SECOND FUNCTION IS USING YOUR PERSONAL IP ADDRESS
    #    This will allow you to scrape the website much faster due to less failed requests.
    #    I recommend you keep the time.sleep in place so that you are adhering to general webscraping ethics and codes of conduct.
    #    This will reduce your chances of being blocked by the website.


    # headers = requests.utils.default_headers()
    # headers.update({
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #     'Accept-Language': 'en-US,en;q=0.5',
    #     'Connection': 'keep-alive',
    #     'Upgrade-Insecure-Requests': '1',
    #     'Cache-Control': 'max-age=0'
    # })
    #
    # tries = 0
    # connected = False
    # while not connected:
    #     print(f"Sending request to {url}")
    #     try:
    #         response = requests.get(url, headers=headers, timeout=5).content
    #         soup = BeautifulSoup(response, "html.parser")
    #         print(f"Successfully connected! It took {tries} tries")
    #         connected = True
    #     except Exception as e:
    #         print(e)
    #         print(f"Try #{tries}: Failed to connect to site. Trying again...")
    #         tries += 1
    #
    #     time.sleep(random.randint(0, 10))
    #     return soup

def industry_crawler(url):
    worked = False
    tries = 1

    print("INDUSTRY CRAWLER - FUNCTION #2")
    print(f"TRYING TO CONNECT TO: {url}")
    while not worked:
        try:
            cur = url_getter(url)
            time.sleep(random.randint(0,10))
            print("MADE CONNECTION")
            cur_results = cur.find("section", {"class": "popular-cats"})
            industries = cur_results.find_all("a")
            print("INDUSTRIES CAPTURED")

            print("INDUSTRY EXTRACTOR - FUNCTION #3")
            for i in industries[60:]:
                industry_extractor(i)

            worked = True

        except Exception as e:
            print(f'FUNCTION 2 FAILED WITH {tries} failed tries')
            print(e)
            tries += 1
            time.sleep(1)

def crawl_companies(url):
    worked = False
    tries = 1

    while not worked:
        try:
            cur = url_getter(url)
            time.sleep(random.randint(0,10))
            cur_results = cur.find("div", {"class": "search-results organic"})
            companies = cur_results.find_all("div", {"class": "result"})

            for i in companies:

                data = i.find("div", {"class": "phones phone primary"})
                phone = data.text
                db = google_sheets.sh2.col_values(1)

                if phone not in db:
                    try:
                        if not i.find("a", {"class": "track-visit-website"}):
                            print("This company does not have a website.")
                        else:
                            website = i.find("a", {"class": "track-visit-website"})['href']
                            print(website)
                            end_link = i.find("a", {"class": "business-name"})['href']
                            print(end_link)
                            link = f"https://yellowpages.com{end_link}"
                            print(f"{link} available for scraping")
                            company_extractor(link, website)
                    except:
                        print("Error something went wrong!")

                    google_sheets.sh2.insert_row([phone], 1)
                    time.sleep(2)

                else:
                    print("Duplicate due to phone number")

            worked = True
            google_sheets.sh.insert_row([url], 3)


        except Exception as e:
            print(f'{tries} failed tries')
            print(e)
            tries += 1
            time.sleep(1)

def company_extractor(url, website):
    worked = False
    tries = 1

    while not worked:
        try:
            cur = url_getter(url)
            time.sleep(random.randint(0, 10))
            if cur.find("a", {"class": "email-business"}):
                email = cur.find("a", {"class": "email-business"})
                phone = ""
                address = ""
                mail = email['href'][7:]
                company = ""
                years_in_business = ""
                years_with_yp = ""
                yp_preferred = "No"
                service = ""

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

                try:
                    data = cur.find("div", {"class": "years-in-business"}).find('div',{"class":"number"}).text
                    years_in_business = int(data)

                except:
                    print(f"{company} years not available")

                try:
                    data = cur.find("div", {"class": "years-with-yp"}).find('div', {"class":"number"}).text
                    years_with_yp = int(data)

                except:
                    print(f"{company} yellow page years not available")

                try:
                    if cur.find("img", {"class": "preferred-badge"}):
                        yp_preferred = "Yes"

                except:
                    print(f"{company} YP preferred not available")


                try:
                    data = cur.find("div", {"class": "categories"}).find_all('a')
                    service = data[0].text

                except:
                    print(f"{company} service not available")

                today = date.today()

                date_scraped = f"{today.strftime('%b-%d-%Y')}"

                # Current time
                curtime = datetime.now().strftime('%b-%d-%Y %H:%M:%S')

                company_data = [company, mail, phone, website, address, url, date_scraped, curtime, years_in_business, years_with_yp, yp_preferred, service]

                seo_data = site_analysis.seo_analyze(website)
                flat_analysis = site_analysis.flatten_dictionary(seo_data)
                restruct_analysis = site_analysis.restruct_data(flat_analysis)

                print(f"Extracted {company_data}")

                db_check(mail, company_data, restruct_analysis)

            else:
                print(f"{url} does not have an email.")
            worked = True

        except Exception as e:
            print(f'{tries} failed tries')
            print(e)
            tries += 1
            time.sleep(1)

def db_check(uid, info, analysis):
    db = google_sheets.sh.col_values(2)
    newe = uid.split("@")
    newemail = newe[0]
    company_name = info[0]

    try:
        if uid in db or int(newemail[-4:]):
            print("This email is invalid")
    except:
        google_sheets.sh.insert_row(info, 3)
        print("company data inserted")

        gmail.send_email(uid, analysis, company_name)
        print("Email sent")

def industry_extractor(industry):
    worked = False
    tries = 1

    while not worked:
        try:
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
            tries += 1
            time.sleep(1)



