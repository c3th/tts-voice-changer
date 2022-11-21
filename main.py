

import requests
import base64
import io

from pydub import AudioSegment
from pygame import mixer
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


    def mimic_voice(self):
        # Initialize it with the correct device
        mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
        mixer.music.load("script.mp3")  # Load the mp3
        mixer.music.play()  # Play it

        while mixer.music.get_busy():  # wait for music to finish playing
            sleep(1)
        else:
            print('Voice over, exiting...')
            mixer.music.unload() # Unload the mp3 to free up system resources
            exit()


if __name__ == '__main__':
    v = VoiceGenerator(
        'en_us_rocket'
    )

    script = v.create_voice_script(
        'script.txt'
    )

    voice_segments = []

    for text in script:
        text = text.strip()
        if text:
            voice = v.request.create_voice_bytes(v.narrator, text)

            voice_segment = AudioSegment.from_raw(
                voice, sample_width=2, frame_rate=44100, channels=2)
            voice_segments.append(voice_segment)

    tmp_voice = None

    for segment in voice_segments:
        if tmp_voice == None:
            print('Starting to concatenate...')
            tmp_voice = segment

        else: tmp_voice += segment
        print(tmp_voice)

    tmp_voice.export('script.mp3', format='mp3')
    print('Script complete')



    # narrator = 'en_us_ghostface'
    # message = 'world'

    # voice = r.createVoiceFromFile(narrator, 'script.txt')
    # voice_1 = r.createVoice('en_us_ghostface', 'i would never do that')[
    #     'data']['v_str']
    # voice_2 = r.createVoice('en_us_ghostface', 'because it would hurt me')[
    #     'data']['v_str']

    # def combine_audio(audios):
    #     combined = None

    #     for i in audios:
    #         audio = AudioSegment.from_raw(io.BytesIO(
    #             i), sample_width=2, frame_rate=44100, channels=2)
    #         combined += audio

    #     return combined

    # filename = f'./{narrator}-{message}.mp3'

    # audio_bytes = [
    #     base64.b64decode(voice_1),
    #     base64.b64decode(voice_2)]

    # voice_segment_1 = AudioSegment.from_raw(io.BytesIO(
    #     base64.b64decode(voice_1)), sample_width=2, frame_rate=44100, channels=2)
    # voice_segment_2 = AudioSegment.from_raw(io.BytesIO(
    #     base64.b64decode(voice_2)), sample_width=2, frame_rate=44100, channels=2)

    # combined = voice_segment_1 + voice_segment_2

    # print(combined)

    # combined.export(filename, format='mp3')

    # r.concatenateAudioFiles(combined, filename)

    # r.writeToFile(filename, v_str)
