import socket

HOST = "192.168.1.13"
PORT = 8000

print("Digite uma mensagem:")
data = input()
data = data.encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as AAA:
	AAA.connect((HOST, PORT))
	AAA.sendall(data)

print(f"enviado: {data}")
