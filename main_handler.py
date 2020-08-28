import rsa_lib as rsa
import call_backs as cb
import socket
import _thread
import random
import string
import time


HOST = '127.0.0.1'
PORT = 65432
reg_clients_dict = {}


def auth_session(thread_id, client):
    print('[INFO]: AUTH SESSION (%s) STARTED'%(thread_id))
    data = ''
    for i in range(10):
        temp = client.recv(1024).decode()
        if len(temp) >= 5:
            data = temp
            break
        else:
            time.sleep(.1)
    if data == '':
        print('[INFO]: AUTH SESSION (%s) TIMED OUT')
    else:
        if data[0:3] == '117':
            print('[INFO]: CHECKING CLIENT ID %s'%(data))
            if data in reg_clients_dict:
                print('[INFO]: FETCHING RSA KEY FOR CLIENT %s...'%(data))
                e = int(reg_clients_dict[data][0])
                d = int(reg_clients_dict[data][1])
                n = int(reg_clients_dict[data][2])
                print('[INFO (%s)]: STARTING RSA AUTH PROTOCOL'%(data))
                rand_str = ''.join([random.choice(string.ascii_letters + string.digits) for x in range(32)])
                client.sendall(rand_str.encode())
                auth_flag = False
                for i in range(10):
                    cipher = client.recv(1024).decode()
                    if len(cipher) == 0:
                        time.sleep(.1)
                        continue
                    print('[INFO (%s)]: (%s) RECEIVED FROM CLIENT'%(data, cipher))
                    cipher = cipher.split(',')
                    cipher = map(lambda x: int(x), cipher)
                    recv_text = rsa.decrypt((d, n), cipher)
                    if recv_text == rand_str:
                        auth_flag = True
                        break
                    time.sleep(.1)
                if auth_flag:
                    cb.on_connect({ 'client':client, 'id':data, 'keys':[e, d, n] })
                else:
                    print('[INFO (%s)]: RSA AUTH PROTOCOL FAILD'%(data))
            else:
                print('[INFO]: ID %s NOT FOUND IN THE DATABASE'%(data))
        else:
            print('[INFO]: ID %s NOT A VALID ID IN THE SYSTEM'%(data))


def index_db():
    f = open('rsa_db.txt', 'r')
    items = f.read().split('\n')
    for x in items:
        key_nums = x.split(':')
        reg_clients_dict[key_nums[0]] = key_nums[1:len(key_nums)]


# RUN MAIN SCRIPT WHEN OPENED DIRECTLY IN THE TERMINAL
if __name__ == '__main__':
    print('[INFO]: INDEXING RSA KEYS DATABASE...')
    index_db()
    print('[INFO]: DONE INDEXING RSA KEYS DATABASE')
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    soc.bind((HOST, PORT))
    soc.listen()
    print('[INFO]: RSA SERVER STARTED ON %s:%s'%(HOST, str(PORT)))
    while True:
        print('[INFO]: WAITING FOR CLIENTS...')
        conn, addr = soc.accept()
        print('[INFO]: CLIENT %s:%s CONNECTED'%(addr[0], addr[1]))
        print('[INFO]: STARTING NEW AUTH SESSION...')
        _thread.start_new_thread(auth_session, (''.join([random.choice(string.digits) for x in range(5)]), conn))