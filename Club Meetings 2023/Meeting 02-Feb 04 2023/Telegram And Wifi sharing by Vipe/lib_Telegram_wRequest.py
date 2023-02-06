import urequests as requests
from time import sleep

def Telegram_wRequest(msg):
    telegram_bot_token= ""
    telegram_chat_id =""
    TelegramMSG = "https://api.telegram.org/bot" + telegram_bot_token + "/sendMessage?chat_id=" + telegram_chat_id + "&text=" + msg
   
    try:
        requests.post(TelegramMSG).json()
    except:
        
        try:
            requests.post(TelegramMSG)
        
        except:
            print('Sent Message Failed')
            sleep(5)
            pass
    
    return TelegramMSG

