from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup as bs

class QuoraScraper:
    def __init__(self):
        self.driver = ''
        self.dataframe = ''
        self.credentials = {
            'email': '',
            'password': '',
        }
        self.questions = []
        self.answers = []
        self.links = []
    
    def start_driver(self):
        self.driver = webdriver.Chrome('H:\DOWNLOADS\chromedriver.exe')

    def close_driver(self):
        self.driver.close()

    def open_url(self, url):
        self.driver.get(url)

    # def initialize_columns(self, columns):
    #     self.dataframe = pd.DataFrame(columns=columns)

    def set_credentials(self, email, password):
        self.credentials['email'] = email
        self.credentials['password'] = password

    def login(self):
        self.open_url('https://www.quora.com/')
    
        email_element = self.driver.find_element(By.ID, "email")
        password_element = self.driver.find_element(By.ID, "password")
        time.sleep(5)
        email_element.send_keys(self.credentials['email'])
        time.sleep(5)
        password_element.send_keys(self.credentials['password'])
        time.sleep(5)
        password_element.send_keys(Keys.ENTER)
        
    def open_new(self,keyword):
        self.driver.get("https://www.quora.com/search?q="+keyword+"&time=day&type=answer")
        y = 1000
        for timer in range(0,50):
            self.driver.execute_script("window.scrollTo(0, "+str(y)+")")
            y += 1000  
            time.sleep(1)
    
    def qa(self):
        html = self.driver.page_source
        soup = bs(html,'html.parser')

        a = soup.find_all('span',attrs={"class":"q-box qu-userSelect--text"})
        for i in a:
            self.questions.append(i.text)


        data = soup.findAll('span',attrs={'class':'q-text qu-dynamicFontSize--regular qu-color--blue_dark qu-bold'})
        for div in data:
            lin = div.findAll('a')
            for a in lin:
                self.links.append(a.get('href'))
        
        a = soup.find_all('span',attrs={"class":"q-text qu-truncateLines--3 qu-wordBreak--break-word qt_truncated_inline"})
        for i in a:
            self.answers.append(i.text)

        # print(len(self.questions),len(self.answers),len(self.links))
        

if __name__ == "__main__":
    scraper = QuoraScraper()
    scraper.start_driver()
    username = "USERNAME"
    password = "PASSWORD"
    # scraper.set_credentials(username, password)
    # scraper.login()
    keyword = "Python"
    scraper.open_new(keyword)
    scraper.qa()
    scraper.close_driver()
