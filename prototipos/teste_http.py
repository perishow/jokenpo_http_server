import socket
import time

def bytes_para_binarios(dados):
    """Converte byte array para string binária"""
    return ''.join(format(byte, '08b') for byte in dados)

endereço = '10.0.17.184'
porta = 8000

reader = open('site/form_namoral.html','r')
arquivo = reader.read()

reader2 = open('site/formulario3.html','r')
arquivo2 = reader2.read()

tamanho_arquivo = str(len(arquivo))
tamanho_arquivo2 = str(len(arquivo2))

msg_resposta = (f'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo}\r\n\r\n{arquivo}')

msg_resposta2 = (f'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo2}\r\n\r\n{arquivo2}')

usuarios_ativos = []

#print(msg_resposta)

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((endereço,porta))
		s.listen(5)
		print(f'ouvindo em {endereço}:{porta}')
		while True:
			new_sock , addr = s.accept()
			if len(usuarios_ativos) < 10:
				ip, door = addr
				if ip not in usuarios_ativos:
					usuarios_ativos.append(ip)
				print(f"usuarios ativos: {usuarios_ativos}")
			else:
				print(f"buffer de usuários cheio: {usuarios_ativos}")
			with new_sock:
				print("recebendo dados:")
				data = new_sock.recv(1024)
				data_ascii = data.decode('ascii')
				data_split = data_ascii.split()
				if data_split[0] == 'GET': 
					#data_bits = bytes_para_binarios(data)
					#print("dados em bits:\n",data_bits)
					#print("dados decodificados:\n",data_ascii)
					new_sock.sendall(str.encode(msg_resposta))
				if data_split[0] == 'POST':
					print(f"mensagem enviada pelo form:\n{data_ascii}")
					new_sock.sendall(str.encode(msg_resposta))
except Exception as e:
	print(f"Erro: {e}")
	reader.close()
	reader2.close()
