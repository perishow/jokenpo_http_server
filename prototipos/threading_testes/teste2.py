# Esse teste consiste em criar um servidor http simples que vai coletar o endereço de ip de quem se conectou com ele e salvar o que ele receber em uma lista, mas 2 usuários podem estar se comunicando com o servidor simultâneamente.

import socket
import threading

endereço = '192.168.1.13'
porta = 8000

usuarios_ativos = {} # [addr] = thread
mensagens = {} # [addr] = msg

def collect_data(ip, socket):
	print(f"recebendo de {ip}...")
	data = socket.recv(1024)
	data = data.decode('ascii')
	mensagens[ip] = data
	print(f"recebeu de {ip}!")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((endereço,porta))
	s.listen(5)
	print(f"ouvindo em {endereço}:{porta}")
	while len(usuarios_ativos) < 2:
		new_sock, addr = s.accept()
		ip, _ = addr
		usuarios_ativos[ip] = new_sock
		new_thread = threading.Thread(target=collect_data, args=(ip,new_sock))
		usuarios_ativos[ip] = new_thread
	
	for ip in usuarios_ativos:
		usuarios_ativos[ip].start()
		
	for ip in usuarios_ativos:
		if usuarios_ativos[ip].is_alive():
			usuarios_ativos[ip].join()
			
	print(mensagens)
