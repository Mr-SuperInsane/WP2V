import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('mywp2v-505293b83604.json', scope)
gc = gspread.authorize(credentials)
SPREADSHEET_KEY = '1Rs8Q01HwJdBPLrxme60rBSZm5aUR8pm6CkQNZzZ-r9w'
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
worksheet2 = gc.open_by_key(SPREADSHEET_KEY).get_worksheet(1)
while True:
    a = 3
    b = 4
    c = 3
    sheet_num = 2
    try:
        day1_pv = int(worksheet.cell(sheet_num,a).value)
        day1 = worksheet.cell(1,a).value
        day2_pv = int(worksheet.cell(sheet_num,b).value)
        day2 = worksheet.cell(1,b).value
        day2_day1 = day2_pv - day1_pv
        worksheet2.update_cell(sheet_num,c,day2_day1)
        worksheet2.update_cell(1,c,day1+'-'+day2)
        a += 1
        b += 1
        c += 1
        sheet_num += 1
    except:
        break