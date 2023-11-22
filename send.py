import requests
import json

PHONE_ID = "180216545167840"
TOKEN = "EAAMw36anjcEBOzJ9uU17fNo6thmU3N7PrWMSYPLHL4AE0BpWVl9QJklIWwZAd4Cs8q2R48mnZCjfKdltvcZAAVJ4n0kdf8LX9VkAoSCwi8ZAq30UZAXseeyj7ceKojcVkstUZCrOuvJNz9stbRY1M6qiV2d0UZCpknaQgOOZCu7uZAgVU5WPpH9fZCsOGhbMOZCvqLB87bMDrmnN6BSZCWNTZAzEZD"
NUMBER = "+6287831302651"
MESSAGE = "Halodsfsus9f"

URL = "https://graph.facebook.com/v13.0/"+PHONE_ID+"/messages"
headers = {
    "Authorization": "Bearer "+TOKEN, 
    "Content-Type": "application/json"
}
data = { 
    "messaging_product": "whatsapp", 
    "to": NUMBER, 
    "type": "text", 
    "text": json.dumps({ "preview_url": False, "body": MESSAGE}) 
}
response = requests.post(URL, headers=headers, data=data)
response_json = response.json()
print(response_json)