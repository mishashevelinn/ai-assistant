import datetime
import queue
import time
from threading import Thread
import numpy as np
import scipy as sp
import pasimple
import matplotlib.pyplot as plt


# Audio attributes for the recording

# Record 10 seconds of audio

class Pulse2PyPipe():
    def __init__(self):
        self.FORMAT = pasimple.PA_SAMPLE_S16LE
        self.SAMPLE_WIDTH = pasimple.format2width(self.FORMAT)
        self.CHANNELS = 2
        self.SAMPLE_RATE = 41000
        self.pipe = queue.Queue()

    def get_pa(self):
        return pasimple.PaSimple(pasimple.PA_STREAM_RECORD, self.FORMAT, self.CHANNELS, self.SAMPLE_RATE,
                                 device_name='recording.monitor')

    def listen_callback(self, device_name, chunk_dur):
        with pasimple.PaSimple(pasimple.PA_STREAM_RECORD, self.FORMAT, self.CHANNELS, self.SAMPLE_RATE,
                               device_name=device_name) as pa:
            t0 = datetime.datetime.now()
            while True:
                audio = pa.read(self.CHANNELS * self.SAMPLE_RATE * self.SAMPLE_WIDTH * chunk_dur)
                self.pipe.put(audio)
                if datetime.datetime.now() - t0 > datetime.timedelta(seconds=10):
                    break

    def listen_threaded(self, device_name='recording.monitor', chunk_dur=2):
        produce_sound_data = Thread(target=self.listen_callback, args=(device_name, chunk_dur))
        produce_sound_data.start()


def main():
    pipe = Pulse2PyPipe()

    pipe.listen_callback(device_name='recording.monitor', chunk_dur=1)
    data = list(pipe.pipe.queue)


if __name__ == '__main__':
    main()
