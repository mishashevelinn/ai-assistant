import datetime
import io
import queue
import time
from threading import Thread
import numpy as np
import scipy as sp
import pasimple
import matplotlib.pyplot as plt
import scipy.io.wavfile


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
                audio_stream_chunk = io.BytesIO(audio)
                self.pipe.put(audio_stream_chunk)
                if datetime.datetime.now() - t0 > datetime.timedelta(seconds=10):
                    break

    def listen_threaded(self, device_name='recording.monitor', chunk_dur=2):
        produce_sound_data = Thread(target=self.listen_callback, args=(device_name, chunk_dur))
        produce_sound_data.start()
        produce_sound_data.join()

    def raw2wav(self, raw, name):
        sig = np.frombuffer(raw, dtype='i4')
        scipy.io.wavfile.write(name, self.SAMPLE_RATE, sig)

    def concat_raw2wav(self, raw_list, name):
        sig = None
        for chunk in raw_list:
            sig_chunk = np.frombuffer(chunk, dtype='i4')
            if sig is None:
                sig = sig_chunk
            else:
                sig = np.concatenate((sig, sig_chunk))
        scipy.io.wavfile.write(name, self.SAMPLE_RATE, sig)

def main():
    pipe = Pulse2PyPipe()

    pipe.listen_threaded(device_name='recording.monitor', chunk_dur=1)
    data = list(pipe.pipe.queue)
    print(f'Recorded {len(data)} chunks')
    # for i, chunk in enumerate(data):
    #     pipe.raw2wav(chunk, f"sample_{i}.wav")
    pipe.concat_raw2wav(data, 'full.wav')

if __name__ == '__main__':
    main()
