import socket
import time
#import sys

#alvo = sys.argv[1]

buff21 = ''

# ENVIA PASV e PEGA PORTA
def passive():
	msg = b'PASV\r\n'
	s21.sendall(msg)
	print("PASV SENT\n")
	buf21 = s21.recv(1024)
	print('BUF21',buf21.decode())
	#
	buf21 = buf21.split()
	#print(buf21)
	# ['227', 'Entering', 'Passive', 'Mode', '(143,106,148,79,102,8).']
	buf21 = buf21[4]
	#print('buff: ', buf21)
	# b'(143,106,148,79,102,8).'
	buf21 = str(buf21)
	buf21 = buf21.split(',')
	print(buf21)
	# ['(143', '106', '148', '79', '102', '8).']
	p1 = buf21[4]
	print(p1)
	#'102'
	#print(buf21[5])
	#'8).'
	p2 = buf21[5].split(')')
	#['8',').']
	#print('\n', 'p2', p2)
	p2 = p2[0]
	port = 256 * int(p1) + int(p2)
	
	#s20.connect((alvo, port))
	
	return port

# CRIA SOQUETE 21
s21 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s21.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)

# CRIA SOQUETE 20
s20 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s20.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ESCOLHE SERVER
#alvo = socket.gethostbyname("ftp.dca.fee.unicamp.br")
#alvo = socket.gethostbyname("ftp.unicamp.br")
#alvo = socket.gethostbyname("ftp.ed.ac.uk")
alvo = socket.gethostbyname("ftp.inf.puc-rio.br")
#alvo = socket.gethostbyname(sys.argv[1])

# CONECTA AO SERVER
s21.connect((alvo, 21))
buf21 = s21.recv(4028)
print(buf21.decode())

if b'220' in buf21:
	msg = b'USER anonymous\r\n'
	s21.sendall(msg)
	buf21 = s21.recv(1024)
	print(buf21.decode())

if b'331' in buf21:
	msg = b'PASS edison@ecomp.poli.br\r\n'
	s21.sendall(msg)
	print('Pass sent')
	buf21 = s21.recv(1024)
	print(buf21.decode())
#
if b'230' in buf21:
	port = passive()
	s20.connect((alvo, port))
	print(port)

	msg = b'LIST\r\n'
	s21.sendall(msg)
	print("LIST SENT ")
	buf21 = s21.recv(1024)
	print(buf21.decode())
	buf21 = s21.recv(1024)
	print(buf21.decode())
	
	buf20 = s20.recv(1024)
	buf20 = buf20.decode()
	print("DATA:\n",buf20)
	s20.close()

# # CRIA SOQUETE 20
# s20 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #s20.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while 1:
	# CRIA SOQUETE 20
	s20 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s20.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	verbo = input('digite comando: \n')
	if verbo != 'QUIT':
		if ('CWD' in verbo) or ('PWD' in verbo): #CWD nome_diretorio
			msg = verbo + '\r\n'
			msg = msg.encode()
			print(msg)
			s21.sendall(msg)
			buf21 = s21.recv(1024)
			print(buf21.decode())
		elif ('LIST' in verbo) or ('RETR' in verbo): #RETR nome_arquivo
			port = passive()
			print(port)
			s20.connect((alvo, port))
			msg = verbo + '\r\n'
			msg = msg.encode()
			
			s21.sendall(msg)
			buf21 = s21.recv(1024)
			print(buf21.decode())
			buf21 = s21.recv(1024)
			print(buf21.decode())
			
			buf20 = s20.recv(1024)
			buf20 = buf20.decode()
			print("DATA:\n",buf20)
			s20.close()
	else:
		msg = verbo + '\r\n'
		msg = msg.encode()
		s21.sendall(msg)
		buf21 = s21.recv(1024)
		#print("verbo ")
		print(buf21.decode())
		break

s20.close()
s21.close()
