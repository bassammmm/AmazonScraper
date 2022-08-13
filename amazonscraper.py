import requests
import bs4
import time


class AmazonScraper:
    def __init__(self,time_interval,base_url,search_query,max_tries):
        self.time_interval = time_interval
        self.base_url = base_url
        self.search_query = search_query
        self.last_query_time = 0
        self.max_tries = max_tries
        self.get_search_query_result()



    def make_url(self,page):
        q = search_query.split(' ')
        if len(q)>1:
            q = "+".join(q)
        else:
            q = q[0]

        url = f"https://www.amazon.com/s?k={q}&s=date-desc-rank&page={page}"
        return url


    def get_max_page_search(self):
        url = self.make_url(1)
        response = self.request_proxy(url)

        soup = bs4.BeautifulSoup(response.text,'lxml')

        paginations = soup.find_all("span",attrs={"class":["s-pagination-item"]})
        print(paginations)
        for each in paginations:
            print(each)


    def get_search_query_result(self):

        self.get_max_page_search()












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
            if response.status_code==200:
                print("Done")
                return response
        if not response:
            print("><----Request Proxy Error----><")
        print("Done")
        return response

if __name__ == '__main__':

    base_url = 'https://www.amazon.com/'
    time_interval = 1
    search_query = 'Apple'
    max_tries = 20
    AmazonScraper(time_interval,base_url,search_query,max_tries)