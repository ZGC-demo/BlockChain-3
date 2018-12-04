block_name = input("읽고 싶은 블럭 이름: ")
block_file = open("id\\" + block_name,"rb")

block_file.seek(0x200)
body = block_file.read(0x200)

body = body[0x5:].decode().replace("\0","\n")

id_list = []
for line in body.splitlines():
	id_list.append(line)
print("\nname: " + id_list[0])
print("private_id: " + id_list[1])
print("birth: " + id_list[2])
print("phone: " + id_list[3])
print("address: " + id_list[4])

block_file.close()