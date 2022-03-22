from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import schedule

mail_username = 'naokun'
password = 'Naokunconsulting8282/wordpress'
wp_edit = 'https://nao-consulting.net/wp-admin/edit.php'

date_number = 2
def check_pv():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('mywp2v-505293b83604.json', scope)
    gc = gspread.authorize(credentials)
    SPREADSHEET_KEY = '1Rs8Q01HwJdBPLrxme60rBSZm5aUR8pm6CkQNZzZ-r9w'
    worksheets = gc.open_by_key(SPREADSHEET_KEY).worksheets()
    worksheet = worksheets[0]
    worksheet2 = worksheets[1]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.get(wp_edit)
    global mail_username
    driver.find_element_by_id('user_login').send_keys(mail_username)
    global password
    driver.find_element_by_id('user_pass').send_keys(password)
    driver.find_element_by_id('wp-submit').click()
    global date_number
    all_id = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/div[1]/div[3]/span[1]').text
    all_id = all_id.replace('個の項目','')
    title_list = []
    id_list = []
    pv_list = []
    if date_number == 1:
        sheet_num = int(all_id) + 1
        n = 1
        while True:
            try:
                title_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[1]/strong/a'
                id_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[8]'
                pv_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[7]'
                title = driver.find_element_by_xpath(title_path).text
                id = driver.find_element_by_xpath(id_path).text
                pv = driver.find_element_by_xpath(pv_path).text
                pv = pv.replace(' ビュー','')
                print(f'タイトル={title}・ID={id}、PV={pv}')
                print(f'n={n}・sheet_num={sheet_num}')
                worksheet.update_cell(sheet_num,1,title)
                #worksheet2.update_cell(sheet_num,1,title)
                worksheet.update_cell(sheet_num,2,id)
                #worksheet2.update_cell(sheet_num,2,id)
                worksheet.update_cell(sheet_num,3,pv)
                if n == 1:
                    date = datetime.datetime.now().strftime('%m/%d')
                    worksheet.update_cell(1,3,date)
                if n % 50 == 0 :
                    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/div[2]/div[3]/span[2]/a[1]').click()
                    sleep(1)
                    n = 0
                sheet_num -= 1
                n += 1
                sleep(2)
            except:
                break

    else:
        sheet_num = int(all_id) + 1
        print(sheet_num)
        n = 1
        column_number = date_number + 2
        while True:
            try:
                title_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[1]/strong/a'
                id_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[8]'
                pv_path = f'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/table/tbody/tr[{n}]/td[7]'
                title = driver.find_element_by_xpath(title_path).text
                id = int(driver.find_element_by_xpath(id_path).text)
                pv = driver.find_element_by_xpath(pv_path).text
                pv = int(pv.replace(' ビュー',''))
                title_list.append(title)
                id_list.append(id)
                pv_list.append(pv)
                title_data = worksheet.cell(sheet_num,2).value
                if title_data == id:
                    worksheet.update_cell(sheet_num,column_num,pv)
                else:
                    worksheet.update_cell(sheet_num,1,title)
                    sleep(0.5)
                    worksheet2.update_cell(sheet_num,1,title)
                    worksheet.update_cell(sheet_num,2,id)
                    sleep(0.5)
                    worksheet2.update_cell(sheet_num,2,id)
                    worksheet.update_cell(sheet_num,column_number,pv)
                if n == 1:
                    date = datetime.datetime.now().strftime('%m/%d')
                    column_num = date_number + 2
                    worksheet.update_cell(1,column_num,date)
                if n % 50 == 0 :
                    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/form[1]/div[2]/div[3]/span[2]/a[1]').click()
                    sleep(1)
                    n = 0 
                n += 1
                sleep(1)
                a = date_number + 1
                b = date_number + 2
                c = date_number + 1
                day1_pv = worksheet.cell(sheet_num,a).value
                day1 = worksheet.cell(1,a).value
                day2_pv = worksheet.cell(sheet_num,b).value
                day2 = worksheet.cell(1,b).value
                print(f'aは{a}、bは{b}、cは{c}、sheet_numは{sheet_num}')
                print(f'day1={day1_pv}、day2={day2_pv}')
                day1_pv = int(day1_pv)
                day2_pv = int(day2_pv)
                day2_day1 = day2_pv - day1_pv
                worksheet2.update_cell(sheet_num, c, day2_day1)
                date_data = str(day1)+'～'+str(day2)
                worksheet2.update_cell(1, c, date_data)
                sheet_num -= 1
                sleep(1)
            except:
                break

    date_number += 1
    driver.quit()

check_pv()
#schedule.every().day.at('14:50').do(check_pv)
#schedule.every(3).minutes.do(check_pv)
# while True:
#     schedule.run_pending()
#     sleep(1)
