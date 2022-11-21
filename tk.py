

import tkinter as tk

import requests
import base64
import io

from pynput.keyboard import Key, Listener

from pydub import AudioSegment
from pygame import mixer
from tkinter import ttk
from time import sleep

voices = [
    "en_us_001",
    "en_us_006",
    "en_us_007",
    "en_us_009",
    "en_us_010",
    "en_uk_001",
    "en_uk_003",
    "en_au_001",
    "en_au_002",
    "fr_001",
    "fr_002",
    "de_001",
    "de_002",
    "es_002",
    "es_mx_002",
    "br_001",
    "br_003",
    "br_004",
    "br_005",
    "id_001",
    "jp_001",
    "jp_003",
    "jp_005",
    "jp_006",
    "kr_002",
    "kr_004",
    "kr_003",
    "en_us_ghostface",
    "en_us_rocket",
    "en_us_stitch",
    "en_us_stormtrooper",
    "en_us_chewbacca",
    "en_us_c3po",
    "en_male_sing_funny_it_goes_up",
    "en_female_ht_f08_wonderful_world",
    "en_female_f08_warmy_breeze",
    "en_male_m03_sunshine_soon",
    "en_male_m2_xhxs_m03_silly",
    "en_female_ht_f08_glorious",
    "en_female_f08_salut_damour",
    "en_male_m03_lobby"
]


class Requester:
    def __init__(self):
        self.base = 'https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/'
        self.params = {
            'text_speaker': '',
            'req_text': '',
            'aid': 1233
        }
        self.headers = {
            'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
            'Cookie': 'sessionid=d332e2af648594a822cb31bc28d18f0b'
        }
        self.request = requests.Session()
        self.tmp = []

    def create_voice_bytes(self, narrator, message):
        self.params['text_speaker'] = narrator
        self.params['req_text'] = message
        print(self.params)
        d = self.request.post(
            self.base, params=self.params, headers=self.headers)
        d = d.json()['data']['v_str']
        return io.BytesIO(base64.b64decode(d))


class VoiceGenerator:
    def __init__(self, narrator):
        self.request = Requester()

        self.narrator = narrator

    def create_voice_script(self, script):
        with open(script, 'rb') as f:
            data = f.read().decode()
            data = data.split('.')
            return data


class TTSgenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.width = 200
        self.height = 600

        self.title('TTS Generator')
        self.geometry(f'{self.height}x{self.width}')
        self.resizable(False, False)
        self.attributes('-alpha', 0.9)
        self.iconbitmap('./assets/icon.ico')

        self.tts = tk.StringVar()

        self.selected_voice = None
        self.voice = None

        self.__init()

    def play_voice(self):
        v = VoiceGenerator(self.selected_voice)

        self.voice = v.request.create_voice_bytes(
            v.narrator, self.tts.get()
        )

        self.play_mic()

    def play_mic(self):
        mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
        mixer.music.load(self.voice)  # Load the mp3
        mixer.music.play()  # Play it

        while mixer.music.get_busy():  # wait for music to finish playing
            sleep(1)
        else:
            print('Voice over, exiting..')
            mixer.music.unload()  # Unload the mp3 to free up system resources

    def __init(self):
        enter_text = ttk.Frame(self)
        enter_text.pack(padx=10, pady=0, fill='x', expand=True)

        tts_label = ttk.Label(enter_text, text="Enter text:")
        tts_label.pack(fill='x', expand=True)

        tts_entry = ttk.Entry(enter_text, textvariable=self.tts)
        tts_entry.pack(fill='x', expand=True)
        tts_entry.focus()

        self.save_btn = ttk.Button(
            enter_text, text="Play", command=self.play_voice)
        self.save_btn.pack(fill='x', expand=True, pady=0)

        if self.selected_voice == None:
            self.save_btn.state(['disabled'])

        var = tk.Variable(value=voices)

        listbox = tk.Listbox(
            self,
            listvariable=var,
            height=6,
            selectmode=tk.EXTENDED
        )

        listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)


        def items_selected(event):
            # get all selected indices
            selected_indices = listbox.curselection()
            # get selected items
            self.selected_voice = ",".join([listbox.get(i) for i in selected_indices])

            if self.selected_voice != None:
                self.save_btn.state(['!disabled'])

        listbox.bind('<<ListboxSelect>>', items_selected)

        # self.mixer_btn = ttk.Button(
        #     enter_text, text="Play to mic", command=self.play_mic)
        # self.mixer_btn.pack(fill='x', expand=True, pady=0)

        # if self.voice == None:
        #     self.mixer_btn.state(['disabled'])


if __name__ == '__main__':
    app = TTSgenerator()

    app.mainloop()
