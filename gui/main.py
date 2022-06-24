from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pandas as pd
import datetime

def check_pv(mailaddress,password,hit,url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get(url)
    driver.find_element_by_id('user_login').send_keys(mailaddress)
    driver.find_element_by_id('user_pass').send_keys(password)
    driver.find_element_by_id('wp-submit').click()
    n=0
    title_list = []
    pv_list = []

    for n in range(int(hit)):
        n += 1
        title_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[1]/strong/a'
        pv_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[7]'
        title = driver.find_element_by_xpath(title_path).text
        pv = driver.find_element_by_xpath(pv_path).text
        pv = pv.replace(' ビュー','')
        title_list.append(title)
        pv_list.append(pv)
        sleep(0.5)
    
    data = list(zip(title_list,pv_list))
    df = pd.DataFrame(data,columns=['【記事のタイトル】','【PV数】'])
    file_path = r'C:/Users/NAOKUN/Desktop/PV'
    date = datetime.datetime.now()

    df.to_csv(file_path+date.date().strftime('%m/%d')+'.scv',index=False)
    