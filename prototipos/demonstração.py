'''Demonstração pra explicar a essência do que é importante para o projeto de redes:'''

import socket

# carrega o arquivo html para a memória RAM

# define o endereço e a porta onde o nosso servidor vai operar 
endereço = '192.168.1.11'
porta = 8080

# formata mensagem de resposta HTTP

#print(msg_resposta)


# configura o socket para funcionar com IPv4 e TCP 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((endereço,porta))
	s.listen(5)
	print(f"ouvindo em: http://{endereço}:{porta}")
	while True:
		new_sock, addr = s.accept() 
		#print(f"endereço: {addr}") # <-- fica preso aqui esperando alguém conectar
		with new_sock:
			data = new_sock.recv(1024)
			data_ascii = data.decode('ascii')
			data_splited = data_ascii.split()
			print(data_ascii)
			#print(data_splited[1])
			
			if data_splited[1] == "/":
				r = open('site/home.html','r')
				arquivo = r.read()
				r.close()
				tamanho_arquivo = len(arquivo)
				msg_resposta = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo}\r\n\r\n{arquivo}'	
				new_sock.sendall(str.encode(msg_resposta))
			elif data_splited[1] == "/favicon.ico":
				"pediu favicon"
			elif data_splited[1] == "/site/form_jokenpo.html":
				r = open('site/form_namoral.html')
				arquivo = r.read()
				r.close()
				tamanho_arquivo = len(arquivo)
				msg_resposta = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo}\r\n\r\n{arquivo}'		
				new_sock.sendall(str.encode(msg_resposta))
			

		

 
