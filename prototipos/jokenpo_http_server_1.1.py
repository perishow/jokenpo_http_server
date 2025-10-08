import socket

endereço = '192.168.1.11'
porta = 8080


# Lê os HTMLs
with open('site/home.html', 'r', encoding='utf-8') as f:
	arquivo_home = f.read()

with open('site/jogo.html', 'r', encoding='utf-8') as f:
	arquivo = f.read()

with open('site/obrigado.html', 'r', encoding='utf-8') as f:
	arquivo2 = f.read()

msg_reposta_home = (
	f'HTTP/1.1 200 OK\r\n'
	f'Connection: close\r\n'
	f'Content-Type: text/html\r\n'
	f'Content-Length: {len(arquivo_home)}\r\n\r\n'
	f'{arquivo_home}'
)

msg_resposta = (
	f'HTTP/1.1 200 OK\r\n'
	f'Connection: close\r\n'
	f'Content-Type: text/html\r\n'
	f'Content-Length: {len(arquivo)}\r\n\r\n'
	f'{arquivo}'
)

msg_resposta2 = (
	f'HTTP/1.1 200 OK\r\n'
	f'Connection: close\r\n'
	f'Content-Type: text/html\r\n'
	f'Content-Length: {len(arquivo2)}\r\n\r\n'
	f'{arquivo2}'
)

usuarios_ativos = {}
jogadas = {}


def calcular_vencedor(jogadas):
	# jogadas é um dicionário: {ip1: "pedra", ip2: "tesoura"}
	ips = list(jogadas.keys())
	jog1, jog2 = jogadas[ips[0]], jogadas[ips[1]]
	
	# regras: o que vence o que
	regras = {"pedra": "tesoura", "tesoura": "papel", "papel": "pedra"}

	# se jogador 1 ganhar do jogador 2, resultado = 1
	# se jogador 2 ganhar do jogador 1, resultado = 2
	# se empate, resultado = 0
	if jog1 == jog2:
		resultado = 2
	elif regras[jog1] == jog2:
		resultado = 0
	else:
		resultado = 1

	return resultado

def jogada_to_emoji(jogada):
	if jogada == 'pedra':
		return '🪨️'
	elif jogada == 'papel':
		return '📄️'
	elif jogada == 'tesoura':
		return '✂️'

def gerar_html_resultado(resultado, jogadas, identificador):
    identificador_oponente = None
    if identificador == 0:
        identificador_oponente = 1
    elif identificador == 1:
        identificador_oponente = 0
    
    # Estilo comum para todas as páginas de resultado
    estilo = """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
            overflow: hidden;
        }

        .background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(74, 86, 226, 0.1) 0%, transparent 50%);
            z-index: 0;
        }

        .container {
            text-align: center;
            z-index: 1;
            position: relative;
            max-width: 600px;
            width: 90%;
        }

        h1 {
            font-size: 4rem;
            font-weight: 300;
            margin-bottom: 50px;
            letter-spacing: 8px;
            background: linear-gradient(135deg, #fff 0%, #a8a8a8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .vitoria {
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .derrota {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .empate {
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .jogadas {
            display: flex;
            justify-content: center;
            gap: 60px;
            margin-top: 60px;
        }

        .jogada {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }

        .jogada-icon {
            font-size: 5rem;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
        }

        .jogada-label {
            font-size: 0.9rem;
            color: #888;
            letter-spacing: 2px;
            text-transform: uppercase;
            font-weight: 300;
        }

        .vs {
            font-size: 2rem;
            color: #444;
            align-self: center;
            font-weight: 300;
        }

        .credits {
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
        }

        .credits-title {
            font-size: 0.75rem;
            color: #444;
            margin-bottom: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .developers {
            font-size: 0.9rem;
            color: #666;
            line-height: 1.8;
            font-weight: 300;
        }

        .discipline {
            font-size: 0.8rem;
            color: #555;
            margin-top: 8px;
            font-style: italic;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container > * {
            animation: fadeIn 0.8s ease forwards;
        }

        h1 {
            animation-delay: 0.1s;
        }

        .jogadas {
            animation-delay: 0.3s;
        }
    </style>
    """
    
    # Em caso de empate
    if resultado == 2:
        html = f"""
        <html>
        <head>
            <title>Resultado - Empate</title>
            <meta charset='UTF-8'>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {estilo}
        </head>
        <body>
            <div class="background"></div>
            
            <div class="container">
                <h1 class="empate">EMPATE</h1>
                
                <div class="jogadas">
                    <div class="jogada">
                        <div class="jogada-icon">{jogada_to_emoji(list(jogadas.values())[identificador])}</div>
                        <div class="jogada-label">Você</div>
                    </div>
                    
                    <div class="vs">×</div>
                    
                    <div class="jogada">
                        <div class="jogada-icon">{jogada_to_emoji(list(jogadas.values())[identificador_oponente])}</div>
                        <div class="jogada-label">Oponente</div>
                    </div>
                </div>
            </div>

            <div class="credits">
                <div class="credits-title">Desenvolvedores</div>
                <div class="developers">
                    Giulia Buonafina<br>
                    Peri Macedo<br>
                    Bernardo Braga
                </div>
                <div class="discipline">Redes de Computadores</div>
            </div>
        </body>
        </html>
        """
        return html
    
    if identificador == resultado:
        html = f"""
        <html>
        <head>
            <title>Resultado - Vitória</title>
            <meta charset='UTF-8'>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {estilo}
        </head>
        <body>
            <div class="background"></div>
            
            <div class="container">
                <h1 class="vitoria">VITÓRIA</h1>
                
                <div class="jogadas">
                    <div class="jogada">
                        <div class="jogada-icon">{jogada_to_emoji(list(jogadas.values())[identificador])}</div>
                        <div class="jogada-label">Você</div>
                    </div>
                    
                    <div class="vs">×</div>
                    
                    <div class="jogada">
                        <div class="jogada-icon">{jogada_to_emoji(list(jogadas.values())[identificador_oponente])}</div>
                        <div class="jogada-label">Oponente</div>
                    </div>
                </div>
            </div>

            <div class="credits">
                <div class="credits-title">Desenvolvedores</div>
                <div class="developers">
                    Giulia Buonafina<br>
                    Peri Macedo<br>
                    Bernardo Braga
                </div>
                <div class="discipline">Redes de Computadores</div>
            </div>
        </body>
        </html>
        """
    elif identificador != resultado:
        html = f"""
        <html>
        <head>
            <title>Resultado - Derrota</title>
            <meta charset='UTF-8'>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {estilo}
        </head>
        <body>
            <div class="background"></div>
            
            <div class="container">
                <h1 class="derrota">DERROTA</h1>
                
                <div class="jogadas">
                    <div class="jogada">
                        <div class="jogada-icon">{jogada_to_emoji(list(jogadas.values())[identificador])}</div>
                        <div class="jogada-label">Você</div>
                    </div>
                    
                    <div class="vs">×</div>
                    
                    <div class="jogada">
                        <div class="jogada-icon">{jogada_to_emoji(list(jogadas.values())[identificador_oponente])}</div>
                        <div class="jogada-label">Oponente</div>
                    </div>
                </div>
            </div>

            <div class="credits">
                <div class="credits-title">Desenvolvedores</div>
                <div class="developers">
                    Giulia Buonafina<br>
                    Peri Macedo<br>
                    Bernardo Braga
                </div>
                <div class="discipline">Redes de Computadores</div>
            </div>
        </body>
        </html>
        """
    
    return html

def jogo():
	n_jogadas = 0
	while n_jogadas < 2:
		new_sock, addr = s.accept()
		print(f"recebendo dados de {addr}:")
		data = new_sock.recv(1024)
		data_ascii = data.decode('ascii')
		data_split = data_ascii.split()
		if data_split[0] == 'POST':
			print(f"jogada de {addr[0]} = \n{data_ascii}")
			ip, _ = addr
			jogadas[ip] = data_split[-1].split('=')[1]
			n_jogadas += 1
			usuarios_ativos[ip] = new_sock

	print(jogadas)

	# Aqui entra o calculo de quem ganhou e quem perdeu
	
	resultado = calcular_vencedor(jogadas) 
	
	html_resultado_1 = gerar_html_resultado(resultado, jogadas, 0)
	msg_http_resultado_1 = (
		f'HTTP/1.1 200 OK\r\n'
		f'Connection: close\r\n'
		f'Content-Type: text/html\r\n'
		f'Content-Length: {len(html_resultado_1)}\r\n\r\n'
		f'{html_resultado_1}'
	)
	
	html_resultado_2 = gerar_html_resultado(resultado, jogadas, 1)
	msg_http_resultado_2 = (
		f'HTTP/1.1 200 OK\r\n'
		f'Connection: close\r\n'
		f'Content-Type: text/html\r\n'
		f'Content-Length: {len(html_resultado_2)}\r\n\r\n'
		f'{html_resultado_2}'
	)
	
	
	# loop que envia o html final
	jogadas_list = list(jogadas.keys())
	for ip in jogadas_list:
		if ip == jogadas_list[0]:
			usuarios_ativos[ip].sendall(msg_http_resultado_1.encode('utf-8'))
		else:
			usuarios_ativos[ip].sendall(msg_http_resultado_2.encode('utf-8'))
	# obs : atualmente o servidor fecha quando o jogo termina

# ---------------------------
# Servidor
# ---------------------------

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((endereço, porta))
		s.listen(5)
		print(f'Ouvindo em http://{endereço}:{porta}')
	
 		# FASE DE ESPERA	
		while True:
			new_sock, addr = s.accept()
			data = new_sock.recv(1024)
			data_ascii = data.decode('ascii')		# requisição http GET ...
			data_splited = data_ascii.split()
			#print(data_ascii)
			if data_splited[0] == "GET" and data_splited[1] == '/':
				new_sock.sendall(msg_reposta_home.encode())
			elif data_splited[0] == "GET" and data_splited[1] == '/site/jogo.html':
				#print ("entrou no elif")
				#new_sock, addr = s.accept()
				ip, door = addr
				if ip not in usuarios_ativos:
					usuarios_ativos[ip] = new_sock 
					#print(f"Usuários ativos: {usuarios_ativos.keys()}")
					print(f"Tamanho usuários ativos: {len(usuarios_ativos.keys())}")
			# FIM DA FASE DE ESPERA
					if len(usuarios_ativos) == 2:
						print("começando o jogo!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
						for ip in usuarios_ativos.keys():
							usuarios_ativos[ip].sendall(msg_resposta.encode())  # envia o formulário
						jogo()	
						usuarios_ativos = {}
						jogadas = {}
# FIM DO WHILE	
	
		
		# Espera os 2 jogadores (GET)
		#while len(usuarios_ativos) < 2:
		#	new_sock, addr = s.accept()
		#	ip, door = addr
		#	if ip not in usuarios_ativos:
		#		usuarios_ativos[ip] = new_sock
		#		print(f"Usuários ativos: {usuarios_ativos.keys()}")
		#		print(f"Tamanho usuários ativos: {len(usuarios_ativos.keys())}")
		
		# INICIO DO JOGO#######################################################
		
		# Loop que envia o formulário para os jogadores
#		for ip in usuarios_ativos.keys():
#			usuarios_ativos[ip].sendall(msg_resposta.encode())  # envia o formulário


except Exception as e:
	print(f"Erro: {e}")
