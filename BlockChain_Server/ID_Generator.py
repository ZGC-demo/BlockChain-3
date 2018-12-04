import sys
import os

prev_block = sys.argv[1]
block_name = sys.argv[2]
name = sys.argv[3]
birth = sys.argv[4]
phone = sys.argv[5]
address = sys.argv[6]
private_id = sys.argv[7]

prev_block_file = open("server_id\\" + prev_block,"rb")
block_file = open("server_id\\" + block_name,"wb")
tmp_file = open("tmp2", "wb")

#reading prev hash
prev_block_file.seek(-0x80,2)#hash size(0x80),end of file
prev_hash = prev_block_file.read()
prev_block_file.close()

#Generate Header
block_file.write(b"HEAD" + b'\0')
block_file.write(prev_hash + b'\0')

tmp_file.write(b"HEAD" + b'\0')
tmp_file.write(prev_hash + b'\0')

#Generate Body
block_file.seek(0x200)
block_file.write(str.encode("BODY") + b'\0')
block_file.write(str.encode(name) + b'\0')
block_file.write(str.encode(private_id) + b'\0')
block_file.write(str.encode(birth) + b'\0')
block_file.write(str.encode(phone) + b'\0')
block_file.write(str.encode(address) + b'\0')

tmp_file.seek(0x200)
tmp_file.write(str.encode("BODY") + b'\0')
tmp_file.write(str.encode(name) + b'\0')
tmp_file.write(str.encode(private_id) + b'\0')
tmp_file.write(str.encode(birth) + b'\0')
tmp_file.write(str.encode(phone) + b'\0')
tmp_file.write(str.encode(address) + b'\0')

tmp_file.close()

#Generate Hashing data
os.system("openssl\\bin\\openssl.exe dgst -sha512 -sign server_private_hash_key.pem -out hash2 tmp2")

#Generate Encrypt data
os.system("openssl\\bin\\openssl.exe rsautl -sign -inkey server_private_key.pem -in hash2 -out pcrypt2")

#Generate Hashing data2
os.system("openssl\\bin\\openssl.exe dgst -sha512 -sign server_private_hash_key.pem -out tmp2 pcrypt2")

#Generate Footer
encrypt_tmp_file = open("tmp2", "rb")
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
block_file.close()

#Removed temp file
os.system("del tmp2")
os.system("del pcrypt2")
os.system("del hash2")