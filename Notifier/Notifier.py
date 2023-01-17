from collections import defaultdict
import requests
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
    
