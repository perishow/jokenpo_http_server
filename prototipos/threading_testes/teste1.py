import logging
import threading 
import time

def function(nome,tempo):
    logging.info("Thread %s: starting", nome)
    time.sleep(tempo)
    logging.info("Thread %s: finishing", nome)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

thread_dic = {}

linha1 = threading.Thread(target=function, args=("joao",3))
linha2 = threading.Thread(target=function, args=("maria",5))

thread_dic["joao"] = linha1 
thread_dic["maria"] = linha2 

for key in thread_dic:
	thread_dic[key].start()

for key in thread_dic:
	if thread_dic[key].is_alive():
		print(f"entrando em {key}")
		thread_dic[key].join()

for key in thread_dic:
	print(f"{key} = {thread_dic[key]}")
