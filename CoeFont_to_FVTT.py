import hmac
import requests
import hashlib
import json
from datetime import datetime, timezone
from fastapi import FastAPI, Response, status, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import PySimpleGUI as sg
import threading
import time
import ctypes
import os
import keyring

print('\033[32m' + '⠀⢀⣴⠿⠿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣿⠿⠿⠿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⢀⡄⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⢸⡿⠿⠿⠿⠇ ⣿⡀⠀⠀⠀⢰⡟   ⠿⠿⢿⡿⠿⠿  ⠿⠿⠿⣿⠿⠿⠿' +'\033[0m')
print('\033[32m' + '⢀⣿⠀⠀⠀⠀⠋⠀⠀⢀⣤⣤⣀⠀⠀⠀⣀⣤⣤⡀⠀ ⠀⣿⠀⠀⠀⠀ ⠀⣠⣤⣄⠀⠀⠀⣤⣀⣤⣄⠀⣤⣼⣧⣤⠀⠀⣤⢠⣿⣤⣤ ⠀⢀⣤⣤⣀⠀⠀⠀⠀⠀ ⢸⡇⠀⠀⠀⠀ ⠈⣷⠀⠀⠀⣿⠀⠀⠀   ⢸⡇⠀⠀⠀    ⣿⠀⠀⠀' +'\033[0m')
print('\033[32m' + '⢸⡇⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠙⣧⠀⣾⠃⠀ ⣿⠀ ⠀⣿⠛⠛⠛⠃ ⣿⠀⠀⠈⣿⠀⠀⣿⠀⠀⢸⡇⠀⢸⡇⠀⠀⠀⠀⠀⣿⠀ ⠀⢠⡟⠀  ⠙⣧⠀⠀⠀ ⢸⡟⠛⠛⠛⠀ ⠀⢻⡆⠀⣼⠁⠀⠀    ⢸⡇⠀⠀⠀    ⣿⠀⠀⠀' +'\033[0m')
print('\033[32m' + '⠈⣿⠀⠀⠀⠀⣀⠀⢸⡇⠀⠀⠀⣿⠀⣿⠉⠉⠉⠉⠀⠀ ⣿⠀⠀⠀⠀⠀⣿⠀⠀ ⣿⠀ ⣿⠀⠀⢸⡇⠀⢸⡇⠀⠀⠀⠀⠀⣿⠀ ⠀⢸⡇⠀⠀⠀ ⣿⠀   ⢸⡇⠀⠀⠀⠀  ⠀⣿⢠⡏⠀    ⠀⠀⢸⡇⠀     ⠀⣿⠀⠀⠀' +'\033[0m')
print('\033[32m' + '⠀⠈⠿⣶⣶⡿⠋⠀⠀⠻⣦⣤⠿⠁⠀⠈⠷⣤⣤⠟ ⠀⠀⣿⠀⠀⠀⠀⠀⠙⢶⣤⡾⠋⠀⠀⣿⠀⠀⢸⡇⠀⠈⣷⣴⠀⠀⠀⠀⠹⣦⡦⠀ ⠻⣦⣤ ⠿⠁⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀ ⠘⣿⠀⠀⠀⠀    ⢸⡇⠀     ⠀⣿⠀⠀⠀' +'\033[0m')
print("")
print("")
print('\033[31m' + '注意：アプリを終了するまでこのコマンド画面を閉じないでください' + '\033[0m')

Kernel32 = ctypes.windll.Kernel32
mutex = Kernel32.CreateMutexA(0, 1, "CoeFontConnectorRunning")
result = Kernel32.WaitForSingleObject(mutex, 0) 

class Item(BaseModel):
  text: str
  coefont: str
  volume: float | None = 1.0

class UserOut(BaseModel):
  url: str
  status: str

access_key = ""
client_secret = ""
folder_path = ""
folder_setting = False
k = keyring.get_password("CoeFont", "key")
s = keyring.get_password("CoeFont", "secret")
f = keyring.get_password("CoeFont", "folder")
se = keyring.get_password("CoeFont", "foldersetting")

if k != None:
  access_key = k
if s != None:
  client_secret = s
if f != None:
  folder_path = f
if se != None:
  if se == "False":
    folder_setting = False
  elif se == "True":
    folder_setting = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['POST', 'OPTIONS']
)

def save_wav(url):
  print("RECEIVE URL:" + url)
  dt = datetime.now()
  file_name = str(dt.year) + str(dt.month) + str(dt.day) + str(dt.hour) + str(dt.minute) + str(dt.second) + ".wav"

  global folder_path
  os.makedirs(folder_path, exist_ok=True)
  re = requests.get(url, stream=True)
  with open(os.path.join(folder_path, file_name), 'wb') as f:
    for chunk in re.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
        f.flush()
  print("CREATE FILE:" + folder_path + "/" + file_name)

@app.post("/", response_model = UserOut, status_code=status.HTTP_200_OK)
async def req(item: Item, res: Response, request: Request, background_tasks: BackgroundTasks):
    if request.headers['content-type'] == 'application/json':
        text = item.text
        coefont = item.coefont
        volume = item.volume
        date: str = str(int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()))
        data: str = json.dumps({
            'coefont': coefont,
            'text': text,
            'format': "wav",
            'volume': volume
        })
        global client_secret
        global access_key
        signature = hmac.new(bytes(client_secret, 'utf-8'), (date+data).encode('utf-8'), hashlib.sha256).hexdigest()

        response = requests.post('https://api.coefont.cloud/v1/text2speech', data=data, headers={
          'Content-Type': 'application/json',
          'Authorization': access_key,
          'X-Coefont-Date': date,
          'X-Coefont-Content': signature
        })
        global folder_setting
        if folder_setting == True:
          background_tasks.add_task(save_wav, url= response.url)
        if response.status_code == 200:
          return {"url": response.url, "status": response.status_code}
        else:
          res.status_code = status.HTTP_502_BAD_GATEWAY
          return {"url": "", "status": response.status_code}
    res.status_code = status.HTTP_400_BAD_REQUEST
    return {"url": "", "status": status.HTTP_400_BAD_REQUEST}

def server_lunch():
  if __name__ == "__main__":
    global result
    if result != 0:
      print("別のプロセスが実行中です")
    else:
      port = 2000
      uvicorn.run(app, host='localhost', port=port)

activate = True

def gui_lunch(key, secret, path, setting):
    sg.theme('GrayGrayGray')

    column1 = [
      [sg.FolderBrowse("DL先フォルダ", font=("", 10)), sg.InputText(default_text=path,font=("", 10), key="-folderpath-")]
    ]

    column2 = [
      [sg.Button('サーバーを立ち上げる', font=("", 10), key="-btn-")]
    ]

    frame = sg.Frame('',
        [
          [
            sg.Text('❶CoeFont APIのアクセスキーを入力してください', size=(None, 2), font=("", 10))
          ],
          [
            sg.Input(default_text=key, key='-accesskey-', readonly=False, disabled=False, use_readonly_for_disable=False)
          ],
          [
            sg.Text('❷CoeFont APIのクライアントシークレットを入力してください', size=(None, 2), font=("", 10))
          ],
          [
            sg.Input(default_text=secret,key='-clientsecret-', readonly=False, disabled=False, use_readonly_for_disable=False)
          ],
          [
            sg.Checkbox("wavファイルをダウンロードする", font=("", 10), default=setting, key="-dlsetting-", change_submits=True)
          ],
          [
            sg.Column(column1, key="-activatedl-", visible=setting), sg.VPush()
          ],
          [
            sg.Column(column2)
          ]
        ] , size=(350, 300), key="-frame-"
    )

    layout = [
              [frame],
              [sg.Button('終了する',key='-exit-')]
    ]

    window = sg.Window('CoeFont to FVTT', layout)

    global activate
    activate = True

    while True:  # Event Loop
      try:
        event, value = window.read(timeout=500,timeout_key='-timeout-')

        if event in (sg.WIN_CLOSED, 'Exit'):
            value = sg.popup_ok_cancel('ソフト自体を終了させる場合はOKを、\n設定画面を再表示させる場合はキャンセルを押してください', title="終了の確認")
            if value == "OK":
              activate = False
            break
        if event == "-exit-":
            activate = False
            break
        if event == "-btn-":
            print("サーバー起動中…")
            global access_key
            global client_secret
            global folder_path
            global folder_setting
            access_key = value['-accesskey-']
            client_secret =  value['-clientsecret-']
            folder_setting = value["-dlsetting-"]
            if value["-dlsetting-"] == True:
              folder_path = value["-folderpath-"]
            window.close()
            server_lunch()
        if event == "-dlsetting-" and value["-dlsetting-"] == True:
            window["-activatedl-"].update(visible=True)
        if event == "-dlsetting-" and value["-dlsetting-"] == False:
            window["-activatedl-"].update(visible=False)
            window["-activatedl-"]
      except KeyboardInterrupt:
        break

    window.close()

def after_shutdown():
  print("Good bye")

timmer = True

def main():
  global timmer
  while timmer == True:
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      break

if result == 0:
  thread = threading.Thread(target=main, daemon=False)
  thread.start()

  while activate == True:
    try:
      key = access_key
      secret = client_secret
      path = folder_path
      fs = folder_setting
      gui_lunch(key=key, secret=secret, path=path, setting=fs)
      after_shutdown()
    except KeyboardInterrupt:
      break
else:
  print("別のプロセスが実行中です")

keyring.set_password("CoeFont", "key", access_key)
keyring.set_password("CoeFont", "secret", client_secret)
keyring.set_password("CoeFont", "folder", folder_path)
keyring.set_password("CoeFont", "foldersetting", folder_setting)

timmer = False
