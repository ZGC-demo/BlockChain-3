import sys
import os

prev_block = sys.argv[1]
block_name = sys.argv[2]
#block_seq = sys.argv[3]
#representitive_seq = sys.argv[4]
participation_name = sys.argv[3]
block_type = sys.argv[4]
data_flag = 0
if sys.argv[5] != "no":
	data_file_path = sys.argv[5]
	data_flag = 1

prev_block_file = open("chain\\" + prev_block,"rb")
block_file = open("chain\\" + block_name,"wb")
if data_flag == 1:
	data_file = open(data_file_path,"rb")
tmp_file = open("block_chain_tmp", "wb")

#reading prev hash
prev_block_file.seek(-0x80,2)#hash size(0x80),end of file
prev_hash = prev_block_file.read()
prev_block_file.close()

#Generate Header
block_file.write(b"HEAD" + b'\0')
block_file.write(prev_hash + b'\0')
#block_file.write(str.encode(block_seq) + b'\0')
#block_file.write(str.encode(representitive_seq) + b'\0')
block_file.write(str.encode(participation_name,'cp949') + b'\0')
block_file.write(str.encode(block_type,'cp949') + b'\0')

tmp_file.write(b"HEAD" + b'\0')
tmp_file.write(prev_hash + b'\0')
#tmp_file.write(str.encode(block_seq) + b'\0')
#tmp_file.write(str.encode(representitive_seq) + b'\0')
tmp_file.write(str.encode(participation_name,'cp949') + b'\0')
tmp_file.write(str.encode(block_type,'cp949') + b'\0')

#Generate Body
block_file.seek(0x200)
block_file.write(str.encode("BODY") + b'\0')
if data_flag == 1:
	data = data_file.read()
	block_file.write(data)

tmp_file.seek(0x200)
tmp_file.write(str.encode("BODY") + b'\0')
if data_flag == 1:
	tmp_file.write(data)
	data_file.close()
tmp_file.close()

#Generate Hashing data
os.system("openssl\\bin\\openssl.exe dgst -sha512 -sign private_hash_key.pem -out hash block_chain_tmp")

#Generate Encrypt data
os.system("openssl\\bin\\openssl.exe rsautl -sign -inkey private_key.pem -in hash -out pcrypt")

#Generate Hashing data2
os.system("openssl\\bin\\openssl.exe dgst -sha512 -sign private_hash_key.pem -out encrypt_block_tmp pcrypt")

#Generate Footer
encrypt_tmp_file = open("encrypt_block_tmp", "rb")
offset = block_file.tell() - 1
block_file.seek((int(offset / 0x200) + 0x01) * 0x200)

block_file.write(str.encode("FOOT") + b'\0')
encrypt_tmp_data = encrypt_tmp_file.read()
block_file.write(encrypt_tmp_data)
#os.system("openssl.exe dgst -sha512 -sign private_key.pem -out hash tmp")
#os.system("openssl.exe dgst -sha512 -sign private_key.pem -passin pass:rufqls -out result.txt sample.txt")
#os.system("openssl.exe rsautl -sign -inkey private_key.pem -in tmp.txt -out sing.txt")
#os.system("openssl.exe rsautl -verify -inkey 전찬빈#14916_public_key.pem -in sign.txt -out out.txt -pubin")
encrypt_tmp_file.close()
encrypt_tmp_file.close()
block_file.close()

#Removed temp file
os.system("del block_chain_tmp")
os.system("del encrypt_block_tmp")
os.system("del pcrypt")
os.system("del hash")