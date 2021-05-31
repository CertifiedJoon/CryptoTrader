import requests

def post_message(text):
    """슬랙 메시지 전송"""
    with open("credentials/slack.txt") as f:
        lines = f.readlines()
        token = lines[0].strip()
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": '#personalproject',"text": text}
    )
    
