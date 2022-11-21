import time
from pygame import mixer

# Initialize it with the correct device
mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')
mixer.music.load("script.mp3")  # Load the mp3
mixer.music.play()  # Play it

while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)
else:
    print('Voice over, exiting..')
    mixer.music.unload() # Unload the mp3 to free up system resources
    exit()