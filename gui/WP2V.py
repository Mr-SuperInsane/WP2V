import PySimpleGUI as sg
from numpy import size
from main import check_pv
import datetime
import pandas as pd

# PySimpleGUI
# column1 setting
frame1 = sg.Frame('',[
    [sg.Text('【必須項目】')],
    [sg.Text('メールアドレスまたはユーザー名')],
    [sg.InputText(key='mail')],
    [sg.Text('パスワード')],
    [sg.InputText(key='password')],
    [sg.Text('ブログのURL')],
    [sg.InputText(default_text='https://',key='url')],
    [sg.Text('検索件数')],
    [sg.InputText(default_text='10',key='hit')],
    [sg.Text('【オプション】')],
    [sg.Text('CSVファイルに保存しますか？')],
    [sg.Checkbox('保存する',key='csv')],
    [sg.Text('保存するファイル名を入力してください(任意)')],
    [sg.InputText(key='csv_name')]
],title_location=sg.TITLE_LOCATION_TOP)
# block
frame2 = sg.Frame('',[
    [sg.Text('【使用方法】')],
    [sg.Text('''
    (1)左の[必須事項]にwordpressに登録しているメールアドレス・
    パスワードおよびサイトのURL・検索件数を入力してください。
    (2)[オプション]はご自由に選択してください。
    (3)最後に下の[実行]を押してください
    
    ※実行すると[アクセスの許可]を求められる場合がありますが
    [許可]を押してください。また実行するとコンソールが
    表示されますが閉じずに放置しておいてください。
    ''')],
    [sg.Button('実行', key='Enter', size=(51,10))]
])

layout = [
    [sg.Text('【WP2V】',font=('meiryo',20))],
    [sg.Text('WP2VはあなたのブログのPV数を測定します。毎日の測定により1日あたりの記事別のPV数を確認することができます')],
    [frame1,frame2],
    [sg.Text('実行結果')],
    [sg.Multiline(key='result',size=(108,15), justification='left')]
]

#event
window = sg.Window('ウィンドウタイトル',layout)
while True:
    event, value = window.read()
    if event == None:
        break

    if event == 'Enter':
        #必須事項 処理
        mailaddress = value['mail']
        password = value['password']
        hit = value['hit']
        url = value['url']
        if mailaddress and password and hit and url:
            url = f'{url}/wp-admin/edit.php'
            title_list, pv_list = check_pv(mailaddress,password,hit,url)
            #設定 処理
            if value['csv'] == True:
                data = list(zip(title_list, pv_list))
                df =  pd.DataFrame(data, columns=['【記事のタイトル】','【PV数】'])
                if value['csv_name']:
                    file_name = value['csv_name']
                else:
                    file_name = datetime.date.today()
                file_path = r'./download_csv/'
                df.to_csv(file_path+str(file_name)+'.csv',index=False)
            data = list(zip(title_list,pv_list))
            df = pd.DataFrame(data, columns=['記事のタイトル','PV数'])
            window['result'].update(df)
        else:
            sg.popup('入力データが不足しています',title='エラー')

window.close()