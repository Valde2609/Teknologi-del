from socket import *
import random
import threading
import json

# Service metode
def service(connectionSocket):
    while True:
        sentence = connectionSocket.recv(1024).decode().strip()

        #Lukker forbindelsen med 'exit' command
        if sentence.lower() == 'exit':
            connectionSocket.sendall("Du har afbrudt forbindelsen".encode())
            connectionSocket.close()
            break

        try:
            # direkte parse JSON fra modtaget tekst
            request = json.loads(sentence)
        except json.JSONDecodeError:
            error_response = {
                "status": "error",
                "message": "Ugyldig JSON. Brug fx: {\"command\": \"add\", \"int1\": 5, \"int2\": 3}"
            }
            connectionSocket.sendall(json.dumps(error_response).encode())
            continue

        # Læser JSON felter fra client request
        command = request.get("command", "").lower()
        int1 = request.get("int1")
        int2 = request.get("int2")

        response = {}

        # gyldig syntax: {"command": "add", "int1": 5, "int2": 3}
        if command == "add":
            if isinstance(int1, (int)) and isinstance(int2, (int)):
                response["result"] = int1 + int2
            else:
                response = {"status": "error", "message": "add kræver int1 og int2 som heltal"}
        
        #gyldig syntax: {"command": "subtract", "int1": 5, "int2": 3}        
        elif command == 'subtract':
            if isinstance(int1, (int)) and isinstance(int2, (int)):
                response["result"] = int1 - int2
            else:
                response = {"status": "error", "message": "subtract kræver int1 og int2 som heltal"}

        #gyldig syntax: {"command": "random", "int1": 5, "int2": 3}
        elif command == "random":
            if isinstance(int1, int) and isinstance(int2, int):
                low, high = sorted([int1, int2])
                response["result"] = random.randint(low, high)
            else:
                response = {"status": "error", "message": "random kræver int1 og int2 som heltal"}
        #Fejlbesked hvis man sender ugyldig JSON string
        else:
            response = {
                "status": "error",
                "message": "Ukendt kommando. Gyldige kommandoer: 'add', 'random', 'exit'."
            }

        # Send altid JSON tilbage til klienten
        connectionSocket.sendall(json.dumps(response).encode())


# SERVER INFORMATION MED UNDERSTØTTELSE AF CONCURRENT (CONCURRENT SERVER)
serverport = 6543
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Forbindelse fra: {addr}")
    threading.Thread(target=service, args=(connectionSocket,)).start()
