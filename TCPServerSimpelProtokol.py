from socket import *  #importere alle sockets, socket er navnet på library.
import threading
import random




def service(connectionSocket):
    while True:
        sentence = connectionSocket.recv(1024).decode().strip() #strip bruges så man kan exit
        
        # Split ved mellemrum
        parts = sentence.split(" ", 2) #Splitter sentence i 3 parts, første bid: command, anden bid: message, tredje bid: message 2
        command = parts[0].lower() #Command er den varriable vi bruge til fx 'add' eller 'random' for at få beskeden udregnet
        message = parts[1] if len(parts) > 1 else "" #message, er anden del af splittet som er beskeden man vil have gjort noget med
        message2 = parts[2] if len(parts) > 2 else "" #message2 er tredje del af splittet som man vil have gjort noget med
        #man bliver nød til at specify at hvis længden af parts er større end 1 eller 2 skal den sende beskeden tilbage, ellers skal den sende ""

        if command == "add":   #Tager to integers og plusser dem, sender en fejlbesked hvis syntax er forkert
                try:
                    a = int(message)
                    b = int(message2)
                    result = str(a + b)
                except (ValueError, TypeError):
                    result = "ERROR: brug 'add <tal1> <tal2>' f.eks. 'add 2 3'"
                connectionSocket.sendall(result.encode())
        elif command == 'subtract':   #Tager to integers og minusser dem fra hindanen og sender svaret tilbage til klienten
                try:
                    a = int(message)
                    b = int(message2)
                    result = str(a - b)
                except (ValueError, TypeError):
                    result = "ERROR: brug 'subtract <tal1> <tal2>' f.eks. 'subtract 2 3'"
                connectionSocket.sendall(result.encode())
        elif command == 'random':  #bruger den importerede random til at vælge et tilfældigt tal mellem de to givende
                try:
                    a = int(message)
                    b = int(message2)
                    rand_num = random.randint(a, b)
                    result = f"{rand_num}"
                except ValueError:
                    result = "ERROR: brug 'random <lavTal> <højTal>' fx 'random 10 50'"  # fejlbesked ved forkert syntax
                connectionSocket.sendall(result.encode()) 
        
        
        if sentence == 'exit':
            connectionSocket.close() #lukker connection ved brug af 'exit' command
            break
            
            
serverPort = 6969
serverSocket = socket(AF_INET, SOCK_STREAM) #AF_INET betyder at man vil bruge internet stacken (bruges ALTID) & SOCKET_STREAM er valg af TCP.
serverSocket.bind(('', serverPort)) # '' = kan bruge både ETH og WIFI(man tager ikke stilling til pc's netkort), serverporten binder "adressen" fast.
serverSocket.listen(1) #tallet betyder hvor mange clienter kan stå i kø til serveren.
print("The server is ready to recieve")
while True: #hvis man har lavet en serve hvor der ikke sker så meget står den her og venter for evigt
    connectionSocket, addr = serverSocket.accept() #den acceptere serveren, og returnere to ting(connectionSocket & addressen) connection socket er det som sker lige nu før man afbryder forbindelsen igen.
    threading.Thread(target=service, args=(connectionSocket,)).start()