import socket
import time

endereço = '192.168.1.11'
porta = 8080

reader = open('site/form_namoral.html','r')
arquivo = reader.read()
reader.close()

reader2 = open('site/obrigado.html','r')
arquivo2 = reader2.read()
reader2.close()

tamanho_arquivo = str(len(arquivo))
tamanho_arquivo2 = str(len(arquivo2))

msg_resposta = (f'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo}\r\n\r\n{arquivo}')

msg_resposta2 = (f'HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/html\r\nContent-Length: {tamanho_arquivo2}\r\n\r\n{arquivo2}')

usuarios_ativos = {} # {key: ip, value: socket 
jogadas = {} # {key: ip, value: jogada}  

#---------------------------------------------------------------------------------------------------

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((endereço,porta))
		s.listen(5)
		print(f'ouvindo em {endereço}:{porta}')
		
		# loop que espera 2 jogadores entrarem
		while len(usuarios_ativos.keys()) < 2:
			new_sock , addr = s.accept()
			ip, door = addr
			if ip not in usuarios_ativos:				
				usuarios_ativos[ip] = new_sock
				print(f"usuarios ativos: {usuarios_ativos.keys()}")
				print(f"tamanho usuarios ativos: {len(usuarios_ativos.keys())}")
		# inicio do jogo
		print("buffer cheio, iniciando jogo!")
		
		# loop que envia o formulario para os jogadores
		for ip in usuarios_ativos.keys():
			usuarios_ativos[ip].sendall(msg_resposta.encode()) # envia o formulario para os clientes
		
		# loop que recebe as jogadas
		n_jogadas = 0
		sockets = []
		while n_jogadas < 2:
			new_sock , addr = s.accept()
			print(f"recebendo dados de {addr}:")
			data = new_sock.recv(1024)
			data_ascii = data.decode('ascii')
			#print(f"mensagem recebida de {ip}:\n{data_ascii}")
			data_split = data_ascii.split()
#				if data_split[0] == 'GET': 
					#data_bits = bytes_para_binarios(data)
					#print("dados em bits:\n",data_bits)
					#print("dados decodificados:\n",data_ascii)
#					new_sock.sendall(str.encode(msg_resposta))
			if data_split[0] == 'POST':
				print(f"jogada de {ip} = \n{data_ascii}")
				ip, _ = addr
				jogadas[ip] = data_split[-1].split('=')[1] 
				n_jogadas += 1
				usuarios_ativos[ip] = new_sock
		print(jogadas)
		
		# Aqui entra o calculo de quem ganhou e quem perdeu
		# 
		# Aqui deve ser gerado o HTML mostrando se ganhou ou perdeu e quais as jogadas
		
		# loop que envia o html de obrigado meu deus vamo nessa porra 
		#
		# 
		#
		
		for ip in usuarios_ativos:
			usuarios_ativos[ip].sendall(msg_resposta2.encode())
# obs : atualmente o servidor fecha quando o jogo termina
			
except Exception as e:
	print(f"Erro: {e}")

