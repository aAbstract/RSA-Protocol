import socket
import rsa_lib as rsa


HOST = '127.0.0.1'
PORT = 65432
rsa_params = '11700:6719:8479:14971'


rsa_items = rsa_params.split(':')
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORT))
print('[INFO]: CONNECTED TO THE SERVER')
soc.sendall(rsa_items[0].encode()) # SEND ID ONCE CONNECTED
print('[INFO]: RSA ID SENT')
cipher = soc.recv(1024).decode()
print('[INFO]: (%s) RECEIVED FROM THE SERVER'%(cipher))
res = rsa.encrypt((int(rsa_items[1]), int(rsa_items[-1])), cipher)
soc.sendall(','.join(map(lambda x: str(x), res)).encode())
print('[INFO]: (%s) SENT TO THE SERVER'%(','.join(map(lambda x: str(x), res))))
data_cipher = soc.recv(1024).decode()
print('[INFO]: TRANSMISSION STARTED')
print('[INFO]: (%s) RECEIVED FROM THE SERVER'%(data_cipher))
data_text = rsa.decrypt((int(rsa_items[1]), int(rsa_items[-1])), map(lambda x: int(x), data_cipher.split(',')))
print('[INFO]: (%s) DATA DECRYPTED'%(data_text))
end_text = 'COPY:' + rsa_items[0]
end_cipher = rsa.encrypt((int(rsa_items[1]), int(rsa_items[-1])), end_text)
print('[INFO]: SENDING (%s) TO THE SERVER...'%(end_text))
soc.sendall(','.join(map(lambda x: str(x), end_cipher)).encode())
print('[INFO]: SENT (%s) TO THE SERVER'%(','.join(map(lambda x: str(x), end_cipher))))
soc.close()