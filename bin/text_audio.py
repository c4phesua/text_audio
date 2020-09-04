from bin.text_audio_ui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtMultimedia
import requests
import ast
import json


class TextAudio(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.VOICE_INFO_URL = 'https://vtcc.ai/voice/api/tts/v1/rest/voices'
        self.TTS_URL = 'https://viettelgroup.ai/voice/api/tts/v1/rest/syn'
        self.TOKEN = '67EYFswc7lE2qrBbRePZCFYYq68sQHr7mngHhf8i8rWXH-XSXmLnfV9Ko3QDWDp1'
        self.voice_info = None
        self.get_voice_info()
        self.play_button.clicked.connect(self.play_button_event)
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.recorder = QtMultimedia.QAudioRecorder()
        self.recorder.audioSettings().setQuality(QtMultimedia.QMultimedia.HighQuality)
        self.recorder.setOutputLocation(QtCore.QUrl.fromLocalFile('record.mp3'))

    def get_voice_info(self):
        response = requests.get(self.VOICE_INFO_URL)
        self.voice_info = ast.literal_eval(response.text)
        for line in self.voice_info:
            self.voice_option.addItem(line['description'] + '-' + line['name'])

    @QtCore.pyqtSlot()
    def play_button_event(self):
        self.player.stop()
        voice = self.voice_info[self.voice_option.currentIndex()]['code']
        speed = 0.7 + 0.6 * self.speed_slider.value() / 99
        data = {"text": self.plainTextEdit.toPlainText(), "voice": voice, "id": "2",
                "without_filter": False,
                "speed": speed,
                "tts_return_option": 3}
        headers = {'Content-type': 'application/json', 'token': self.TOKEN}
        response = requests.post(self.TTS_URL, data=json.dumps(data), headers=headers)
        with open('raw.mp3', 'wb') as f:
            f.write(response.content)
        file = QtCore.QUrl.fromLocalFile('raw.mp3')
        content = QtMultimedia.QMediaContent(file)
        self.playlist.clear()
        self.playlist.addMedia(content)
        self.player.setVolume(self.volum_slider.value())
        self.player.play()
