
import time
from csv import writer
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import SB
import os
os.system('say "Check Scroll."')
os.system('afplay /System/Library/Sounds/Sosumi.aiff')
# Proxy_List = [
#     'http://sekzfhgw:t0iyex3rtzix@107.180.191.36:6729',
#     'http://sekzfhgw:t0iyex3rtzix@193.160.80.230:6498',
#     'http://sekzfhgw:t0iyex3rtzix@192.46.185.231:5921',
#     'http://sekzfhgw:t0iyex3rtzix@45.196.54.54:6633',
#     'http://sekzfhgw:t0iyex3rtzix@130.180.237.178:7121',
#     'http://sekzfhgw:t0iyex3rtzix@130.180.232.109:8547',
#     'http://sekzfhgw:t0iyex3rtzix@104.243.210.75:5723',
#     'http://sekzfhgw:t0iyex3rtzix@192.46.201.208:6722',
# ]

Proxy_List = [
    'http://sekzfhgw:t0iyex3rtzix@130.180.232.90:8528',
    'http://sekzfhgw:t0iyex3rtzix@193.160.82.12:5984',
    'http://sekzfhgw:t0iyex3rtzix@130.180.234.229:7452',
    'http://sekzfhgw:t0iyex3rtzix@192.46.185.0:5690',
    'http://sekzfhgw:t0iyex3rtzix@192.53.137.67:6355',
    'http://sekzfhgw:t0iyex3rtzix@130.180.228.114:6398',
    'http://sekzfhgw:t0iyex3rtzix@192.53.66.152:6258',
    'http://sekzfhgw:t0iyex3rtzix@192.53.67.242:5791',
]
list_data =  []
Start = random.choice(Proxy_List)

#start options
options = {
    'proxy': {
        'http': Start,
        'https': Start,
        'no_proxy':'localhost,127.0.0.1'
    }
}


# chromeOptions =  Options()
# chromeOptions.headless = False
# chromeOptions.add_argument("--headless")
# chromeOptions.add_argument("--disable-gpu")
# chromeOptions.add_argument("--no-sandbox")
# chromeOptions.add_argument("enable-automation")
# chromeOptions.add_argument("--disable-infobars")
# chromeOptions.add_argument("--disable-dev-shm-usage")
# chromeOptions.add_argument('--proxy-server=%s' % PROXY_IP)
driver = webdriver.Chrome(seleniumwire_options=options)
# driver = webdriver.Chrome()
# driver.get('https://ipinfo.io/json')
# print(driver.page_source)





#swap proxys
def swp():
    time.sleep(1)
    Start = random.choice(Proxy_List)
    options = {
        'proxy': {
            'http': Start,
            'https': Start,
            'no_proxy':'localhost,127.0.0.1'
        }
    }
    webdriver.Chrome(seleniumwire_options=options)


#constructor dict/object
class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

#check for dict for same company
checkList = AttrDict()

def initialize_browser():
    #Link start
    driver.get('https://www.bbb.org/search?find_country=USA&find_latlng=46.992603%2C-122.194283&find_loc=Electron%2C%20WA&find_text=medical%20group&page=1&sort=Relevance')
    print("Starting Driver.:.:.")
    time.sleep(5)
    #find next button
    nextButton = driver.find_element(By.XPATH, '//a[text()="Next"]')

    #run scraper while there's a next button
    while nextButton:

        #find business card div
        hold = driver.find_elements(by=By.CLASS_NAME, value="e1ri33r70")

        #loop through all card div 
        for i in hold:

            #try to find title element in card div
            try:
                Title = i.find_element(by=By.CLASS_NAME, value="eou9tt71").text
                #run scrape if checkList dose not find Title Key
                if Title not in checkList:
                    #add title to check list
                    checkList[Title] = Title

                    #check for link and open card div in a new tab and start scrape
                    if (i.find_element(by=By.CLASS_NAME, value="eou9tt70").get_attribute('href') != None):
                        iHREF = i.find_element(by=By.CLASS_NAME, value="eou9tt70").get_attribute('href')
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[1])
                        driver.get(iHREF)
                        

                        #test for rate limit
                        try:
                            if (driver.find_element(By.XPATH, '//a[text()="You are being rate limited"]')):
                                print('fix')
                                os.system('say "Fix."')
                                #close window and switch to page index0
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])

                        #run normal scrape
                        except:

                            try:
                                #Info
                                dbTitle = driver.find_element(by=By.CLASS_NAME, value="bds-h2.font-normal.text-black").text
                                dbPhone = driver.find_element(by=By.CLASS_NAME, value="dtm-phone").text
                                dbAddress = driver.find_element(by=By.TAG_NAME, value="address").text.replace("\n"," ")
                                dbAddressArr = dbAddress.split(",")
                                
                                #append data
                                list_data.append([dbTitle.replace(",",""),dbPhone,dbAddressArr[0].replace(",",""),dbAddressArr[1].replace(",","")])
                                print([dbTitle,dbPhone,dbAddressArr[0],dbAddressArr[1]])

                                #close window and switch to page index0
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                            except:
                                #run on fail
                                print("NA","NA","NA","NA","NA")
                                #close window and switch to page index0
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                            swp()
                #     else:
                #         print('cant find')
                # else:
                #     print('skip')
                #     swp()
            except:
                swp()
        try:
            #click next
            driver.find_element(By.XPATH, '//a[text()="Next"]').click()
            #reminder
            os.system('say "Check Scroll."')
            os.system('afplay /System/Library/Sounds/Sosumi.aiff')

            #scroll
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except:

            #return data
            return list_data
    return list_data

    


#Build csv file
headers = ['Clinic Name','Phone Number','Street','City, State, Zip','Who talked to','Email address of main contact','Results']
initialize_browser()
filename = 'MedicalGroup.csv'
with open(filename, 'a') as file:
    writer_object = writer(file)
    # for header in headers:
    #     file.write(str(header)+', ')
    # writer_object.writerow('Called')
    for row in list_data:
       writer_object.writerow(row)
        # for x in row:
        #     file.write(str(x)+', ')
        # file.write('n')
driver.quit()