import requests

def post_message(text):
    """슬랙 메시지 전송"""
    
    token = "xoxb-2090282742643-2090295046947-Vl7EZ13JeEKoEAVQQPNGTFzs"
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": '#personalproject',"text": text}
    )
    
