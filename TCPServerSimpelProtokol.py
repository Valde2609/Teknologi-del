from socket import *  #importere alle sockets, socket er navnet på library.
import threading




def service(connectionSocket):
    while True:
        sentence = connectionSocket.recv(1024).decode().strip() #strip bruges så man kan exit
        
        # Split ved første mellemrum
        parts = sentence.split(" ", 1) #Splitter sentence i 2 parts, første bid: command, anden bid: message
        command = parts[0].lower() #Command er den varriable vi bruge til fx 'upper' for at få beskeden til at blive sendt i uppercase
        message = parts[1] if len(parts) > 1 else "" #message, er anden del af splittet som er beskeden man vil have gjort noget med
        #man bliver nød til at specify at hvis længden af parts er større end 1 skal den sende beskeden tilbage, ellers skal den sende ""

        if command == 'upper':
            capitalizedSentence = message.upper() #ny variabel som konvertere message til uppercase
            connectionSocket.send(capitalizedSentence.encode()) #sende den nye uppercase message tilbage til client
        elif command == 'double':
            doubleSentence = message = message + message # ny variabel som konvertere beskeden til dobbelt besked
            connectionSocket.send(doubleSentence.encode()) # sender den nye dobbelt besked tilbage til client
        else:
            connectionSocket.send(sentence.encode()) #in case man ikke bruger en command, sender den bare base beskeden tilbage
        
        if sentence == 'exit':
            connectionSocket.close() #lukker connection
            break
            
            
serverPort = 6969
serverSocket = socket(AF_INET, SOCK_STREAM) #AF_INET betyder at man vil bruge internet stacken (bruges ALTID) & SOCKET_STREAM er valg af TCP.
serverSocket.bind(('', serverPort)) # '' = kan bruge både ETH og WIFI(man tager ikke stilling til pc's netkort), serverporten binder "adressen" fast.
serverSocket.listen(1) #tallet betyder hvor mange clienter kan stå i kø til serveren.
print("The server is ready to recieve")
while True: #hvis man har lavet en serve hvor der ikke sker så meget står den her og venter for evigt
    connectionSocket, addr = serverSocket.accept() #den acceptere serveren, og returnere to ting(connectionSocket & addressen) connection socket er det som sker lige nu før man afbryder forbindelsen igen.
    threading.Thread(target=service, args=(connectionSocket,)).start()
    # service(connectionSocket)