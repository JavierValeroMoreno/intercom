import pyaudio
import pywt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

if __name__ == '__main__':

    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )
    print("**RECORDING 5 SECONDS**")
    frames =[]

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("**DONE RECORDING**")

    frames_int =[]
    for _byte in frames:
        frames_int.append(int.from_bytes(frames[1], byteorder = 'big'))
    
    (cA, cD) = pywt.dwt(frames_int, 'db1')

    print(cA)
    print(cD)

    undwt = pywt.idwt(cA, cD, 'db1')
    