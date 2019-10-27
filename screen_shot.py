import os
import pyautogui
from dotenv import load_dotenv
import requests


class Screen_shot:
    def __init__(self):
        self.count = 0
        self.path = "./image"

    def main(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        s = pyautogui.screenshot()
        s.save('{0}/screenshot{1}.png'.format(self.path, self.count))
        line_notify_api = 'https://notify-api.line.me/api/notify'
        line_notify_token = os.environ["LINE_NOTIFY_TOKEN"]
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        payload = {'message': "おはあやさ"}
        files = {"imageFile": open(
            '{0}/screenshot{1}.png'.format(self.path, self.count), "rb")}
        requests.post(line_notify_api, data=payload,
                      headers=headers, files=files)
        self.count += 1