from collections import defaultdict
import requests

# Notifier Purpose:
#   When the algorithm makes a transaction, we must notify us by some way.
#   Feel free to add/remove feature.
#   Right now i am using slack to send notification to my phone.
#   Replace NotImplementedError to add your own code.

class Notifier:
    def __init__(self):
        self._contacts = defaultdict(list)
    
    def add_contacts(self, contact_type, contact):
        self._contacts[contact_type].append(contact)
    
    def send_email(self):
        raise NotImplementedError("Oops not implemented yet")
    
    def notify_all(self):
        raise NotImplementedError("Oops not implemented yet")
    
    def post_message(text):
        """슬랙 메시지 전송"""
        with open("credentials/slack.txt") as f:
            lines = f.readlines()
            token = lines[0].strip()
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": '#personalproject',"text": text}
        )
    
