import socket

HOST = "0.0.0.0"
PORT = 6666
data = b"teste rsrs"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as AAA:
	AAA.connect((HOST, PORT))
	AAA.sendall(data)

print(f"enviado: {data}")
