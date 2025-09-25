from socket import *

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(('localhost', 6969))  # Valg af port

while True:
    request = input('Enter request: ')
    clientSocket.send(request.encode())  # sender tekst til serveren

    response = clientSocket.recv(1024).decode()  
    print(f'Response from server: {response}')

    if request.lower().strip() == 'exit':
        print('Exiting client.')
        break

clientSocket.close() #lukker clientsocket