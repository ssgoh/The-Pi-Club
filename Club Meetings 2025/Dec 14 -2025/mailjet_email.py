import urequests
import json



def send_email(MAILJET_API_KEY,MAILJET_SECRET_KEY,FROM_EMAIL,TO_EMAIL,SENDER_NAME,msg):
    url = "https://api.mailjet.com/v3.1/send"
    
    payload = {
        "Messages": [
            {
                "From": {
                    "Email": FROM_EMAIL,
                    "Name": SENDER_NAME
                },
                "To": [
                    {
                        "Email": TO_EMAIL,
                        "Name": "Recipient"
                    }
                ],
                "Subject": "Pico Temperature & Humidity Update",
                "TextPart": msg
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    json_data = json.dumps(payload)

    print("===== JSON SENT TO MAILJET =====")
    print(json_data)
    print("===== END JSON =====")

    response = urequests.post(
        url,
        data=json_data,
        headers=headers,
        auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY)
    )

    print("Mailjet response:", response.text)
    response.close()