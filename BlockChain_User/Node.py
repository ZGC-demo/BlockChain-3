#thread socket programming
import threading
import socket
import os

os.system("chcp 949")
os.system("cls")
node_ip = input("\n본인 ip: ")
while True:
	if node_ip == "" or len(node_ip)>20:
		node_ip = input("\n본인 ip: ")
	else:
		break
#node_ip = "192.168.0.6"
os.system("cls")

def node():
	representative = "전찬빈#11197"
	while True:
		node_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		node_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		node_socket.bind(('', 12347))
		data = node_socket.recvfrom(12347)[0]
		try:
			block_protocol = str(data[0:13].decode())
		except:
			continue
		else:
			if not data:
				continue

			elif block_protocol == "id_block_name":
				sign = node_socket.recvfrom(12347)[0]
				with open("node_id_sign", "wb") as node_id_sign:
					node_id_sign.write(sign)
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey server_public_key.pem -in node_id_sign -out node_id_verify -pubin")	
				with open("node_id_verify", "r") as node_id_verify:
					node_id_verify = node_id_verify.read()
				os.system("del node_id_sign")
				os.system("del node_id_verify")
				if node_id_verify[:-2] == "신원 등록":
					title = node_socket.recvfrom(12347)[0].decode()
					id_block = open("id\\" + title,"wb")
					while True:
						id_block_data = node_socket.recvfrom(12347)[0]
						if id_block_data == "end of file".encode():
							break
						id_block.write(id_block_data)
					id_block.close()
					print(title + "이 전송되었습니다.")
				else:
					continue

			elif block_protocol == "vote_res_time":
				with open("node_tmp","wb") as tmp:
					tmp.write(data[13:])
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey server_public_key.pem -in node_tmp -out node_tmp2 -pubin")	
				with open("node_tmp2", "rb") as tmp2:
					net_data = tmp2.read().decode('cp949')[:-3]
				os.system("del node_tmp")
				os.system("del node_tmp2")
				print("지금부터 대표자 선출이 시작됩니다! (" + net_data + "까지)")

			elif block_protocol == "vote_res_rsut":
				with open("node_tmp","wb") as tmp:
					tmp.write(data[13:])
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey server_public_key.pem -in node_tmp -out node_tmp2 -pubin")	
				with open("node_tmp2", "rb") as tmp2:
					net_data = tmp2.read().decode('cp949')[:-3]
				os.system("del node_tmp")
				os.system("del node_tmp2")
				print("새로운 대표자는 '"+net_data+"'입니다!!")
				representative = net_data

			elif block_protocol == "block_content":
				rep = node_socket.recvfrom(12347)[0].decode('cp949')
				if rep == representative:
					title = node_socket.recvfrom(12347)[0].decode('cp949')
					print(title)
					block = open("chain\\" + title,"wb")
					while True:
						block_data = node_socket.recvfrom(12347)[0]
						if block_data == "end of file".encode():
							break
						block.write(block_data)
					block.close()
					print("새로운 블록 '" + title + "'이 전송되었습니다.")
				else:
					continue

def rep():
	while True:
		rep_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rep_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		rep_socket.settimeout(3)
		rep_socket.bind((node_ip, 12355))
		rep_socket.listen(0)
		try:
			rep_data, addr = rep_socket.accept()
		except:
			continue
		else:
			block_protocol = rep_data.recv(12355)[0:14]
			if not rep_data:
				continue
			elif block_protocol == "block_contents".encode('cp949'):
				title = rep_data.recv(12355).decode('cp949')
				block_file = open("representative\\" + title,"wb")
				while True:
					block_data = rep_data.recv(12355)
					if block_data == "end of file".encode():
						break
					block_file.write(block_data)
				block_file.close()
				print("새로운 블록내용 '" + title + "'이 전송되었습니다.")



t1 = threading.Thread(target=node)
t2 = threading.Thread(target=rep)
t1.start()
t2.start()