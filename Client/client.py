import config
import socket

def client_connection(request):
    SERVER_HOST = config.SERVER_HOST
    SERVER_PORT = config.SERVER_PORT

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SERVER_HOST, SERVER_PORT))

    client_socket.send(request.encode('utf-8'))

    response = client_socket.recv(2048).decode('utf-8')

    client_socket.close()
    return response