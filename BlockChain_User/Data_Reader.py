block_name = input("읽고 싶은 블럭 이름: ")
with open("chain\\" + block_name,"rb") as block_file:
	head = block_file.read()
	start = 0x86
	end = start + head[start:].find(b'\x00')
	participation_name = head[start:end]
	start = end + 1
	end = start + head[start:].find(b'\x00')
	block_type = head[start:end]
	print("participation_name: " + participation_name.decode('cp949'))
	print("block_type: " + block_type.decode('cp949'))

	#Generate File
	block_file.seek(0x200)
	data = block_file.read()
	data = data[5:].split(b"FOOT")[0] #푸터 전까지 data자르기
	result_file = open("chain\\" + block_name[:-4] + "." + block_type.decode('cp949'), "wb")
	result_file.write(data)
	result_file.close()
print("추출이 완료되었습니다.\n")