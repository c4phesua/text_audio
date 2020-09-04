import json
import requests
import ast
import wave
import sys
import pyaudio

url = 'https://viettelgroup.ai/voice/api/tts/v1/rest/syn'
VOICE_DATA_URL = 'https://vtcc.ai/voice/api/tts/v1/rest/voices'
token = '67EYFswc7lE2qrBbRePZCFYYq68sQHr7mngHhf8i8rWXH-XSXmLnfV9Ko3QDWDp1'
data = {"text": "hôm nay là thứ mấy", "voice": "doanngocle", "id": "2", "without_filter": False, "speed": 1.0, "tts_return_option": 3}
headers = {'Content-type': 'application/json', 'token': token}
response = requests.get(VOICE_DATA_URL, headers=headers)
voice_info = ast.literal_eval(response.text)
print(voice_info[0]['name'])
