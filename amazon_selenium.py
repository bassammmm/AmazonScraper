import requests
import bs4
import time
import pandas
import datetime
from undetected_chromedriver import Chrome, ChromeOptions
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AmazonScraper:
    def __init__(self,time_interval,base_url,search_query,max_tries):
        self.time_interval = time_interval
        self.base_url = base_url
        self.search_query = search_query
        self.last_query_time = 0
        self.max_tries = max_tries

        q = self.search_query.split(" ")
        if len(q)>1:
            q = "_".join(q)
        else:
            q = q[0]
        self.excel_name = datetime.datetime.today().strftime(f"{q}_%H_%M_%S.xlsx")

        self.data = []
        self.search_each_page()





    def search_each_page(self):


        option = ChromeOptions()
        option.headless=True
        option.add_argument("window-size=1920,1080")
        self.driver = Chrome(options=option)
        self.driver.get("https://www.amazon.com/")
        self.driver.maximize_window()

        search_bar = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#twotabsearchtextbox")))

        search_bar.send_keys(self.search_query)

        search_bar.send_keys(Keys.ENTER)

        el = self.driver.find_element(By.ID,'s-result-sort-select')
        for option in el.find_elements(By.TAG_NAME,'option'):
            if 'newest arrivals' in option.text.lower():
                print("found")
                option.click()
                break

        time.sleep(5)

        while True:

            current_scroll_position, new_height = 0, 1
            while current_scroll_position <= new_height:
                current_scroll_position += 8
                self.driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
                new_height = self.driver.execute_script("return document.body.scrollHeight")

            try:
                next_page = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"a.s-pagination-next")))
            except:

                break
            time.sleep(5)

            print(f"SCRAPING URL :::::::  {self.driver.current_url}")
            print("===========================================================================================================================================================================================================================================")
            print("===========================================================================================================================================================================================================================================")
            print("===========================================================================================================================================================================================================================================")



            page_html = self.driver.page_source
            soup = bs4.BeautifulSoup(page_html, 'lxml')

            products_on_page = soup.find_all("div", attrs={"class": ["s-result-item"]})
            self.scrape_product_information(products_on_page)




            classes = next_page.get_attribute("class")


            if "s-pagination-disabled" in classes:
                break


            next_page.click()

        self.write_to_excel()

    def scrape_product_information(self,products):

        for each in products[1:]:

            product_a = each.find_all("a",attrs={"class":["s-underline-link-text","a-text-normal"]})

            p_a = 0
            if product_a==[]:
                continue
            for x in product_a:
                if 'feedback' in x.text:
                    continue
                p_a = x
                break
            product_href = p_a["href"]
            product_href = self.base_url+product_href
            try:
                product_name = p_a.find_all("span")[0].text
            except:
                continue
            try:
                product_p = each.find_all("span",attrs={"class":["a-price"]})[0]
                product_price = product_p.text
            except:
                product_price = 0

            product_i = each.find_all("img",attrs={"class":["s-image"]})[0]
            product_image = product_i["src"]
            print("===========================================================================================================================================================================================================================================")
            print(product_href)
            print(product_name)
            print(product_price)
            print(product_image)

            self.data.append([product_href,product_name,product_price,product_image])


    def write_to_excel(self):
        headers = ["LINK","NAME","PRICE","IMAGE"]
        df = pandas.DataFrame(self.data,columns=headers)
        df.to_excel(self.excel_name)

if __name__ == '__main__':

    base_url = 'https://www.amazon.com/'
    time_interval = 1
    search_query = 'Red Keyboards'
    max_tries = 20
    AmazonScraper(time_interval,base_url,search_query,max_tries)

    