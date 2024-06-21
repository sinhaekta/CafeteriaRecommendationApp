import socket

def client_connection(request):
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 12358
    print("in client")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SERVER_HOST, SERVER_PORT))

    client_socket.send(request.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(response)
    client_socket.close()
    return response
