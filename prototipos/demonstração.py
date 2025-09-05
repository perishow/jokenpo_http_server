'''Demonstração pra explicar a essência do que é importante para o projeto de redes:'''


import socket

# carrega o arquivo html para a memória RAM
r = open('site/homepage.html','r')
arquivo = r.read()
r.close()

# define o endereço e a porta onde o nosso servidor vai operar 
endereço = 'localhost'
porta = 8000

# formata mensagem de resposta HTTP
tamanho_arquivo = str(len(arquivo))
msg_resposta = (f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo}\r\n\r\n{arquivo}')

print(msg_resposta)

# configura o socket para funcionar com IPv4 e TCP 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((endereço,porta))
	s.listen(5)
	print(f"ouvindo em: {endereço}:{porta}")
	new_sock, addr = s.accept() 
	#print(f"endereço: {addr}") # <-- fica preso aqui esperando alguém conectar
	with new_sock:
		#data = new_sock.recv(1024)
		#data_ascii = data.decode('ascii')
		#print(data_ascii)
		#print(f"mensagem recebida:\n{data_ascii}")
		new_sock.sendall(str.encode(msg_resposta))

		

 
