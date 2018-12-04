import os
import sys
import random
import socket
import datetime
import pickle
from time import sleep
#from Crypto.PublicKey import RSA
os.system("chcp 949")
os.system("cls")
utility_ip = input("\n본인 ip: ")
while True:
	if utility_ip == "" or len(utility_ip)>20:
		utility_ip = input("\n본인 ip: ")
	else:
		break
server_ip = input("\n서버 ip: ")
while True:
	if server_ip == "" or len(server_ip)>20:
		server_ip = input("\n서버 ip: ")
	else:
		break
#utility_ip = "192.168.0.6"
#server_ip = "192.168.0.6"

while True:
	name = ""
	birth = ""
	phone = ""
	address = ""
	private_id = ""
	name_private = ""

	os.system("cls")
	print("\n\t블록체인\n")
	print("1. 사용자 등록")
	print("2. 블록체인 내용 등록")
	print("3. 투표 요청(상시)")
	print("4. 투표")
	print("5. 블록체인 등록(대표자 전용)")
	print("9. 현재 사용자 아이디")
	print("0. 프로그램 종료")
	print("\n\n")
	print("\t\t\t선택: ", end='')

	menu = input()

	if menu == "1":
		os.system("cls")
		print("===사용자 등록 메뉴===")
		name = input("\n사용자 이름: ")
		while True:
			if name == "" or len(name)>20:
				name = input("\n사용자 이름: ")
			else:
				break
		birth = input("\n주민번호 앞자리: ")
		while True:
			if birth == "" or len(birth)>6:
				birth = input("\n주민번호 앞자리: ")
			else:
				break
		phone = input("\n전화번호: ")
		while True:
			if phone == "" or len(phone)>14:
				phone = input("\n전화번호: ")
			else:
				break
		address = input("\n주소: ")
		while True:
			if address == "" or len(birth)>100:
				address = input("\n주소: ")
			else:
				break
		private_id = str(random.randint(11111,99999))
		
		identification = []
		identification.append(name)
		identification.append(birth)
		identification.append(phone)
		identification.append(address)
		identification.append(private_id)

		print("\n\n기존의 사용자는 삭제됩니다")
		check = input("\n정말 신원을 등록 하시겠습니까?(Y/N): ")
		
		if check == "Y" or check == "y" or check == "ㅛ":

			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				send_socket.connect((server_ip, 12345))#여긴 서버 ip
			except:
				print("\n현재 신원 생성이 불가능합니다(투표중)\n")
				os.system("pause")
				continue
			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			recv_socket.settimeout(3)
			try:
				recv_socket.bind((utility_ip, 12346))#여긴 본인 (localhost x)ip
			except:
				print("\n현재 신원 생성이 불가능합니다(동일 ip 접속중)\n")
				os.system("pause")
				continue
			recv_socket.listen(0)
			send_socket.send("신원 생성중?".encode('cp949'))
			try:
				recv_data, addr = recv_socket.accept()
			except:
				print("현재 신원 생성이 불가능합니다(서버가 다른 신원 생성중)")
				os.system("pause")
				continue
			else:
				response = recv_data.recv(12346).decode()

				if response == "신원 생성가능":
					send_socket.send(pickle.dumps(identification))
					os.system("openssl\\bin\\openssl.exe genrsa" + " -out private_key.pem 2048")
					os.system("openssl\\bin\\openssl.exe genrsa" + " -out private_hash_key.pem 1024")

					#os.system("openssl\\bin\\openssl.exe rsa -in private_key.pem -out " + str(name) + "#" + str(private_id) +
					#			"_public_key.pem -pubout")
					os.system("openssl\\bin\\openssl.exe rsa -in private_key.pem -out " + "public_key.pem -pubout")
					#os.system("openssl\\bin\\openssl.exe rsa -in private_hash_key.pem -out " + str(name) + "#" + str(private_id) +
					#			"_public_hash_key.pem -pubout")
					os.system("openssl\\bin\\openssl.exe rsa -in private_hash_key.pem -out " + "public_hash_key.pem -pubout")
					#with open("private_key.pem", "rb") as p:
					#	private_key = RSA.importKey(p.read())
					#msg = (str(name) + "#" + str(private_id)).encode()
					#enc = private_key.encrypt(msg,1)
					#print(enc)
					#with open("curid","w") as id_file:
					#	id_file.write(str(enc))
					os.system("echo "+str(name)+"#"+str(private_id)+" | openssl\\bin\\openssl.exe rsautl -sign -inkey private_key.pem -out curid")
					os.system("pause")
			send_socket.close()
			recv_socket.close()

		elif check == "N" or check == "n" or check == "ㅜ":
			print("\n등록하지 않았습니다")
			os.system("pause")

		else:
			print("\n등록에 실패하였습니다. 첫 화면으로 돌아갑니다")
			os.system("pause")


	elif menu == "2":
		os.system("cls")
		print("===블록체인 내용 등록 메뉴===\n\n")
		print("먼저, 등록하고 싶은 파일을 blockchain폴더 안의 contents폴더에 넣어주세요\n\n")
		title = input("등록하고 싶은 파일 이름과 확장자를(ex: 블록이름.pdf) 입력해주세요\n: ")
		check = input("\n\n내용 등록을 요청하시겠습니까?(Y/N): ")

		if not os.path.exists("contents\\"+title):
			print("\n'"+title+"'파일이 존재하지 않습니다\n\n첫 화면으로 돌아갑니다.\n")
			os.system("pause")
			continue

		if check == "Y" or check == "y" or check == "ㅛ":
			#파일 찾아서 읽는다 try except else로 파일 없으면 없다고 하고
			#서버에 대표자ip를 요청한다
			#ip 받아와서 서버 공개키로 푼다
			#대표자의 노드로 파일제목과 파일 내용을 보낸다
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			send_socket.settimeout(3)
			try:
				send_socket.connect((server_ip, 12345))#여긴 서버 ip
			except:
				send_socket.close()
				print("\n지금은 요청이 불가능합니다\n")
				os.system("pause")
				continue
			else:
				send_socket.send("블록체인 내용 등록".encode('cp949'))
				sleep(0.5)
				send_socket.send(title.encode('cp949'))
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_key.pem -in curid -out curidtmp -pubin")
				with open("curidtmp","r") as curid:
					curid = curid.read()
				time = str(datetime.datetime.now())[:19].replace(" ","_").replace(":","")
				send_socket.send((time+"_"+curid[:-2]+"."+title.split('.')[1]).encode('cp949'))
				sleep(0.5)
				try:
					with open("contents\\"+title, "rb") as contents:
						for block_contents in contents:
							send_socket.send(block_contents)
				except:
					send_socket.send("no file".encode())
				send_socket.send("end of file".encode())
				send_socket.close()

				print("\n\n블록 등록을 대표자에게 요청했습니다...\n\n중복 등록은 서버에서 무시됩니다\n")
			os.system("pause")

		elif check == "N" or check == "n" or check == "ㅜ":
			print("\n내용 등록을 요청하지 않았습니다\n")
			os.system("pause")

		else:
			print("\n내용 등록 요청에 실패하였습니다. 첫 화면으로 돌아갑니다\n")
			os.system("pause")

	elif menu == "3":
		os.system("cls")
		print("===투표 요청(상시)===")
		name_private = input("\n\n본인 신원(아이디#private_id): ")
		check = input("\n\n상시 투표를 요청하시겠습니까?(Y/N): ")

		if check == "Y" or check == "y" or check == "ㅛ":

			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			send_socket.settimeout(3)
			try:
				send_socket.connect((server_ip, 12345))#여긴 서버 ip
			except:
				send_socket.close()
				print("\n지금은 요청이 불가능합니다\n")
				os.system("pause")
				continue
			else:
				#with open("private_key.pem", "rb") as p2:
				#	private_key = RSA.importKey(p2.read())
				#request_sign = private_key.sign(name_private.encode(),1)
				###############상시투표 본인만 받게 하는 코드
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_key.pem -in curid -out curidtmp -pubin")
				with open("curidtmp","r") as curid:
					current_id = curid.read()
				os.system("del curidtmp")
				if current_id != name_private:
					print("본인의 신원을 입력해주세요!!!")
					os.system("pause")
					continue
				os.system("echo "+str(name_private)+" | openssl\\bin\\openssl.exe rsautl -sign -inkey private_key.pem -out reqtmp")
				with open("reqtmp", "rb") as voteid:
					request_sign = voteid.read()
				with open("public_key.pem","rb") as public:
					key = public.read()
				send_socket.send(("상시 투표 요청!").encode('cp949'))
				send_socket.send(request_sign)
				print(request_sign)
				send_socket.send(key)
				print(key)
				send_socket.close()
				os.system("del reqtmp")

				rating_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				rating_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				rating_socket.bind(('', 12348))
				temp_vote = rating_socket.recvfrom(12348)[0]
				temp_vote_rate = str(temp_vote.decode())
				rating_socket.close()
				print("\n"+temp_vote_rate)
				print("상시 투표를 요청했습니다...\n\n중복 참여 및 미등록자의 참여는 서버에서 무시되며, 한번 참여하면 바꿀 수 없습니다\n")

			os.system("pause")

		elif check == "N" or check == "n" or check == "ㅜ":
			print("\n상시 투표를 요청하지 않았습니다")
			os.system("pause")

		else:
			print("\n상시 투표 요청에 실패하였습니다. 첫 화면으로 돌아갑니다")
			os.system("pause")

	elif menu == "4":
		os.system("cls")
		print("===투표===")
		man_on_the_ballot = input("\n\n선출하고 싶은 사람(아이디#private_id): ")
		check = input("\n\n투표 하시겠습니까?(Y/N): ")

		if check == "Y" or check == "y" or check == "ㅛ":
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			send_socket.settimeout(3)
			try:
				send_socket.connect((server_ip, 12333))#여긴 서버 ip
			except:
				send_socket.close()
				print("\n지금은 요청이 불가능합니다\n\n다시 한번 투표해 주세요\n")
				os.system("pause")
				continue
			else:
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_key.pem -in curid -out curidtmp -pubin")
				with open("curidtmp","r") as curid:
					voter = curid.read()
				os.system("echo "+str(voter[:-2]+":"+man_on_the_ballot)+" | openssl\\bin\\openssl.exe rsautl -sign -inkey private_key.pem -out votetmp")
				with open("votetmp", "rb") as voteid:
					request_sign = voteid.read()
				with open("public_key.pem","rb") as public:
					key = public.read()
				send_socket.send(request_sign)
				send_socket.send(key)
				send_socket.close()
				os.system("del curidtmp")
				os.system("del votetmp")
			os.system("pause")

		elif check == "N" or check == "n" or check == "ㅜ":
			print("\n투표를 요청하지 않았습니다")
			os.system("pause")

		else:
			print("\n투표에 실패하였습니다. 첫 화면으로 돌아갑니다")
			os.system("pause")

	elif menu == "5":
		os.system("cls")
		print("===블록체인 등록(대표자)===")
		send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		send_socket.settimeout(3)
		try:
			send_socket.connect((server_ip, 12345))#여긴 서버 ip
		except:
			send_socket.close()
			print("\n지금은 요청이 불가능합니다\n\n다시 한번 요청해 주세요\n")
			os.system("pause")
			continue
		else:
			send_socket.send("저는 대표자 입니까?".encode('cp949'))

			recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			recv_socket.settimeout(3)
			try:
				recv_socket.bind((utility_ip, 12346))#여긴 본인 (localhost x)ip
			except:
				print("\n대표자만 블록 생성이 가능합니다(동일 ip 접속중)\n")
				os.system("pause")
				continue
			recv_socket.listen(0)
			try:
				recv_data, addr = recv_socket.accept()
			except:
				print("현재 요청이 불가능합니다(서버가 다른 요청 작업중)")
				os.system("pause")
				continue
			else:
				response = recv_data.recv(12346)
				with open("util_verify_tmp","wb") as util_verify_tmp:
					util_verify_tmp.write(response)
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey server_public_key.pem -in util_verify_tmp -out util_verify_tmp2 -pubin")	
				with open("util_verify_tmp2", "rb") as util_verify_tmp2:
					sign_data = util_verify_tmp2.read().decode('cp949')
				os.system("del util_verify_tmp")
				os.system("del util_verify_tmp2")

		if sign_data[:-3] == "맞습니다":
			print("\n\nrepresentative폴더에서 등록을 원하는 파일을 고르세요.")
			registing_block = input("\n\n등록할 파일(ex: a.pdf): ")
			check = input("\n\n블록체인에 등록하시겠습니까?(Y/N): ")
			if not os.path.exists("representative\\"+registing_block):
				print("\n'"+registing_block+"'파일이 존재하지 않습니다\n\n첫 화면으로 돌아갑니다.\n")
				os.system("pause")
				continue
			send_socket.close()
			recv_socket.close()

			if check == "Y" or check == "y" or check == "ㅛ":
				broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_key.pem -in curid -out curidtmp -pubin")
				with open("curidtmp","r") as curid:
					curid = curid.read()[:-2]
				broad_socket.sendto("block_content".encode(), ("255.255.255.255", 12347))
				os.system("del curidtmp")
				broad_socket.sendto(curid.encode('cp949'), ("255.255.255.255", 12347))
				
				file_list = os.listdir("chain")
				file_list.sort()
				prev_block = file_list[-1]
				block_time = str(datetime.datetime.now())[:19].replace(" ","_").replace(":","")
				block_name = block_time + "_" + str(curid) + ".blk"
				participation_name = registing_block.split('_')[2].split('.')[0]
				block_type = registing_block[-3:]
				data_file_path = "representative\\"+registing_block
				broad_socket.sendto(block_name.encode('cp949'), ("255.255.255.255", 12347))

				os.system("Data_Generator.exe " + prev_block + " " + block_name + " " + participation_name + " " + block_type + " " + data_file_path)

				with open("chain\\" + block_name, "rb") as f:
					for block_data in f:
						broad_socket.sendto(block_data, ("255.255.255.255", 12347)) #라우터내 브로드캐스팅 주소
					broad_socket.sendto("end of file".encode(), ("255.255.255.255", 12347))
					broad_socket.close()
				os.system("pause")

			elif check == "N" or check == "n" or check == "ㅜ":
				print("\n블록체인 등록을 요청하지 않았습니다")
				os.system("pause")

			else:
				print("\n블록체인 등록에 실패하였습니다. 첫 화면으로 돌아갑니다")
				os.system("pause")

		else:
			print("\n대표자가 아닙니다. 블록체인 등록을 요청하지 않았습니다.")
			send_socket.close()
			recv_socket.close()
			os.system("pause")




		#이름#private_id를 받아서 개인키 찾은후 서명한 "이름#private_id"문자열과 공개키를 서버에 보낸다

		#서버는 임시파일에 공개키 데이터를 쓰고, 공개키로 풀었을때 리스트에 있는 해당 순서의 대표자 인지 확인 
		#서버는 임시파일 지우고, "생성가능"문자열을 서버 개인키로 암호화하여 서버 공개키와 같이 보낸다

		#유틸에서는 서버 공개키를 임시파일에 쓰고 문자열 풀어본 후, "생성가능"이면 임시파일 지우고	
		#블록 제네레이터로 블록 생성 후 읽어서 노드에 브로드 캐스팅 한다
		#블록 이름은 datetime_파일명.blk로 한다 (파일명은 블록내용이 담긴 파일 이름이다)


	elif menu == "9":
		print("===현재 사용자 아이디===")
		#try:
		#	with open("curid","r") as curid:
		#		with open("private_key.pem", "rb") as pkey:
		#			private_key = RSA.importKey(pkey.read())
		#		current_id1 = curid.read()
		#		current_id2 = private_key.decrypt(current_id1)
		#		print("\n현재 등록된 사용자는 " + current_id1 + " 입니다\n")
		#except:
		#	print("\n현재 등록된 사용자가 없습니다\n")
		os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_key.pem -in curid -out curidtmp -pubin")
		with open("curidtmp","r") as curid:
			print("\n현재 등록된 사용자는 '" + curid.read()[:-2] + "'입니다\n")
		os.system("del curidtmp")
		os.system("pause")

	elif menu == "0":
		os.system("cls")
		sys.exit()

	else:
		os.system("cls")
		print("다시 입력해주세요")
		os.system("pause")



