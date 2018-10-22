import pyaudio
import pywt
import numpy as np
import math
import scipy.stats as st

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

#Funcion para calcular la entropia de un array
def entropy (arr):    
    hist = np.histogram(arr, range=(arr.min(),arr.max()))
    return st.entropy(hist[0])

if __name__ == '__main__':

    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )
    print("**RECORDING**")

    while True:
        #Leemos el chunk de audio
        data = stream.read(CHUNK)
        data2=np.frombuffer(data, dtype=np.int16)
        print("Datos Originales")
        print("Entropia: ",entropy(data2), "\nMinimo: ", data2.min(), "\nMaximo: ", data2.max())
       
        #Realizamos la transformada
        (cA, cD) = pywt.dwt(data2, 'db1')
        print("Datos Transformada")
        print("Primeros valores de cA: ",cA[0], cA[1], cA[2], cA[3], cA[4] )
        print("Primeros valores de cD: ",cD[0], cD[1], cD[2], cD[3], cD[4] )
        print("Entropia: ",entropy(cA), "\nMinimo: ", cA.min(), "\nMaximo: ", cA.max())
        
        #Realizamos la transformada inversa
        decode = pywt.idwt(cA,cD, 'db1')

        decode2 = np.array(decode)
        decode2 = decode2.astype(np.int16)
        print("Datos Transformada Inversa")
        print("Entropia: ",entropy(decode2), "\nMinimo: ", decode2.min(), "\nMaximo: ", decode2.max())
        
        decode2.tobytes()

        try:
            stream.write(decode2,CHUNK)
        except Exception as e:
            decode2 = '\00' * CHUNK

    
  