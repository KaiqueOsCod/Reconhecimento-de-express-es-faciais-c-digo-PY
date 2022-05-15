import socket
import os
import cv2
import base64
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import time


###SOCKETS###

#Tamanho do buffer 
BUFFER_SIZE = 4048

host = "127.0.0.1" # ip de onde o server esta rodando
port = 5001 # porta do ip do servidor
s = socket.socket() #cria o socket
print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

###OPENCV###

#Habilita a câmera e abre uma nova janela com o vídeo da webcam 
cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera")
img_counter = 0

while True:
    ret, frame = cam.read()
    
    '''
    ret é uma variavel booleana que ira retornar True ou False se o frame estiver disponivel
    frame é vetor array de uma img capturada definida no fps sendo explicito ou implicito
    Frame ira pegar o proximo quadro da camera pelo cap
    
    '''
    if not ret:
        print("Erro, não foi possivel pegar o frame")
        break
    
    cv2.imshow("Camera", frame)
    k = cv2.waitKey(1)
    
    if k%256 == 27:
        # O botão ESC foi precionado
        print("Fechando camera...")
        break
    elif k%256 == 32:
        
        # O botão SPACE foi precionado
        img_name = "get.jpg" #nome da imagem com o formato
        cv2.imwrite(img_name, frame) #salvando a img


        img = mpimg.imread(img_name)
        R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]
        imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B
        plt.savefig(img_name, format='jpg')
        plt.imshow(imgGray, cmap='gray')
        plt.savefig(img_name, format='jpg')


        
        filesize = os.path.getsize(img_name)
        img_counter += 1
        print(filesize)

        tempo_inicio = time.time()
        #Converte a imagem para string, e depois para byte
        with open("get.jpg", "rb") as image2string: 
            converted_string = base64.b64encode(image2string.read())  
  
        #Envia para o servidor a imagem convertida para base64   
        s.send(converted_string)


        #Recebe do servidor o resultados das emoções e printa
        #emotion = s.recv(BUFFER_SIZE) 
        possibilidades = s.recv(BUFFER_SIZE)
        possibilidades = possibilidades.decode("utf8")
        #emotion = emotion.decode("utf8")
        #print('Emotion: ',emotion, '\n\n', 'Scores:', possibilidades, '\n\n')
        print('Scores:', possibilidades)
        print("--- %s segundos ---" % (time.time() - tempo_inicio))
        

        #OBS: após cada iteração o cliente deverá fechar a conezão e abrir uma nova
        s.close() 
        s = socket.socket()
        s.connect((host, port))
     

#Fecha a câmera e destró a janela criada anteriormente
cam.release()
cv2.destroyAllWindows()
s.close() #fecha o socketZ
os.remove("get.jpg") #limpa a pasta do cliente

