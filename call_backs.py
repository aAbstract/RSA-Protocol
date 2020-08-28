import rsa_lib as rsa
import time


# on authorized connection opend call back
def on_connect(args):
    client = args['client']
    id = args['id']
    print('[INFO (%s)]: RSA AUTH PROTOCOL SUCCEEDED'%(id))
    print('[INFO (%s)]: TESTING RSA TRANSMISSION PROTOCOL'%(id))
    d = args['keys'][1]
    n = args['keys'][2]
    cipher = rsa.encrypt((d, n), 'SECRET MESSAGE FOR %s'%(id))
    cipher = ','.join(map(lambda x: str(x), cipher))
    client.sendall(cipher.encode())
    trans_flag = False
    for i in range(10):
        cipher = client.recv(1024).decode()
        if len(cipher) == 0:
            time.sleep(.1)
            continue
        cipher = map(lambda x: int(x), cipher.split(','))
        recv_text = rsa.decrypt((d, n), cipher)
        print('[INFO (%s)]: (%s) RECEIVED FROM THE SERVER'%(id, recv_text))
        if recv_text == 'COPY:%s'%(id):
            trans_flag = True
            break
        time.sleep(.1)
    if trans_flag:
        print('[INFO (%s)]: TESTING RSA TRANSMISSION PROTOCOL SUCCEEDED'%(id))
    else:
        print('[INFO (%s)]: TESTING RSA TRANSMISSION PROTOCOL FAILD'%(id))
    client.close()


# on data read call back
def on_read(args):
    pass


# on connection error call back
def on_error(args):
    pass


# on connection closed call back
def on_closed(args):
    pass