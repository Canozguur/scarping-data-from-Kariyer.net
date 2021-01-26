from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from xlsxwriter import Workbook

Job_Name= []
Company_Name =[]
City = []
Tel_No =[]
Sektör = []
Çalışan_Sayısı = []
Kuruluş_Yılı = []
Web_Site = []
Adres = []
data = {"Job_Name":[],
        "Company_Name":[],
        "City":[],
        "Tel_No":[],
        "Sektör":[],
        "Çalışan_Sayısı":[],
        "Kuruluş_Yılı":[],
        "Web_Site":[],
        "Adres":[]}
index =[]


# print("Name of Job :", self.name_of_job)
# print("Company of Name :", self.company_of_job)
# print("City of Job :", self.city_of_job)
# print("Company of Tel No :", self.tel__no)

search_word = input("WHAT YOU WANNA SEARCH WRITE : ")


class start:
    def __init__(self):
        self.basic()



    def basic(self):
        # Burası çalışıyormu emin değilim daha
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(f"https://www.kariyer.net/is-ilanlari/#&kw={search_word}+&cp={1}")
        last_page = int(str(self.driver.find_element_by_class_name("last").text).split(" ")[0])

        for j in range(1,last_page):

            self.url = f"https://www.kariyer.net/is-ilanlari/#&kw={search_word}+&cp={j}"
            self.driver.get(self.url)

            self.find_jobs()

    def find_jobs(self):
        jobs = self.driver.find_elements_by_class_name("ilan")

        for i in range(2,len(jobs)):  # len(jobs)
            time.sleep(1)
            self.driver.get(self.url)
            try:

                jobs = self.driver.find_elements_by_class_name("ilan")
                data = jobs[i].find_element_by_class_name("col-9").text
                self.name_of_job, self.company_of_job, self.city_of_job = str(data).split("\n")
                self.link = jobs[i].find_element_by_xpath(f'//*[@id="ilan{i}"]/div/div[2]/p[2]/a').get_attribute("href")
                print(self.link)
                self.link_git()
                self.print()
            except Exception:
                print("Hata Alındı")


    def print(self):
        print("Name of Job :", self.name_of_job)
        print("Company of Name :", self.company_of_job)
        print("City of Job :", self.city_of_job)
        print("Company of Tel No :", self.tel__no)
        index.append(self.company_of_job)
        Job_Name.append(self.name_of_job)
        Company_Name.append(self.company_of_job)
        City.append(self.city_of_job)
        Tel_No.append(self.tel__no)
        if len(Sektör) != len(Job_Name):
            Sektör.append("-")
        if len(Kuruluş_Yılı) != len(Job_Name):
            Kuruluş_Yılı.append("-")
            Çalışan_Sayısı.append("-")
            Web_Site.append("-")
            Adres.append("-")
        print(len(Sektör),len(Job_Name))
    def link_git(self):
        self.driver.get(self.link)
        time.sleep(2)
        data = self.driver.find_elements_by_class_name("info-item")
        for infolar in data:
            sektor = "-"
            kurulus_yili = "-"
            calisansayi = "-"
            web_site = "-"
            address = "-"
            title = infolar.find_element_by_class_name("title").text
            description = infolar.find_element_by_class_name("description")

            try :
                if str(title) == "Sektör":
                    sektör = description.text
                    Sektör.append(sektör)
                elif str(title) == "Kuruluş Yılı":
                    kurulus_yili = description.text
                    if description.text:
                        Kuruluş_Yılı.append(kurulus_yili)
                    else:
                        Kuruluş_Yılı.append("-")

                elif str(title) == "Çalışan Sayısı":
                    calisansayi = description.text
                    Çalışan_Sayısı.append(calisansayi)
                elif str(title) == "Web Sitesi":
                    Web_Site.append(description.get_attribute("href"))
                elif str(title) == "Adres":
                    address = description.text
                    Adres.append(address)
            except Exception:
                Sektör.append(sektor)
                Kuruluş_Yılı.append(kurulus_yili)
                Çalışan_Sayısı.append(calisansayi)
                Web_Site.append(web_site)
                Adres.append(address)

            print(title, ":", description.text, end="")
            print()
            #print("TITLE :",title,"\n","RESULT",description)

        self.find_tel_no()

    def find_tel_no(self):
        self.driver.get("https://www.google.com/search?q="+str(self.company_of_job))
        tel_no = self.driver.find_elements_by_class_name("Z1hOCe")
        for i in tel_no:
            try:
                tel,self.tel__no = str(i.text).split(":")
                if tel == "Telefon":
                    break
            except Exception:
                print("adres yeri")
        print(self.tel__no)
start()

data['Job_Name'] = Job_Name
data['Company_Name'] = Company_Name
data['City'] = City
data['Tel_No'] = Tel_No
data['Sektör'] = Sektör
data['Çalışan_Sayısı'] = Çalışan_Sayısı
data['Kuruluş_Yılı'] = Kuruluş_Yılı
data['Web_Site'] = Web_Site
data['Adres'] = Adres
print(len(Job_Name),len(Company_Name),len(City),len(Tel_No),len(Sektör),len(Çalışan_Sayısı),len(Kuruluş_Yılı),len(Web_Site),len(Adres))
df = pd.DataFrame(data, columns=['Job_Name',"Company_Name","City","Tel_No","Sektör","Çalışan_Sayısı","Kuruluş_Yılı","Web_Site","Adres",],index=index)

writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name=f'{search_word}')
writer.save()
print(df)



