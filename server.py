import socket, threading, argparse


parser = argparse.ArgumentParser()
parser.add_argument("-a","--address",dest='address',action="store",type=str)
args = parser.parse_args()
if args.address: HOST = args.address
else: HOST = '127.0.0.1'

PORT = 8080



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(10)
server.bind((HOST, PORT))
server.listen()


clients_list = []


def broadcast(message):
    for client in clients_list:
        client.send(str(message).encode('ascii'))

def handle(client,address):
    while True:
        try:
            message = client.recv(1024)
            message_str = message.decode('ascii')
            print(message_str)
            broadcast(message_str)
        except Exception as e:
            print("handle {} except: ".format(address),end='')
            print(str(e))
            clients_list.remove(client)
            client.close()
            return


def receive():
    while True:
        try:
            client, address = server.accept()
            print("Connected with {}".format(str(address)))
            clients_list.append(client)

            client.send('Connected to server!'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,address))
            thread.start()

        except socket.timeout as se:
            pass

        except Exception as e:
            print("receive except: ",end='')
            print(str(e))
            server.close()
            return

def write():
    while True:
        try:
            message = str("Server:") + input()
            broadcast(message.encode('ascii'))
        except Exception as e:
            print("write: ",end='')
            print(str(e))
            server.close()
            for c in clients_list:
                c.close()
            return

recv_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

try:
    
    recv_thread.start()
    write_thread.start()
    while True:
        pass
except Exception as e:
    for c in clients_list:
        c.close()
