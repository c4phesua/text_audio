from bin.text_audio_ui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtMultimedia
from os import getcwd
import requests
import ast
import json


class TextAudio(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.VOICE_INFO_URL = 'https://vtcc.ai/voice/api/tts/v1/rest/voices'
        self.TTS_URL = 'https://viettelgroup.ai/voice/api/tts/v1/rest/syn'
        self.STT_URL = 'https://vtcc.ai/voice/api/asr/v1/rest/decode_file'
        self.TOKEN = '67EYFswc7lE2qrBbRePZCFYYq68sQHr7mngHhf8i8rWXH-XSXmLnfV9Ko3QDWDp1'
        self.CERT_PATH = 'bin/wwwvtccai.crt'
        self.voice_info = None
        self.get_voice_info()
        self.play_button.clicked.connect(self.play_button_event)
        self.player = QtMultimedia.QMediaPlayer()
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.recorder = QtMultimedia.QAudioRecorder()
        self.recorder.audioSettings().setCodec('audio/pcm')
        self.recorder.audioSettings().setSampleRate(11025)
        self.recorder.audioSettings().setChannelCount(1)
        self.recorder.setContainerFormat('wav')
        record_file = QtCore.QUrl.fromLocalFile(getcwd() + '/temp/record.wav')
        self.recorder.setOutputLocation(record_file)
        self.record_button.clicked.connect(self.record_event)

    def get_voice_info(self):
        response = requests.get(self.VOICE_INFO_URL)
        self.voice_info = ast.literal_eval(response.text)
        for line in self.voice_info:
            self.voice_option.addItem(line['description'] + '-' + line['name'])

    @QtCore.pyqtSlot()
    def play_button_event(self):
        self.play_button.setEnabled(False)
        self.player.stop()
        self.playlist.clear()
        voice = self.voice_info[self.voice_option.currentIndex()]['code']
        speed = 0.7 + 0.6 * self.speed_slider.value() / 99
        data = {"text": self.plainTextEdit.toPlainText(), "voice": voice, "id": "2",
                "without_filter": False,
                "speed": speed,
                "tts_return_option": 3}
        headers = {'Content-type': 'application/json', 'token': self.TOKEN}
        response = requests.post(self.TTS_URL, data=json.dumps(data), headers=headers)
        print(response.headers)
        print(response.status_code)
        with open('temp/raw.mp3', 'wb') as f:
            f.write(response.content)
        file = QtCore.QUrl.fromLocalFile('temp/raw.mp3')
        content = QtMultimedia.QMediaContent(file)
        self.playlist.addMedia(content)
        self.player.setVolume(self.volum_slider.value())
        self.player.play()
        self.play_button.setEnabled(True)

    @QtCore.pyqtSlot()
    def record_event(self):
        if self.recorder.state() == QtMultimedia.QMediaRecorder.StoppedState:
            self.recorder.record()
            self.record_button.setText('Dừng')
        else:
            self.recorder.stop()
            self.record_button.setText('Thu âm')
            self.record_button.setEnabled(False)
            self.convert_audio()
            self.record_button.setEnabled(True)

    def convert_audio(self):
        headers = {'token': self.TOKEN}
        s = requests.Session()
        files = {'file': open('temp/record.wav', 'rb')}
        response = requests.post(self.STT_URL,
                                 files=files,
                                 headers=headers,
                                 verify=self.CERT_PATH)
        print(response.status_code)
        data = ast.literal_eval(response.text.replace('true', 'True').replace('false', 'False'))
        print(data)
        text = ''
        for d in data:
            text += d['result']['hypotheses'][0]['transcript'] + '\n'
        self.plainTextEdit.setPlainText(text)
