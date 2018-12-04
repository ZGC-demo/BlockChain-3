#thread socket programming
import threading
import socket
import os
import pickle
import datetime
from time import sleep
import csv

global vote_init #투표 기능 on/off
vote_init = 0
os.system("cls")
server_ip = input("\n본인 ip: ")
while True:
	if server_ip == "" or len(server_ip)>20:
		server_ip = input("\n본인 ip: ")
	else:
		break
#server_ip = "192.168.0.6"

def quicksort(x):
	if len(x) <= 1:
		return x

	pivot = x[len(x) // 2][1]
	less = []
	more = []
	equal = []
	for a in x:
		if a[1] < pivot:
			less.append(a)
		elif a[1] > pivot:
			more.append(a)
		else:
			equal.append(a)

	return quicksort(less) + equal + quicksort(more)

def vote(vote_time):
	voting_result = []
	voters = []
	list_index = 0
	voter_overlap = 0
	interim_overlap = 0
	with open("server_id\\1id_list.txt", "r") as id_list:#참여자가 12000명 초과하면 코드 수정 및 DB 사용 요망
		for info in id_list:
			voting_result.append([info.split()[0],0,info.split()[1]])
	while True:
		end_time = datetime.datetime.now()
		if (vote_time - end_time).seconds > 60: #투표시간 1시간 보다 작아지다가 24시간으로 커진다.끝날때까지
			vote_socket.close()
			print("투표 종료")
			break
		vote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vote_socket.settimeout(1)
		vote_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		vote_socket.bind((server_ip, 12333))#서버 ip
		vote_socket.listen(0)
		try:
			ballot = vote_socket.accept()[0]
		except:
			continue
		else:
			crypto_ballot = ballot.recv(12333)
			with open("ballot_tmp", "wb") as ballot_tmp:
				ballot_tmp.write(crypto_ballot)
			
			key_file = ballot.recv(12333)
			with open("public_vote_key", "wb") as pkey:
				pkey.write(key_file)
			
			os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_vote_key -in ballot_tmp -out ballot_tmp2 -pubin")
			with open("ballot_tmp2", "rb") as ballot_tmp2:
				man_on_the_ballot = ballot_tmp2.read().decode('cp949')
			voter = man_on_the_ballot.split(":")[0]
			interim = man_on_the_ballot.split(":")[1][:-3]
			
			os.system("del ballot_tmp")
			os.system("del ballot_tmp2")
			os.system("del public_vote_key")

			if not man_on_the_ballot:
				vote_socket.close()
				continue
			else:
				print("투표자: "+voter)
				for man in voters:
					if man == voter:
						voter_overlap = 1
						break
				for man2 in voting_result:
					if man2[0] == interim:
						interim_overlap = 1
						break
					list_index = list_index + 1
				if voter_overlap == 0 and interim_overlap == 1:
					voters.append(voter)
					voting_result[list_index][1] = voting_result[list_index][1] + 1

				voter_overlap = 0
				interim_overlap = 0
				list_index = 0
				vote_socket.close()

	voting_result_sort = []
	voting_result_sort = quicksort(voting_result)
	print("새로운 대표자는 '"+voting_result_sort[-1][0]+"'입니다!!")

	os.system("echo "+str(voting_result_sort[-1][0])+" | openssl\\bin\\openssl.exe rsautl -sign -inkey server_private_key.pem -out serv_vote_tmp")
	with open("serv_vote_tmp", "rb") as serv_vote_tmp:
		sign = serv_vote_tmp.read()
	os.system("del serv_vote_tmp")
	broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	broad_socket.sendto(("vote_res_rsut").encode()+sign, ("255.255.255.255", 12347))
	broad_socket.close()

	ip_file = open("rep_info.csv", "w", encoding="UTF-8", newline="")
	ip_csv = csv.writer(ip_file)
	ip_csv.writerow(voting_result_sort[-1])
	ip_file.close()

	voting_result_sort.clear()
	voting_result.clear()

def server():
	os.system("cls")
	request_vote = []
	vote_init = 0

	while True:
		recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			recv_socket.bind((server_ip, 12345))#서버 ip
		except:
			print("-----Error!!!!!-----")
			os.system("pause")
			continue
		recv_socket.listen(0)
		recv_data, addr = recv_socket.accept()
		data = recv_data.recv(12345)
		if not data:
			continue
		elif data.decode('cp949')[0:7] == "신원 생성중?":
			sleep(0.5)
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				send_socket.connect((addr[0],12346))
			except:
				print("사용자쪽 통신채널이 막혀있습니다")
			send_socket.send("신원 생성가능".encode())
			identification = pickle.loads(recv_data.recv(12345))
			print("새로 등록한 신원: " + str(identification))
			file_list = os.listdir("server_id")
			file_list.sort()
			prev_block = file_list[-1]
			with open("server_id\\1id_list.txt", "r") as id_list:
				overlap = 0
				for line in id_list:
					if line == identification[0]+"#"+identification[4]:
						overlap = 1
						break
				if overlap == 0:
					with open("server_id\\1id_list.txt", "a") as id_list2:
						id_list2.write(identification[0]+"#"+identification[4]+" "+str(addr[0])+"\n")

					id_block_name = str(datetime.datetime.now())[:19].replace(" ","_").replace(":","") + "_" + identification[0] + ".blk"
					os.system("ID_Generator.exe " + prev_block + " " + str(id_block_name) + " " + str(identification[0]) + " " + str(identification[1]) + " " + str(identification[2]) + " " + str(identification[3]) + " " + str(identification[4]))

					broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

					os.system("echo "+"신원 등록"+" | openssl\\bin\\openssl.exe rsautl -sign -inkey server_private_key.pem -out id_title_sign")
					with open("id_title_sign", "rb") as id_title_sign:
						id_title_sign = id_title_sign.read()
					os.system("del id_title_sign")
					broad_socket.sendto(("id_block_name").encode(), ("255.255.255.255", 12347))
					sleep(0.5)
					broad_socket.sendto(id_title_sign, ("255.255.255.255", 12347))
					sleep(0.5)

					with open("server_id\\" + id_block_name, "rb") as f:
						broad_socket.sendto(id_block_name.encode(), ("255.255.255.255", 12347))
						sleep(0.5)
						for id_block_data in f:
							broad_socket.sendto(id_block_data, ("255.255.255.255", 12347)) #라우터내 브로드캐스팅 주소
						else:
							broad_socket.sendto("end of file".encode(), ("255.255.255.255", 12347))
							broad_socket.close()
							continue
				elif overlap == 1:
					overlap = 0
					print("****Alert(신원 중복)****		: 신원 등록 취소")
					continue
			send_socket.close()

		elif data.decode('cp949')[0:9] == "상시 투표 요청!" and vote_init == 0:
			part = recv_data.recv(12345)
			with open("vote_tmp","wb") as tmp:
				tmp.write(part)

			key_file = recv_data.recv(12345)
			with open("public_tmp_key","wb") as pkey:
				pkey.write(key_file)
			os.system("openssl\\bin\\openssl.exe rsautl -verify -inkey public_tmp_key -in vote_tmp -out vote_tmp2 -pubin")
			
			with open("vote_tmp2", "rb") as tmp2:
				part = tmp2.read().decode('cp949')[:-3]
			os.system("del vote_tmp")
			os.system("del vote_tmp2")
			os.system("del public_tmp_key")
			overlap = 0
			exist = 0
			count = 0
			with open("server_id\\1id_list.txt", "r") as id_list:
				for line in id_list:
					count = count + 1
					line = line.split(" ")[0]
					if line == part:#서버 id list에 존재하는지 확인
						exist = 1
						for list_line in request_vote:
							if list_line == part:#투표 리스트에 중복되는지 확인
								overlap = 1
								break
			if exist == 0:
				overlap = 1
			if overlap == 0:
				request_vote.append(part)
			elif overlap == 1:
				overlap = 0

			print("상시 투표 요청률: "+ str(len(request_vote)/count*100) + "%")
			rating_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			rating_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			rating_socket.sendto(("상시 투표 요청률: "+ str(len(request_vote)/count*100) + "%\n").encode(), ("255.255.255.255", 12348))
				

			if (len(request_vote)/count*100)>50:
				vote_init = 1
			if vote_init == 1:
				broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				vote_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
				os.system("echo "+str(vote_time)+" | openssl\\bin\\openssl.exe rsautl -sign -inkey server_private_key.pem -out serv_time_tmp")
				with open("serv_time_tmp", "rb") as serv_time_tmp:
					sign = serv_time_tmp.read()
				os.system("del serv_time_tmp")
				broad_socket.sendto(("vote_res_time").encode()+sign, ("255.255.255.255", 12347))
				broad_socket.close()
				count = 0
				request_vote.clear()
				recv_socket.close()
				vote(vote_time)
				vote_init = 0
		
		#elif 절대투표시간:
			#broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			#broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
			#vote_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
			#broad_socket.sendto(("vote_res" + str(vote_time)).encode(), ("255.255.255.255", 12347))
			#broad_socket.close()
			#vote(absolute_vote_time)

		elif data.decode('cp949')[0:10] == "블록체인 내용 등록":
			tmp_overlap = 0
			success = 0
			title = recv_data.recv(12345)
			title = title.decode('cp949')
			#contents = recv_data.recv(12345)
			with open("tmp\\tmp_list.txt","r") as tmp_list:
				for line in tmp_list:
					if title.replace("\r\n","") == line.replace("\n",""):
						tmp_overlap = 1
						break
			if tmp_overlap == 0:
				title2 = recv_data.recv(12345)
				title2 = title2.decode('cp949')
				block = open("tmp\\" + title2,"wb")
				while True:
					contents = recv_data.recv(12345)
					if contents == "end of file".encode():
						block.close()
						break
					elif contents == "no file".encode():
						block.close()
						os.system("del tmp\\"+title2)
						print("잘못된 블록에 대한 요청이 들어왔습니다 (" + addr[0] + ")")
						success = 1
						break
					block.write(contents)
				if success == 0:
					with open("tmp\\tmp_list.txt","a") as tmp_list2:
						tmp_list2.write(title+"\n")
					print("블록내용 '" + title + "'이 전송되었습니다.")
					ip_file = open("rep_info.csv", "r", encoding="UTF-8")
					ip_csv = csv.reader(ip_file)
					for ip_address in ip_csv:
						rep_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						rep_node.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
						rep_node.settimeout(3)
						while True:
							try:
								rep_node.connect((ip_address[2], 12355))
							except:
								continue
							else:
								rep_node.send("block_contents".encode('cp949'))
								sleep(0.5)
								rep_node.send(title2.replace("\r\n","").encode('cp949'))
								sleep(0.5)
								with open("tmp\\"+title2, "rb") as contents:
									for block_contents in contents:
										rep_node.send(block_contents)
								sleep(0.5)
								rep_node.send("end of file".encode())
								rep_node.close()
								os.system("del tmp\\"+title2)
								break
				recv_socket.close()
			else:
				print("중복된 블록내용에 대한 요청이 들어왔습니다 (" + addr[0] + ")")
				recv_socket.close()

		elif data.decode('cp949')[0:11] == "저는 대표자 입니까?":
			send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				send_socket.connect((addr[0],12346))
			except:
				print("사용자쪽 통신채널이 막혀있습니다")
			else:
				ip_file = open("rep_info.csv", "r", encoding="UTF-8")
				ip_csv = csv.reader(ip_file)
				ip_match = 0
				for ip_address in ip_csv:
					if ip_address[2] == addr[0]:
						os.system("echo "+ "맞습니다" +" | openssl\\bin\\openssl.exe rsautl -sign -inkey server_private_key.pem -out rep_verify_tmp")
						with open("rep_verify_tmp", "rb") as rep_verify_tmp:
							sign = rep_verify_tmp.read()
						os.system("del rep_verify_tmp")
						send_socket.send(sign)
						print("대표자가 블록체인에 등록을 시도합니다")
						ip_match = 1
						break
				if ip_match == 0:
					send_socket.send("아닙니다".encode('cp949'))
			send_socket.close()

os.system("chcp 949")
server()