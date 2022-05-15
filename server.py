import socket
import os
from fer import FER
import matplotlib.pyplot as plt
import base64
import warnings
import time
from time import sleep

###SOCKETS###

#SERVER_HOST = "192.168.1.101"  --- ip do host

port = 5001 #porta do ip
#BUFFER_SIZE = 72864 #Tamanho do buffer do socket
BUFFER_SIZE = 129536 #Tamanho do buffer do socket
s = socket.socket() #cria o soket
s.bind(('', port))   # nas '' a gente passa o ip que a gente quer, como estamos testando local deixa vazio -- coloca o soket no ip e na port q queremos
s.listen(5)

while True:
    #Aopós cada iteração, o cliente deve reconectar ao socket
    client_socket, address = s.accept() #habilita o socket para aceitar conexoes
    print(f"[+] {address} is connected.")


    #recebe os dados da imagem capturada no cliente em forma de string codificada em bytes
    received = client_socket.recv(BUFFER_SIZE)

    #trecho para decodificar os bytes da imagem recebida
    decodeit = open('gets.jpg', 'wb') 
    decodeit.write(base64.b64decode((received))) 
    decodeit.close()
    filename = 'gets.jpg'
    
####Emotion####

    #lê a imagem utilizando matplotlib
    img = plt.imread(filename)


    tempo_inicio = time.time()
    #Trecho aplica a interpretação de emoção na imagem, e retorna a emoção mais forte (emotion), a pontuação dessa emoção (score) e todas as pontuações de todas as emoções (possibilidaddes)
    detector = FER(mtcnn=True)
    #emotion, score = detector.top_emotion(img)
    possibilidades = str(detector.detect_emotions(img))
    #score = str(score)
    print("--- %s segundos ---" % (time.time() - tempo_inicio))


###SOCKETS###
    
    #retorna para o cliente as informações coletadas pelo detector de emoções
    #client_socket.send(emotion.encode())
    client_socket.send(possibilidades.encode())
    
    

# fecha a conexao com o cliente
client_socket.close()
# fecha o serverZ
s.close()

