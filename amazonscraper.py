import requests
import bs4
import time
import pandas
import datetime

class AmazonScraper:
    def __init__(self,time_interval,base_url,search_query,max_tries):
        self.time_interval = time_interval
        self.base_url = base_url
        self.search_query = search_query
        self.last_query_time = 0
        self.max_tries = max_tries
        self.excel_name = datetime.datetime.today().strftime("%H_%M_%S.xlsx")

        self.data = []
        self.search_each_page()





    def search_each_page(self):

        max_pages = self.get_max_page_search()

        for page in range(1, max_pages + 1):
            url = self.make_url(page)
            response = self.request_proxy(url)
            soup = bs4.BeautifulSoup(response.text, 'lxml')

            products_on_page = soup.find_all("div",attrs={"class":["s-result-item"]})
            self.scrape_product_information(products_on_page)



    def scrape_product_information(self,products):

        for each in products[1:]:

            product_a = each.find_all("a", attrs={"class": ["s-underline-link-text", "a-text-normal"]})

            p_a = 0
            if product_a == []:
                continue
            for x in product_a:
                if 'feedback' in x.text:
                    continue
                p_a = x
                break
            product_href = p_a["href"]
            product_href = self.base_url + product_href
            try:
                product_name = p_a.find_all("span")[0].text
            except:
                continue
            try:
                product_p = each.find_all("span", attrs={"class": ["a-price"]})[0]
                product_price = product_p.text
            except:
                product_price = 0

            product_i = each.find_all("img", attrs={"class": ["s-image"]})[0]
            product_image = product_i["src"]
            print(product_href)
            print(product_name)
            print(product_price)
            print(product_image)


    def get_max_page_search(self):
        url = self.make_url(1)
        response = self.request_proxy(url)

        soup = bs4.BeautifulSoup(response.text,'lxml')

        paginations = soup.find_all("span",attrs={"class":["s-pagination-item"]})
        last_page = paginations[-1]
        last_page = last_page.text
        return int(last_page)


    def make_url(self,page):
        q = search_query.split(' ')
        if len(q)>1:
            q = "+".join(q)
        else:
            q = q[0]

        url = f"https://www.amazon.com/s?k={q}&s=date-desc-rank&page={page}"
        return url















    def request_proxy(self,url):

        time_now = time.time()

        while time_now-self.last_query_time<self.time_interval:
            True

        response = None
        tries=1
        print(f"Trying to get : {url}")
        while not response and tries<=self.max_tries:
            proxies = {
                "http": "http://es365:Spain123_country-gb_session-5zahdlce_lifetime-5s@geo.iproyal.com:22323",
                "https": "http://es365:Spain123_country-gb_session-5zahdlce_lifetime-5s@geo.iproyal.com:22323",
            }

            response = requests.post(url,proxies=proxies)
            print(response)
            if response.status_code==200:
                print("Done")
                return response
            tries+=1
            self.last_query_time=time.time()
        if not response:
            print("><----Request Proxy Error----><")
        print("Done")
        return response

if __name__ == '__main__':

    base_url = 'https://www.amazon.com/'
    time_interval = 1
    search_query = 'Black'
    max_tries = 20
    AmazonScraper(time_interval,base_url,search_query,max_tries)