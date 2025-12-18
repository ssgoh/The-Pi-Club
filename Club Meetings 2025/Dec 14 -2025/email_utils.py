import urequests
import wificonfig
import ujson
GOOGLE_SCRIPT_URL=wificonfig.GOOGLE_SCRIPT_URL
def send_email(temp, humidity):
    url = wificonfig.GOOGLE_SCRIPT_URL  # from your config.py

    payload = {
        "temperature": str(temp),
        "humidity": str(humidity)
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        #response = urequests.post(url, data=ujson.dumps(payload), headers=headers)
        response = urequests.post(GOOGLE_SCRIPT_URL, data="temperature={}&humidity={}".format(temp, humidity))

        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Error sending email:", e)
