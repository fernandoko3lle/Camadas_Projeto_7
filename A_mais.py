
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.signal import butter, lfilter, freqz




#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:

    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas.
    #Muitas vezes a gravação retorna uma lista de listas. Você poderá ter que tratar o sinal gravado para ter apenas uma lista.

    duration =  2  #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic  

    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisições) durante a gravação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    #faca um print na tela dizendo que a captação comecará em n segundos. e então 
    #use um time.sleep para a espera.
   
    freqDeAmostragem = sd.default.samplerate
    numAmostras = int(duration * freqDeAmostragem)

    # Parâmetros do filtro
    order = 6
    fs = freqDeAmostragem       # taxa de amostragem, Hz
    cutoff = 500    # frequência de corte desejada do filtro, Hz

    # Função para o design do filtro passa-baixa Butterworth
    def butter_lowpass(cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    # Função para aplicar o filtro
    def butter_lowpass_filter(data, cutoff, fs, order=5):
        b, a = butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

    print("Gravação iniciada...")
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")

    print(f'audio: {audio}')

    # Aplicação do filtro
    audio_ = audio.flatten()
    filtered_data = butter_lowpass_filter(audio_, cutoff, fs, order)

    # Plota o sinal de áudio original
    xf, yf = signal.calcFFT(audio_, freqDeAmostragem)
    plt.figure()
    plt.plot(xf, yf)
    plt.legend('Antes')
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio')
   

    # Plota o sinal de áudio filtrado
    xf, yf = signal.calcFFT(filtered_data, freqDeAmostragem)
    plt.figure()
    plt.plot(xf, yf)
    plt.legend('Depois')
    plt.xlabel('Frequência (Hz)') 
    plt.ylabel('Amplitude')
    plt.title('Fourier do sinal de áudio')
    plt.show()

if __name__ == "__main__":
    main()
