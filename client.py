import socket, threading, argparse


parser = argparse.ArgumentParser()
parser.add_argument("-a","--address",dest='address',action="store",type=str)
args = parser.parse_args()
if args.address: HOST = args.address
else: HOST = '127.0.0.1'

PORT = 8080

nickname = input("Entry nickname:\n")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except (Exception,ConnectionResetError) as e:
            print(str(e))

            client.close()
            return


def write():
    while True:
        try:
            message_input = input('')
            message = '{} ({}): {}'.format(nickname,str(client.getsockname()), message_input)
            client.send(message.encode('ascii'))
        except Exception as e:
            print(str(e))

            client.close()
            return

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)


try:
    receive_thread.start()
    write_thread.start()
    while True:
        pass

except Exception as e:
    print(str(e))

    client.close()
    exit(1)
