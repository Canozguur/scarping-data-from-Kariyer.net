from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


class start:
    def __init__(self):
        self.basic()


    def basic(self):
        search_word = input("WHAT YOU WANNA SEARCH WRITE : ")
        self.url = f"https://www.kariyer.net/is-ilanlari/#&kw={search_word}"
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)
        self.find_jobs()
    def find_jobs(self):
        jobs = self.driver.find_elements_by_class_name("ilan")

        for i in range(len(jobs)):
            time.sleep(1)
            self.driver.get(self.url)
            jobs = self.driver.find_elements_by_class_name("ilan")
            try:
                data = jobs[i].find_element_by_class_name("col-9").text
                self.name_of_job, self.company_of_job, self.city_of_job = str(data).split("\n")
                self.link = jobs[i].find_element_by_xpath(f'//*[@id="ilan{i}"]/div/div[2]/p[2]/a').get_attribute("href")
                print(self.link)
                self.link_git()

            except Exception:
                print("Hata alındı")

    def print(self):
        print("Name of Job :", self.name_of_job)
        print("Company of Job :", self.company_of_job)
        print("City of Job :", self.city_of_job)

    def link_git(self):
        self.driver.get(self.link)
        time.sleep(2)
        data = self.driver.find_elements_by_class_name("info-item")
        for infolar in data:
            title = infolar.find_element_by_class_name("title").text
            description = infolar.find_element_by_class_name("description").text
            print("TITLE :",title,"\n","RESULT",description)

start()
